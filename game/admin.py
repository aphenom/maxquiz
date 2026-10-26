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
    list_display = ("name", "kind", "slug", "join_code", "dashboard_username", "dashboard_code", "active",
                    "members_only", "subscription_required", "trial_enabled", "trial_days", "free_until")
    list_editable = ("trial_enabled", "trial_days")
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
    list_display = ("membership", "plan", "amount", "payment_ref", "status", "start_date", "end_date", "created_at")
    list_filter = ("status", "plan", "membership__space")
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
