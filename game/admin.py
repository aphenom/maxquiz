from django import forms
from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from django.utils.html import format_html, escape
from django.utils.safestring import mark_safe
from .models import (GameConfig, Player, Question, AdCampaign,
                     GameSession, Answer, JokerUse, Withdrawal, Space,
                     Category, SubCategory, Theme, Quiz, Membership, License, AuditLog,
                     Subscription, Teacher, Resource, Lesson, LiveSession, SessionBooking,
                     PushDevice, Notification)

admin.site.site_header = "MaxQuiz — MQ Technologies"
admin.site.site_title = "MaxQuiz"
admin.site.index_title = "Back-office MaxQuiz"
admin.site.index_template = "admin/mq_index.html"


@admin.register(GameConfig)
class GameConfigAdmin(admin.ModelAdmin):
    list_display = ("__str__", "daily_question_count", "daily_pot",
                    "joker_max_per_game", "joker_paid_enabled", "joker_ad_enabled")

    def has_add_permission(self, request):
        return not GameConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("pseudo", "phone", "city", "balance", "created_at")
    search_fields = ("pseudo", "phone")


@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ("name", "kind", "price_monthly", "price_quarterly", "price_yearly", "trial_enabled",
                    "trial_days", "slug", "join_code", "dashboard_username", "dashboard_code", "active",
                    "members_only", "subscription_required", "free_until")
    list_editable = ("price_monthly", "price_quarterly", "price_yearly", "trial_enabled", "trial_days")
    list_filter = ("kind", "active")
    prepopulated_fields = {"slug": ("name",)}


from django import forms


class LessonAdminForm(forms.ModelForm):
    pdf_file = forms.FileField(label="Fiche PDF (5 Mo max.)", required=False)

    class Meta:
        model = Lesson
        exclude = ("pdf_data", "pdf_name")

    def clean_pdf_file(self):
        f = self.cleaned_data.get("pdf_file")
        if f and (f.size > Lesson.MAX_PDF_BYTES or not f.name.lower().endswith(".pdf")):
            raise forms.ValidationError("Un PDF de 5 Mo maximum.")
        return f

    def save(self, commit=True):
        obj = super().save(commit=False)
        f = self.cleaned_data.get("pdf_file")
        if f:
            obj.pdf_name, obj.pdf_data = f.name[:200], f.read()
        if commit:
            obj.save()
        return obj


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Les cours communs MQ (sans espace) se créent ici : niveau, matière et
    chapitre doivent reprendre les libellés des quiz partagés."""
    form = LessonAdminForm
    list_display = ("title", "space", "shared_level_name", "shared_subject_name", "shared_theme_name",
                    "sub_category", "has_video", "pdf_name", "free_preview", "active")
    list_filter = ("space", "active", "free_preview")
    search_fields = ("title", "shared_theme_name")

    @admin.display(boolean=True, description="Vidéo")
    def has_video(self, obj):
        return bool(obj.video_id)


@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ("title", "space", "teacher", "starts_at", "provider", "price_live", "price_replay", "cancelled")
    list_filter = ("space", "provider", "cancelled")


@admin.register(SessionBooking)
class SessionBookingAdmin(admin.ModelAdmin):
    list_display = ("membership", "session", "kind", "amount", "payment_ref", "status", "created_at")
    list_filter = ("status", "kind", "session__space")


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "space", "username", "role", "active")
    list_filter = ("space", "role", "active")
    filter_horizontal = ("sub_categories",)
    exclude = ("password_hash",)


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "space", "sub_category", "theme", "teacher", "status", "created_at")
    list_filter = ("space", "status")
    exclude = ("data",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("membership", "plan", "amount", "list_price", "promo", "provider", "payment_method", "payment_ref",
                    "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "provider", "payment_method", "plan", "membership__space", "promo")
    search_fields = ("membership__full_name", "membership__external_ref", "payment_ref", "payer_phone")


@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ("space", "period_label", "billing_mode", "seat_count",
                    "seats_used", "price", "jokers_allowed", "reward_type", "active",
                    "start_date", "end_date")
    list_filter = ("space", "billing_mode", "jokers_allowed", "active")


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("full_name", "space", "license", "category", "sub_category", "phone",
                    "external_ref", "player", "matched_at")
    list_filter = ("space", "license", "category")
    search_fields = ("full_name", "phone", "external_ref")


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "space", "order")
    list_filter = ("space",)
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SubCategoryInline]


@admin.register(Theme)
class ThemeAdmin(admin.ModelAdmin):
    list_display = ("name", "sub_category", "order")
    list_filter = ("sub_category__category__space",)
    prepopulated_fields = {"slug": ("name",)}


class DatalistTextInput(forms.TextInput):
    """Champ texte avec suggestions (noms de Catégorie/Sous-catégorie déjà
    utilisés) : garde la souplesse du texte libre (un niveau pas encore créé
    par aucun espace reste saisissable) tout en réduisant le risque de faute
    de frappe qui casserait silencieusement le rattachement par nom."""
    def __init__(self, datalist_id, options, attrs=None):
        self.datalist_id = datalist_id
        self.options = options
        merged = {"list": datalist_id, "autocomplete": "off"}
        if attrs:
            merged.update(attrs)
        super().__init__(attrs=merged)

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        options_html = mark_safe("".join(f'<option value="{escape(opt)}">' for opt in self.options))
        return format_html('{}<datalist id="{}">{}</datalist>', input_html, self.datalist_id, options_html)


class QuizAdminForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        levels = sorted(set(Category.objects.values_list("name", flat=True)))
        subjects = sorted(set(SubCategory.objects.values_list("name", flat=True)))
        self.fields["shared_level_name"].widget = DatalistTextInput("shared-level-names", levels)
        self.fields["shared_subject_name"].widget = DatalistTextInput("shared-subject-names", subjects)


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    form = QuizAdminForm
    list_display = ("name", "space", "shared_level_name", "shared_subject_name", "category", "sub_category",
                    "theme", "replay_policy", "reward_type", "joker_enabled", "active", "created_at")
    list_filter = ("space", "category", "replay_policy", "joker_enabled", "active")
    prepopulated_fields = {"slug": ("name",)}
    fieldsets = (
        (None, {"fields": ("name", "slug", "active")}),
        ("Quiz propre à un espace", {
            "fields": ("space", "category", "sub_category", "theme"),
            "description": "À remplir pour un quiz propre à un établissement précis. Laisser "
                           "« Espace » vide si ce quiz est partagé (voir ci-dessous) — dans ce cas, "
                           "ne pas remplir ces champs non plus, ils ne s'appliqueraient qu'à un seul espace.",
        }),
        ("Quiz partagé (sans espace, par niveau/matière)", {
            "fields": ("shared_level_name", "shared_subject_name"),
            "description": "À remplir seulement si « Espace » ci-dessus est vide : le quiz devient "
                           "automatiquement disponible dans tout établissement dont une catégorie/sous-catégorie "
                           "porte ce nom (comparaison insensible à la casse), avec sa propre banque de questions "
                           "(à ajouter depuis l'admin Question, champ « Quiz partagé »).",
        }),
        ("Paramètres de jeu", {"fields": ("question_count", "survey_every", "elimination",
                                          "replay_policy", "show_corrections")}),
        ("Récompense & joker", {"fields": ("reward_type", "reward_text", "joker_enabled")}),
    )


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "space", "quiz", "kind", "category", "sub_category", "theme", "difficulty", "active")
    list_filter = ("space", "quiz", "kind", "category", "sub_category", "difficulty", "active")
    list_editable = ("difficulty", "active")
    search_fields = ("text",)


@admin.register(AdCampaign)
class AdCampaignAdmin(admin.ModelAdmin):
    list_display = ("brand", "tagline", "is_video", "active", "impressions", "clicks")
    list_filter = ("active", "is_video")


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0
    readonly_fields = ("question", "choice", "time_ms", "is_correct", "saved_by_joker")


class JokerInline(admin.TabularInline):
    model = JokerUse
    extra = 0
    readonly_fields = ("question_index", "kind", "price", "ad", "created_at")


@admin.register(GameSession)
class GameSessionAdmin(admin.ModelAdmin):
    list_display = ("player", "day", "status", "reached", "jokers_used",
                    "pot_share", "paid_out", "flagged")
    list_filter = ("status", "day", "flagged", "paid_out")
    inlines = [AnswerInline, JokerInline]
    actions = ["payout_pot"]

    @admin.action(description="💰 Répartir la cagnotte du jour entre les finalistes sélectionnés")
    def payout_pot(self, request, queryset):
        cfg = GameConfig.get()
        finalists = queryset.filter(status="finished", flagged=False, paid_out=False)
        n = finalists.count()
        if not n:
            self.message_user(request, "Aucun finaliste non payé dans la sélection.")
            return
        share = cfg.daily_pot // n
        for s in finalists:
            s.pot_share = share
            s.paid_out = True
            s.player.balance += share
            s.player.save(update_fields=["balance"])
            s.save(update_fields=["pot_share", "paid_out"])
        self.message_user(request, f"{n} finaliste(s) crédité(s) de {share} F chacun.")


@admin.register(Withdrawal)
class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ("player", "amount", "momo_number", "status", "created_at")
    list_filter = ("status",)
    list_editable = ("status",)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "space", "actor", "action", "model_name", "object_repr")
    list_filter = ("action", "model_name", "space")
    search_fields = ("object_repr", "actor", "details")
    readonly_fields = [f.name for f in AuditLog._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(PushDevice)
class PushDeviceAdmin(admin.ModelAdmin):
    list_display = ("player", "teacher", "kind", "active", "created_at", "last_success_at")
    list_filter = ("kind", "active")


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "player", "teacher", "kind", "pushed", "created_at", "read_at")
    list_filter = ("kind",)
    search_fields = ("title", "body")


from .models import AdAttribution


@admin.register(AdAttribution)
class AdAttributionAdmin(admin.ModelAdmin):
    list_display = ("player", "utm_source", "utm_campaign", "utm_content", "consent", "created_at")
    list_filter = ("utm_source", "consent")
    search_fields = ("utm_campaign", "utm_content", "player__phone")
    readonly_fields = [f.name for f in AdAttribution._meta.fields]


# --- Signalements et assistance -------------------------------------------------
from django.urls import reverse  # noqa: E402

from .models import Signalement  # noqa: E402


@admin.register(Signalement)
class SignalementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "status", "kind", "motif", "cible", "apercu", "contact")
    list_filter = ("status", "kind", "motif", ("created_at", admin.DateFieldListFilter))
    list_editable = ("status",)
    search_fields = ("message", "question__text", "lesson__title", "contact")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at", "handled_at", "kind", "motif", "message", "player", "contact", "page",
                       "contenu_signale")
    fields = ("status", "reponse", "note", "kind", "motif", "message", "contenu_signale", "player", "contact",
              "page", "created_at", "handled_at")
    actions = ("marquer_en_cours", "marquer_traite", "marquer_sans_suite")
    list_per_page = 50

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("question__quiz", "lesson", "player")

    def changelist_view(self, request, extra_context=None):
        n = Signalement.objects.filter(status="nouveau").count()
        extra_context = {**(extra_context or {}),
                         "title": f"Signalements et assistance — {n} nouveau{'x' if n > 1 else ''}"}
        return super().changelist_view(request, extra_context)

    @admin.display(description="Contenu")
    def cible(self, obj):
        if obj.question_id:
            url = reverse("admin:game_question_change", args=[obj.question_id])
            return format_html('<a href="{}">Question · {}</a>', url, obj.question.text[:50])
        if obj.lesson_id:
            url = reverse("admin:game_lesson_change", args=[obj.lesson_id])
            return format_html('<a href="{}">Cours · {}</a>', url, obj.lesson.title[:50])
        return "—"

    @admin.display(description="Message")
    def apercu(self, obj):
        return (obj.message[:70] + "…") if len(obj.message) > 70 else (obj.message or "—")

    @admin.display(description="Contenu signalé")
    def contenu_signale(self, obj):
        q = obj.question
        if q:
            opts = "".join(
                format_html('<li{}>{}{}</li>', mark_safe(' style="font-weight:700;color:#0B9A5C"') if i == q.correct else "",
                            o, " ✔" if i == q.correct else "")
                for i, o in enumerate([q.option_a, q.option_b, q.option_c, q.option_d]))
            where = f"{q.quiz.shared_level_name} · {q.quiz.shared_subject_name} · {q.quiz.name}" if q.quiz_id else ""
            return format_html('<p><b>{}</b><br>{}</p><ul>{}</ul><p><i>Explication :</i> {}</p><p><a href="{}">Corriger la question</a></p>',
                               where, q.text, mark_safe(opts), q.explanation or "—",
                               reverse("admin:game_question_change", args=[q.id]))
        if obj.lesson_id:
            return format_html('<p><b>{}</b> ({} · {})</p><p><a href="{}">Corriger le cours</a></p>',
                               obj.lesson.title, obj.lesson.shared_level_name, obj.lesson.shared_subject_name,
                               reverse("admin:game_lesson_change", args=[obj.lesson_id]))
        return "—"

    def _close(self, obj, status):
        """Passage à « Traité » : date de traitement et notification à l'élève (une seule fois)."""
        first_time = status == "traite" and obj.handled_at is None
        obj.status = status
        if status in ("traite", "rejete") and obj.handled_at is None:
            obj.handled_at = timezone.now()
        obj.save()
        if first_time and obj.player_id:
            from .push import notify
            if obj.kind == "contenu":
                title = "Merci pour ton signalement !"
                body = obj.reponse or "L'erreur que tu as signalée a été vérifiée et corrigée."
            else:
                title = "Réponse de l'assistance MaxQuiz"
                body = obj.reponse or "Ta demande a été traitée. Écris-nous si tu as encore besoin d'aide."
            notify(players=[obj.player], title=title, body=body, url=reverse("aide"), kind="info")

    def save_model(self, request, obj, form, change):
        status = obj.status
        if change:
            previous = Signalement.objects.get(pk=obj.pk)
            obj.handled_at = previous.handled_at
        self._close(obj, status)

    @admin.action(description="Marquer « En cours »")
    def marquer_en_cours(self, request, queryset):
        queryset.update(status="en_cours")

    @admin.action(description="Marquer « Traité » (prévient l'élève)")
    def marquer_traite(self, request, queryset):
        for obj in queryset:
            self._close(obj, "traite")

    @admin.action(description="Marquer « Sans suite »")
    def marquer_sans_suite(self, request, queryset):
        for obj in queryset:
            self._close(obj, "rejete")



from .models import Mission, Rappels  # noqa: E402


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ("day", "player", "kind", "title", "pushed_at", "opened_at")
    list_filter = ("kind", "day", "space")
    search_fields = ("player__phone", "player__pseudo", "title")
    date_hierarchy = "day"


@admin.register(Rappels)
class RappelsAdmin(admin.ModelAdmin):
    list_display = ("player", "actifs", "heure", "pause_jusquau", "ignores", "dernier_envoi", "derniere_visite")
    list_filter = ("actifs",)
    search_fields = ("player__phone", "player__pseudo")



from .models import Telechargement, Visite  # noqa: E402


@admin.register(Telechargement)
class TelechargementAdmin(admin.ModelAdmin):
    list_display = ("created_at", "kind", "source", "player")
    list_filter = ("kind", "day", "source")
    date_hierarchy = "day"


@admin.register(Visite)
class VisiteAdmin(admin.ModelAdmin):
    list_display = ("created_at", "page", "source", "device", "in_app", "player")
    list_filter = ("day", "device", "in_app", "source")
    date_hierarchy = "day"

    def has_add_permission(self, request):
        return False



from .models import CodePromo  # noqa: E402


@admin.register(CodePromo)
class CodePromoAdmin(admin.ModelAdmin):
    list_display = ("code", "partenaire", "percent", "commission", "formules", "utilisations", "filleuls_count",
                    "max_uses", "first_only", "starts_on", "ends_on", "active")
    list_editable = ("active",)
    list_filter = ("active", "percent", "first_only")
    search_fields = ("code", "note", "partenaire")
    readonly_fields = ("lien",)

    @admin.display(description="Lien à partager")
    def lien(self, obj):
        from django.conf import settings as dj
        if not obj.pk:
            return "Disponible après l'enregistrement."
        url = f"{(dj.SITE_URL or 'https://maxquiz.net').rstrip('/')}/p/{obj.code}/"
        return format_html('<code>{}</code>', url)

    @admin.display(description="Inscrits via le lien")
    def filleuls_count(self, obj):
        return obj.filleuls.count()
    fieldsets = (
        (None, {"fields": ("code", "percent", "note", "active")}),
        ("Influenceur ou partenaire", {"fields": ("partenaire", "contact", "commission", "lien"),
                                       "description": "Pour un influenceur : son nom, son contact et sa commission. "
                                                      "Partage-lui le lien ci-dessous (après enregistrement)."}),
        ("Formules concernées", {"fields": ("monthly", "quarterly", "yearly")}),
        ("Utilisations", {"fields": ("max_uses", "max_per_player", "first_only"),
                          "description": "Code unique : « Utilisations au total » = 1. Code réutilisable par "
                                         "plusieurs comptes : 0 (illimité) ou un plafond, et 1 utilisation par compte."}),
        ("Période", {"fields": ("starts_on", "ends_on")}),
        ("Espace", {"fields": ("space",), "classes": ("collapse",)}),
    )

    @admin.display(description="Formules")
    def formules(self, obj):
        names = {"monthly": "mensuel", "quarterly": "trimestriel", "yearly": "annuel"}
        return ", ".join(names[c] for c in obj.plans()) or "—"

    @admin.display(description="Utilisé")
    def utilisations(self, obj):
        from .promos import _uses
        validated = obj.subscriptions.filter(status="active").count()
        return f"{_uses(obj.subscriptions.all()).count()} (dont {validated} payé{'s' if validated > 1 else ''})"



from .models import SmsEnvoi  # noqa: E402


@admin.register(SmsEnvoi)
class SmsEnvoiAdmin(admin.ModelAdmin):
    list_display = ("created_at", "phone", "operateur", "kind", "sender_name", "status", "status_at", "error")
    list_filter = ("status", "operateur", "kind", "provider")
    search_fields = ("phone", "resource_id")
    date_hierarchy = "created_at"
