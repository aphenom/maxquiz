from django.contrib import admin
from django.db.models import Sum
from django.utils import timezone
from .models import (GameConfig, Player, Question, AdCampaign,
                     GameSession, Answer, JokerUse, Withdrawal, Space,
                     Category, SubCategory, Quiz, Membership)

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
    list_display = ("name", "slug", "active", "consent_required", "question_count", "elimination", "dashboard_code")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Membership)
class MembershipAdmin(admin.ModelAdmin):
    list_display = ("full_name", "space", "category", "sub_category", "phone",
                    "external_ref", "player", "matched_at")
    list_filter = ("space", "category")
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


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("name", "space", "category", "sub_category", "active", "created_at")
    list_filter = ("space", "category", "active")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "space", "kind", "category", "sub_category", "difficulty", "active")
    list_filter = ("space", "kind", "category", "sub_category", "difficulty", "active")
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
