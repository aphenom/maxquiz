import random

from django.db import models
from django.utils import timezone


class SoftDeleteManager(models.Manager):
    """Manager par défaut d'un modèle « suppression douce » : exclut les lignes
    marquées supprimées (deleted_at renseigné) de tout accès normal — y compris
    les relations inverses (ex. category.subcategories.all()), Django utilisant
    le manager par défaut du modèle pour celles-ci. Rien n'est donc jamais
    réellement effacé par les actions du tableau de bord établissement : la
    ligne reste en base, récupérable (voir AuditLog et la restauration), juste
    filtrée de l'affichage normal. Utiliser `all_objects` pour tout voir
    (administration, audit, restauration)."""
    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class GameConfig(models.Model):
    """Configuration du jeu, modifiable dans l'admin (singleton)."""
    daily_question_count = models.PositiveSmallIntegerField("Questions du défi", default=50)
    # Répartition des difficultés en % (1 facile → 4 expert)
    difficulty_mix = models.JSONField("Répartition difficulté (%)", default=dict)
    # Chrono en secondes par niveau de difficulté
    timer_by_difficulty = models.JSONField("Chrono par difficulté (s)", default=dict)
    ad_every = models.PositiveSmallIntegerField("Pub toutes les N questions", default=3)
    # Interrupteur général : récompenses et jokers ne sont plus le cœur du jeu,
    # désactivés par défaut sur une nouvelle installation.
    rewards_enabled = models.BooleanField("Récompenses et jokers activés (jeu public)", default=False)
    # Jokers
    joker_paid_enabled = models.BooleanField("Joker payant activé", default=True)
    joker_ad_enabled = models.BooleanField("Joker publicité activé", default=True)
    joker_max_per_game = models.PositiveSmallIntegerField("Jokers max par partie", default=3)
    joker_price_by_difficulty = models.JSONField("Prix joker par difficulté (F)", default=dict)
    # Cagnotte du jour, partagée entre tous les finalistes
    daily_pot = models.PositiveIntegerField("Cagnotte du jour (F CFA)", default=100000)
    pot_sponsor = models.CharField("Sponsor de la cagnotte", max_length=80, blank=True, default="")

    class Meta:
        verbose_name = "Configuration du jeu"

    def save(self, *args, **kwargs):
        self.pk = 1
        if not self.difficulty_mix:
            self.difficulty_mix = {"1": 40, "2": 30, "3": 20, "4": 10}
        if not self.timer_by_difficulty:
            self.timer_by_difficulty = {"1": 15, "2": 12, "3": 9, "4": 6}
        if not self.joker_price_by_difficulty:
            self.joker_price_by_difficulty = {"1": 100, "2": 200, "3": 500, "4": 1000}
        super().save(*args, **kwargs)

    @classmethod
    def get(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return "Configuration MaxQuiz"


class Player(models.Model):
    phone = models.CharField("Téléphone", max_length=20, unique=True, null=True, blank=True)
    pseudo = models.CharField("Pseudo", max_length=30)
    full_name = models.CharField("Nom complet", max_length=80, blank=True, default="")
    city = models.CharField("Ville", max_length=50, blank=True, default="")
    balance = models.PositiveIntegerField("Solde (F CFA)", default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Joueur"

    def __str__(self):
        return self.pseudo


class Question(models.Model):
    CATEGORIES = [
        ("ci", "Côte d'Ivoire & Afrique"), ("cg", "Culture générale"),
        ("ec", "École & savoirs"), ("sp", "Sport & actu"),
    ]
    DIFFICULTIES = [(1, "Facile"), (2, "Moyen"), (3, "Difficile"), (4, "Expert")]
    KINDS = [("quiz", "Quiz (bonne réponse)"), ("survey", "Sondage (opinion)")]
    space = models.ForeignKey("Space", null=True, blank=True, on_delete=models.CASCADE,
                              related_name="questions",
                              verbose_name="Espace (vide = jeu public MaxQuiz)")
    kind = models.CharField("Type", max_length=6, choices=KINDS, default="quiz")
    lesson = models.ForeignKey("Lesson", null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="questions",
                               verbose_name="Cours à revoir en cas d'erreur (vide = cours du chapitre)")
    resource = models.ForeignKey("Resource", null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="questions",
                                 verbose_name="Ressource d'origine (exercices du professeur)")
    category = models.CharField("Catégorie", max_length=2, choices=CATEGORIES)
    sub_category = models.ForeignKey("SubCategory", null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="questions",
                                     verbose_name="Sous-catégorie (espace entreprise)")
    theme = models.ForeignKey("Theme", null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="questions",
                              verbose_name="Thématique (optionnelle, au sein de la sous-catégorie)")
    quiz = models.ForeignKey("Quiz", null=True, blank=True, on_delete=models.CASCADE,
                             related_name="own_questions",
                             verbose_name="Quiz partagé (banque dédiée d'un quiz sans espace)")
    difficulty = models.PositiveSmallIntegerField("Difficulté", choices=DIFFICULTIES, default=1)
    text = models.TextField("Question")
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.PositiveSmallIntegerField("Bonne réponse (0-3)")
    explanation = models.TextField("Explication", blank=True, default="")
    active = models.BooleanField("Active", default=True)
    deleted_at = models.DateTimeField("Supprimée le", null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Question"

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.text[:50]}"

    def options(self):
        return [self.option_a, self.option_b, self.option_c, self.option_d]

    def correct_text(self):
        return self.options()[self.correct]


class AdCampaign(models.Model):
    brand = models.CharField("Marque", max_length=60)
    tagline = models.CharField("Slogan", max_length=120)
    pitch = models.TextField("Message")
    emoji = models.CharField("Emoji / logo", max_length=10, default="⭐")
    color = models.CharField("Couleur (hex)", max_length=9, default="#F2790F")
    url = models.URLField("Lien", blank=True, default="")
    is_video = models.BooleanField("Format vidéo (joker)", default=False)
    active = models.BooleanField("Active", default=True)
    impressions = models.PositiveIntegerField(default=0)
    clicks = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Campagne publicitaire"

    def __str__(self):
        return self.brand


class GameSession(models.Model):
    MODES = [("daily", "Défi du jour"), ("training", "Entraînement"), ("space", "Espace entreprise")]
    STATUS = [("playing", "En cours"), ("eliminated", "Éliminé"), ("finished", "Finaliste 🏆")]
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="sessions")
    space = models.ForeignKey("Space", null=True, blank=True, on_delete=models.CASCADE,
                              related_name="sessions")
    quiz = models.ForeignKey("Quiz", null=True, blank=True, on_delete=models.SET_NULL,
                             related_name="sessions",
                             verbose_name="Quiz (vide = pool à plat de l'espace)")
    consent = models.BooleanField("Consentement marketing", default=False)
    mode = models.CharField(max_length=10, choices=MODES)
    status = models.CharField(max_length=10, choices=STATUS, default="playing")
    day = models.DateField(default=timezone.localdate)
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    reached = models.PositiveSmallIntegerField("Question atteinte", default=0)
    total_time_ms = models.PositiveIntegerField(default=0)
    jokers_used = models.PositiveSmallIntegerField(default=0)
    question_ids = models.JSONField(default=list)
    pot_share = models.PositiveIntegerField("Part de cagnotte (F)", default=0)
    paid_out = models.BooleanField("Cagnotte créditée", default=False)
    flagged = models.BooleanField("Suspect (anti-triche)", default=False)

    class Meta:
        verbose_name = "Partie"
        constraints = [
            models.UniqueConstraint(
                fields=["player", "day"], condition=models.Q(mode="daily"),
                name="one_daily_per_player_per_day",
            )
        ]

    def __str__(self):
        return f"{self.player} · {self.day} · Q{self.reached} · {self.get_status_display()}"


class Answer(models.Model):
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.SmallIntegerField()  # -1 = temps écoulé
    time_ms = models.PositiveIntegerField()
    is_correct = models.BooleanField()
    saved_by_joker = models.BooleanField(default=False)


class JokerUse(models.Model):
    TYPES = [("paid", "Payant"), ("ad", "Publicité vidéo")]
    session = models.ForeignKey(GameSession, on_delete=models.CASCADE, related_name="jokers")
    question_index = models.PositiveSmallIntegerField()
    kind = models.CharField(max_length=5, choices=TYPES)
    price = models.PositiveIntegerField(default=0)
    ad = models.ForeignKey(AdCampaign, null=True, blank=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Joker utilisé"


class Withdrawal(models.Model):
    STATUS = [("pending", "À traiter"), ("paid", "Payé"), ("rejected", "Rejeté")]
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="withdrawals")
    amount = models.PositiveIntegerField("Montant (F)")
    momo_number = models.CharField("Numéro mobile money", max_length=20)
    status = models.CharField(max_length=10, choices=STATUS, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    note = models.TextField(blank=True, default="")

    class Meta:
        verbose_name = "Demande de retrait"

    def __str__(self):
        return f"{self.player} · {self.amount} F · {self.get_status_display()}"


REWARD_TYPES = [("monetaire", "Monétaire"), ("nature", "En nature"), ("autre", "Autre")]


def _generate_dashboard_username():
    """Identifiant de connexion au tableau de bord, généré à la création de
    l'espace — volontairement distinct du slug (public, utilisé dans les
    liens `/e/slug/...`) : un identifiant de connexion ne doit pas être
    devinable à partir d'une URL publique. Alphabet sans caractères ambigus
    à l'oral/à l'écrit (pas de 0/O ni de 1/I/l)."""
    alphabet = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    while True:
        candidate = "".join(random.choices(alphabet, k=8))
        if not Space.objects.filter(dashboard_username=candidate).exists():
            return candidate


class Space(models.Model):
    """Espace cloisonné d'une entreprise cliente (multi-tenant)."""
    name = models.CharField("Nom de l'entreprise", max_length=80)
    slug = models.SlugField("Identifiant d'URL", unique=True)
    dashboard_username = models.CharField(
        "Identifiant du tableau de bord", max_length=30, unique=True,
        default=_generate_dashboard_username,
        help_text="Généré automatiquement à la création, distinct du slug d'URL — modifiable si besoin. "
                  "Avec le mot de passe ci-dessous, sert à se connecter sur la page de connexion commune "
                  "à tous les établissements.")
    emoji = models.CharField("Logo (emoji/texte)", max_length=10, default="🏢")
    color_primary = models.CharField("Couleur principale", max_length=9, default="#F2790F")
    color_accent = models.CharField("Couleur secondaire", max_length=9, default="#0B9A5C")
    welcome = models.TextField("Message d'accueil", blank=True, default="")
    reward_type = models.CharField("Type de récompense", max_length=10, choices=REWARD_TYPES,
                                   blank=True, default="")
    reward_text = models.CharField("Récompense annoncée (vide = aucune)", max_length=200,
                                   blank=True, default="")
    access_code = models.CharField("Code d'accès joueurs (vide = lien public)",
                                   max_length=20, blank=True, default="")
    dashboard_code = models.CharField(
        "Mot de passe du tableau de bord", max_length=20,
        help_text="Avec l'identifiant du tableau de bord ci-dessus, sert à se connecter sur la page de "
                  "connexion commune à tous les établissements. Modifiable ensuite par l'établissement "
                  "lui-même depuis son tableau de bord (l'ancien mot de passe lui sera demandé).")
    question_count = models.PositiveSmallIntegerField("Questions par partie", default=10)
    survey_every = models.PositiveSmallIntegerField("Un sondage toutes les N questions (0 = jamais)", default=4)
    elimination = models.BooleanField("Mode survie (élimination)", default=False)
    one_per_day = models.BooleanField("Une participation par jour", default=True)
    playful_fx = models.BooleanField(
        "Effets ludiques (confettis, séries, vibrations)",
        default=True,
        help_text="À désactiver pour un contexte sobre (évaluation notée, quiz de conformité...) : "
                  "le jeu garde son minuteur et son suivi de score, sans les effets festifs.")
    category_label = models.CharField("Libellé d'une catégorie (singulier)", max_length=30,
                                      blank=True, default="Catégorie")
    category_label_plural = models.CharField("Libellé des catégories (pluriel)", max_length=30,
                                              blank=True, default="Catégories")
    subcategory_label = models.CharField("Libellé d'une sous-catégorie (singulier)", max_length=30,
                                         blank=True, default="Sous-catégorie")
    subcategory_label_plural = models.CharField("Libellé des sous-catégories (pluriel)", max_length=30,
                                                 blank=True, default="Sous-catégories")
    theme_label = models.CharField("Libellé d'une thématique (singulier)", max_length=30,
                                   blank=True, default="Thématique")
    theme_label_plural = models.CharField("Libellé des thématiques (pluriel)", max_length=30,
                                          blank=True, default="Thématiques")
    logo_url = models.URLField("Logo (URL image, vide = emoji)", blank=True, default="")
    cover_url = models.URLField("Image de couverture (URL, vide = dégradé de couleur)", blank=True, default="")
    consent_required = models.BooleanField(
        "Consentement marketing requis",
        default=True,
        help_text="À désactiver pour un usage sans finalité marketing (ex. suivi pédagogique en école) : "
                  "la case à cocher n'est plus proposée aux participants et personne n'est anonymisé dans les exports.")
    # --- Accès et abonnements individuels (accompagnement scolaire) ---
    members_only = models.BooleanField(
        "Réservé aux membres de l'établissement", default=False,
        help_text="Seuls les joueurs reliés à une fiche membre (élève importé par l'établissement) "
                  "peuvent jouer les quiz de l'espace. À activer pour une école.")
    subscription_required = models.BooleanField(
        "Abonnement individuel requis", default=False,
        help_text="Chaque élève doit avoir un abonnement actif (mensuel, trimestriel ou annuel) "
                  "pour lancer un quiz, après la période d'essai.")
    free_until = models.DateField(
        "Accès gratuit jusqu'au (inclus)", null=True, blank=True,
        help_text="Période d'essai ou pilote : tous les membres jouent sans abonnement jusqu'à cette date.")
    price_monthly = models.PositiveIntegerField("Prix mensuel (F CFA)", default=2000)
    price_quarterly = models.PositiveIntegerField("Prix trimestriel (F CFA, 0 = non proposé)", default=0)
    price_yearly = models.PositiveIntegerField("Prix annuel (F CFA, 0 = non proposé)", default=15000)
    school_share_per_month = models.PositiveIntegerField(
        "Part de l'établissement par élève abonné et par mois (F CFA)", default=500)
    live_teacher_share_pct = models.PositiveSmallIntegerField(
        "Part du professeur sur les séances payantes (%)", default=60)
    live_school_share_pct = models.PositiveSmallIntegerField(
        "Part de l'établissement sur les séances payantes (%)", default=10)
    payment_number = models.CharField(
        "Numéro de paiement mobile money", max_length=30, blank=True, default="",
        help_text="Numéro Wave / Orange Money / MTN / Moov sur lequel les familles paient.")
    payment_instructions = models.TextField(
        "Consignes de paiement", blank=True,
        default="Indique le matricule de l'élève en motif du paiement, puis saisis ci-dessous "
                "la référence de la transaction reçue par SMS.")
    active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Espace entreprise"

    def __str__(self):
        return self.name


class License(models.Model):
    """Licence d'un espace pour une période donnée (l'année scolaire n'est qu'un
    cas particulier : ce concept vaut pour tout type d'établissement)."""
    BILLING_MODES = [("per_seat", "Par siège"), ("forfait", "Forfait (illimité)")]
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="licenses")
    period_label = models.CharField("Période (ex. 2026-2027)", max_length=30)
    billing_mode = models.CharField("Mode de facturation", max_length=10,
                                    choices=BILLING_MODES, default="per_seat")
    seat_count = models.PositiveIntegerField("Sièges (si facturation par siège)", null=True, blank=True)
    price = models.CharField("Tarif convenu (informatif)", max_length=60, blank=True, default="")
    reward_type = models.CharField("Type de récompense par défaut", max_length=10, choices=REWARD_TYPES,
                                   blank=True, default="")
    reward_text = models.CharField("Récompense par défaut (vide = aucune)", max_length=200,
                                   blank=True, default="")
    jokers_allowed = models.BooleanField(
        "Joker « pub vidéo » activable sur les quiz",
        default=False,
        help_text="Autorise l'établissement à activer un joker (seconde chance via pub vidéo, "
                  "pas d'achat) sur les quiz de son choix. Le joker payant reste réservé au jeu public.")
    start_date = models.DateField("Début de période")
    end_date = models.DateField("Fin de période")
    active = models.BooleanField("Licence active", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Licence"

    def __str__(self):
        return f"{self.space} · {self.period_label}"

    def seats_used(self):
        return self.memberships.count()


class Membership(models.Model):
    """Personne identifiée par l'établissement (élève, employé...), matchée par téléphone.
    Une ligne par période/licence : permet de conserver l'historique d'une année sur l'autre."""
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="members")
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.SET_NULL,
                               related_name="memberships")
    license = models.ForeignKey(License, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="memberships")
    category = models.ForeignKey("Category", null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="members")
    sub_category = models.ForeignKey("SubCategory", null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="members")
    full_name = models.CharField("Nom complet", max_length=120)
    phone = models.CharField("Téléphone (base établissement)", max_length=20, blank=True, default="")
    external_ref = models.CharField("Référence externe (matricule...)", max_length=60, blank=True, default="")
    parent_phone = models.CharField("Téléphone du parent", max_length=20, blank=True, default="",
                                    help_text="Reçoit le bilan mensuel. Peut être partagé par des frères et sœurs.")
    pin_hash = models.CharField("Code PIN (haché)", max_length=128, blank=True, default="")
    pin_failed = models.PositiveSmallIntegerField("Échecs PIN consécutifs", default=0)
    pin_locked_until = models.DateTimeField("PIN verrouillé jusqu'au", null=True, blank=True)
    pin_failures_24h = models.PositiveSmallIntegerField("Échecs PIN sur 24 h", default=0)
    pin_last_failed_at = models.DateTimeField("Dernier échec PIN", null=True, blank=True)
    matched_at = models.DateTimeField("Apparié le", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField("Supprimé le", null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Membre de l'espace"
        constraints = [
            # Avec matricule : un élève = un matricule (des frères et sœurs peuvent
            # partager le téléphone d'un parent). Sans matricule : un par téléphone.
            models.UniqueConstraint(fields=["space", "license", "external_ref"],
                                    condition=models.Q(deleted_at__isnull=True) & ~models.Q(external_ref=""),
                                    name="unique_active_membership_ref"),
            models.UniqueConstraint(fields=["space", "phone", "license"],
                                    condition=models.Q(deleted_at__isnull=True, external_ref="") & ~models.Q(phone=""),
                                    name="unique_active_membership"),
        ]

    def __str__(self):
        return f"{self.space} · {self.full_name}"


class OTPCode(models.Model):
    """Code de connexion à usage unique envoyé par SMS (stub dev : loggué/affiché)."""
    phone = models.CharField("Téléphone", max_length=20)
    code = models.CharField("Code", max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    consumed = models.BooleanField(default=False)
    attempts = models.PositiveSmallIntegerField(default=0)

    class Meta:
        verbose_name = "Code de connexion (OTP)"

    def __str__(self):
        return f"{self.phone} · {self.code}"


class Category(models.Model):
    """Catégorie de premier niveau d'un espace (ex : niveau scolaire, famille de produits)."""
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField("Nom", max_length=80)
    slug = models.SlugField("Identifiant d'URL", max_length=60)
    order = models.PositiveSmallIntegerField("Ordre", default=0)
    deleted_at = models.DateTimeField("Supprimée le", null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["space", "slug"], condition=models.Q(deleted_at__isnull=True),
                                    name="unique_active_category_slug"),
        ]

    def __str__(self):
        return f"{self.space} · {self.name}"


class SubCategory(models.Model):
    """Sous-catégorie (ex : matière, sous-famille de produits)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField("Nom", max_length=80)
    slug = models.SlugField("Identifiant d'URL", max_length=60)
    order = models.PositiveSmallIntegerField("Ordre", default=0)
    deleted_at = models.DateTimeField("Supprimée le", null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["category", "slug"], condition=models.Q(deleted_at__isnull=True),
                                    name="unique_active_subcategory_slug"),
        ]

    def __str__(self):
        return f"{self.category.name} · {self.name}"


class Theme(models.Model):
    """Thématique au sein d'une sous-catégorie (ex : point précis d'une matière)."""
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="themes")
    name = models.CharField("Nom", max_length=80)
    slug = models.SlugField("Identifiant d'URL", max_length=60)
    order = models.PositiveSmallIntegerField("Ordre", default=0)
    taught_on = models.DateField("Cours prévu le", null=True, blank=True,
                                 help_text="Sert au suivi du rythme : les ressources du chapitre sont attendues "
                                           "au plus tard 7 jours après.")
    deleted_at = models.DateTimeField("Supprimée le", null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Thématique"
        verbose_name_plural = "Thématiques"
        ordering = ["order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["sub_category", "slug"], condition=models.Q(deleted_at__isnull=True),
                                    name="unique_active_theme_slug"),
        ]

    def __str__(self):
        return f"{self.sub_category} · {self.name}"


class Quiz(models.Model):
    """Quiz partageable par lien direct, rattaché à une catégorie/sous-catégorie
    d'un espace précis — ou, si space est vide, quiz partagé rattaché par nom
    de niveau/matière (shared_level_name/shared_subject_name) et automatiquement
    disponible dans tout espace dont une Catégorie/Sous-catégorie porte ce nom."""
    space = models.ForeignKey(Space, null=True, blank=True, on_delete=models.CASCADE,
                              related_name="quizzes",
                              verbose_name="Espace (vide = quiz partagé par niveau/matière)")
    shared_level_name = models.CharField(
        "Niveau (si quiz partagé, ex. 6ème)", max_length=80, blank=True, default="",
        help_text="Doit correspondre exactement (insensible à la casse) au nom d'une Catégorie "
                  "d'un espace pour que le quiz y apparaisse automatiquement.")
    shared_subject_name = models.CharField(
        "Matière (optionnel, si quiz partagé, ex. Français)", max_length=80, blank=True, default="",
        help_text="Doit correspondre exactement au nom d'une Sous-catégorie de la catégorie ci-dessus. "
                  "Vide = le quiz cible le niveau entier, sans matière précise.")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="quizzes")
    sub_category = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="quizzes")
    theme = models.ForeignKey(Theme, null=True, blank=True, on_delete=models.SET_NULL,
                              related_name="quizzes",
                              verbose_name="Thématique (optionnelle, au sein de la sous-catégorie)")
    name = models.CharField("Nom du quiz", max_length=100)
    slug = models.SlugField("Identifiant d'URL", max_length=60)
    question_count = models.PositiveSmallIntegerField("Questions par partie", default=10)
    survey_every = models.PositiveSmallIntegerField("Un sondage toutes les N questions (0 = jamais)", default=4)
    elimination = models.BooleanField("Mode survie (élimination)", default=False)
    REPLAY_POLICIES = [
        ("daily", "Une fois par jour"),
        ("once", "Une seule fois (jamais rejouable)"),
        ("unlimited", "Illimité (rejouable à tout moment)"),
    ]
    replay_policy = models.CharField("Rejouabilité", max_length=10, choices=REPLAY_POLICIES, default="daily")
    show_corrections = models.BooleanField(
        "Corrections visibles après coup", default=False,
        help_text="Si activé, le joueur voit la bonne réponse et l'explication de chaque question "
                  "dans le détail de sa partie sur son compte, une fois celle-ci terminée.")
    joker_enabled = models.BooleanField(
        "Joker « pub vidéo » activé sur ce quiz", default=False,
        help_text="Nécessite que la licence de l'espace l'autorise (License.jokers_allowed).")
    reward_type = models.CharField("Type de récompense (vide = hérite de l'espace/licence)", max_length=10,
                                   choices=REWARD_TYPES, blank=True, default="")
    reward_text = models.CharField("Récompense (vide = hérite de l'espace/licence)", max_length=200,
                                   blank=True, default="")
    active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField("Supprimé le", null=True, blank=True, default=None)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"
        ordering = ["category__order", "sub_category__order", "name"]
        constraints = [
            models.UniqueConstraint(fields=["space", "slug"], condition=models.Q(deleted_at__isnull=True),
                                    name="unique_active_quiz_slug"),
            models.UniqueConstraint(fields=["slug"],
                                    condition=models.Q(space__isnull=True, deleted_at__isnull=True),
                                    name="unique_global_quiz_slug"),
        ]

    def __str__(self):
        if self.space_id:
            return f"{self.space} · {self.name}"
        label = " · ".join(filter(None, [self.shared_level_name, self.shared_subject_name]))
        return f"[Partagé{' · ' + label if label else ''}] {self.name}"

    def level_name(self):
        """Nom du niveau, que le quiz soit propre à un espace (Category) ou
        partagé (shared_level_name en texte libre)."""
        return self.category.name if self.category_id else self.shared_level_name

    def subject_name(self):
        """Nom de la matière, même logique que level_name()."""
        return self.sub_category.name if self.sub_category_id else self.shared_subject_name


class AuditLog(models.Model):
    """Journal d'activité du tableau de bord établissement : trace chaque
    création/modification/suppression pour qu'on puisse toujours remonter à ce
    qui a été fait, quand, et pourquoi un élément a disparu de l'affichage
    (suppression douce — voir SoftDeleteManager, rien n'est réellement effacé).
    Une entrée « delete »/« bulk_delete » peut être annulée (restauration) tant
    que l'objet visé existe toujours en base (ce qui est garanti par le
    principe même de la suppression douce)."""
    ACTIONS = [
        ("create", "Création"), ("update", "Modification"),
        ("toggle", "Activation/désactivation"),
        ("delete", "Suppression"), ("bulk_delete", "Suppression groupée"),
        ("restore", "Restauration"),
    ]
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="audit_logs")
    actor = models.CharField(
        "Auteur", max_length=60, blank=True, default="",
        help_text="Identifiant du tableau de bord ayant effectué l'action (pas de comptes "
                  "individuels par employé à ce stade — un seul identifiant par établissement).")
    action = models.CharField("Action", max_length=15, choices=ACTIONS)
    model_name = models.CharField("Type d'objet", max_length=40)
    object_id = models.PositiveIntegerField("Identifiant de l'objet", null=True, blank=True)
    object_repr = models.CharField("Aperçu", max_length=200, blank=True, default="")
    details = models.CharField("Détails", max_length=300, blank=True, default="")
    created_at = models.DateTimeField("Date", auto_now_add=True)

    class Meta:
        verbose_name = "Entrée du journal d'activité"
        verbose_name_plural = "Journal d'activité"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.created_at:%d/%m/%Y %H:%M} · {self.get_action_display()} · {self.model_name} · {self.object_repr}"


class Subscription(models.Model):
    """Abonnement individuel d'un élève (Membership) pour une période donnée.
    Le paiement mobile money est déclaré par la famille (référence de
    transaction), puis validé à la main dans le tableau de bord : tant qu'il
    n'est pas validé, l'abonnement est « en attente » et ne donne pas accès."""
    PLANS = [("monthly", "Mensuel"), ("quarterly", "Trimestriel"), ("yearly", "Annuel")]
    PLAN_MONTHS = {"monthly": 1, "quarterly": 3, "yearly": 12}
    STATUS = [("pending", "En attente de validation"), ("active", "Validé"), ("rejected", "Refusé")]

    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.CharField("Formule", max_length=10, choices=PLANS)
    amount = models.PositiveIntegerField("Montant payé (F CFA)")
    payer_phone = models.CharField("Téléphone du payeur", max_length=20, blank=True, default="")
    payment_ref = models.CharField("Référence de la transaction", max_length=60)
    status = models.CharField("Statut", max_length=10, choices=STATUS, default="pending")
    start_date = models.DateField("Début", null=True, blank=True)
    end_date = models.DateField("Fin (incluse)", null=True, blank=True)
    validated_at = models.DateTimeField("Validé le", null=True, blank=True)
    note = models.CharField("Note interne", max_length=200, blank=True, default="")
    expiry_notified_at = models.DateTimeField("Rappel d'échéance envoyé le", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Abonnement élève"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["membership", "payment_ref"], name="unique_payment_ref_per_member"),
        ]

    def __str__(self):
        return f"{self.membership} · {self.get_plan_display()} · {self.get_status_display()}"

    def is_current(self, day=None):
        from django.utils import timezone as _tz
        day = day or _tz.localdate()
        return (self.status == "active" and self.start_date and self.end_date
                and self.start_date <= day <= self.end_date)


class Teacher(models.Model):
    """Compte individuel d'un membre de l'équipe pédagogique (direction ou
    professeur), distinct de l'identifiant unique du tableau de bord."""
    ROLES = [("direction", "Direction / administration"), ("teacher", "Professeur")]
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="teachers")
    full_name = models.CharField("Nom complet", max_length=120)
    username = models.CharField("Identifiant de connexion", max_length=40, unique=True)
    password_hash = models.CharField("Mot de passe (haché)", max_length=128, blank=True, default="")
    role = models.CharField("Rôle", max_length=10, choices=ROLES, default="teacher")
    sub_categories = models.ManyToManyField(SubCategory, blank=True, related_name="teachers",
                                            verbose_name="Matières suivies")
    active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Enseignant"

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    def set_password(self, raw):
        from django.contrib.auth.hashers import make_password
        self.password_hash = make_password(raw)

    def check_password(self, raw):
        from django.contrib.auth.hashers import check_password
        return bool(self.password_hash) and check_password(raw, self.password_hash)


class Resource(models.Model):
    """Exercices corrigés déposés par un professeur pour un chapitre. Le
    fichier est stocké en base (pas de disque persistant sur l'hébergement)."""
    STATUS = [("deposited", "Déposée"), ("converted", "Transformée en quiz"),
              ("validated", "Validée par le professeur")]
    MAX_BYTES = 5 * 1024 * 1024
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="resources")
    teacher = models.ForeignKey(Teacher, null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="resources")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="resources")
    theme = models.ForeignKey(Theme, null=True, blank=True, on_delete=models.SET_NULL, related_name="resources")
    title = models.CharField("Titre", max_length=150)
    note = models.TextField("Commentaire", blank=True, default="")
    file_name = models.CharField("Nom du fichier", max_length=200)
    content_type = models.CharField(max_length=100, default="application/octet-stream")
    data = models.BinaryField("Contenu du fichier")
    status = models.CharField("Statut", max_length=10, choices=STATUS, default="deposited")
    created_at = models.DateTimeField("Déposée le", auto_now_add=True)
    converted_at = models.DateTimeField("Transformée le", null=True, blank=True)
    validated_at = models.DateTimeField("Validée le", null=True, blank=True)

    class Meta:
        verbose_name = "Ressource pédagogique"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.sub_category} · {self.title}"


def youtube_id(url):
    """Identifiant d'une vidéo YouTube depuis ses formes d'URL courantes
    (watch?v=, youtu.be/, /embed/, /live/, /shorts/), ou "" si non reconnu."""
    import re
    m = re.search(r"(?:v=|youtu\.be/|/embed/|/live/|/shorts/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else ""


class Lesson(models.Model):
    """Cours (fiche PDF et/ou vidéo YouTube) rattaché à un chapitre.
    space vide = cours commun MQ, rattaché par niveau/matière/chapitre comme
    les quiz partagés ; sinon cours propre à l'établissement."""
    space = models.ForeignKey(Space, null=True, blank=True, on_delete=models.CASCADE, related_name="lessons",
                              verbose_name="Espace (vide = cours commun à toutes les écoles)")
    shared_level_name = models.CharField("Niveau (cours commun)", max_length=80, blank=True, default="")
    shared_subject_name = models.CharField("Matière (cours commun)", max_length=80, blank=True, default="")
    shared_theme_name = models.CharField("Chapitre (cours commun)", max_length=100, blank=True, default="",
                                         help_text="Même nom que le quiz partagé du chapitre : relie les corrections au cours.")
    sub_category = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.CASCADE,
                                     related_name="lessons")
    theme = models.ForeignKey(Theme, null=True, blank=True, on_delete=models.SET_NULL, related_name="lessons")
    teacher = models.ForeignKey("Teacher", null=True, blank=True, on_delete=models.SET_NULL, related_name="lessons")
    title = models.CharField("Titre", max_length=150)
    summary = models.TextField("Résumé", blank=True, default="")
    youtube_url = models.URLField("Lien de la vidéo YouTube", blank=True, default="",
                                  help_text="Vidéo publique ou « non répertoriée » ; lue directement dans MaxQuiz.")
    pdf_name = models.CharField("Nom du PDF", max_length=200, blank=True, default="")
    pdf_data = models.BinaryField("Fiche PDF", null=True, blank=True)
    free_preview = models.BooleanField("Accessible sans abonnement", default=False)
    order = models.PositiveSmallIntegerField("Ordre", default=0)
    active = models.BooleanField("Publié", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    MAX_PDF_BYTES = 5 * 1024 * 1024

    class Meta:
        verbose_name = "Cours"
        verbose_name_plural = "Cours"
        ordering = ["order", "title"]

    def __str__(self):
        return self.title

    @property
    def video_id(self):
        return youtube_id(self.youtube_url)

    @property
    def has_pdf(self):
        return bool(self.pdf_name)


class LiveSession(models.Model):
    """Séance de cours en direct (payante ou non), avec différé."""
    PROVIDERS = [("youtube", "YouTube Live intégré (diffusion à toute une classe)"),
                 ("jitsi", "Visio Jitsi intégrée (petit groupe interactif)"),
                 ("external", "Lien externe (Google Meet, Zoom…)")]
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="live_sessions")
    teacher = models.ForeignKey("Teacher", null=True, blank=True, on_delete=models.SET_NULL,
                                related_name="live_sessions")
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, related_name="live_sessions")
    theme = models.ForeignKey(Theme, null=True, blank=True, on_delete=models.SET_NULL, related_name="live_sessions")
    title = models.CharField("Titre", max_length=150)
    description = models.TextField("Description", blank=True, default="")
    starts_at = models.DateTimeField("Début")
    duration_min = models.PositiveSmallIntegerField("Durée (minutes)", default=60)
    price_live = models.PositiveIntegerField("Prix du direct (F CFA, 0 = gratuit)", default=500)
    price_replay = models.PositiveIntegerField("Prix du différé seul (F CFA, 0 = gratuit)", default=300)
    seats = models.PositiveIntegerField("Places en direct (0 = illimité)", default=0)
    provider = models.CharField("Diffusion", max_length=10, choices=PROVIDERS, default="youtube")
    stream_url = models.URLField("Lien du direct (YouTube Live ou Meet/Zoom)", blank=True, default="")
    jitsi_room = models.CharField("Salle Jitsi", max_length=80, blank=True, default="")
    replay_url = models.URLField("Lien du différé (YouTube)", blank=True, default="",
                                 help_text="Pour YouTube Live, vide = le lien du direct sert aussi de différé.")
    cancelled = models.BooleanField("Annulée", default=False)
    reminder_sent_at = models.DateTimeField("Rappel envoyé le", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Séance en direct"
        verbose_name_plural = "Séances en direct"
        ordering = ["starts_at"]

    def __str__(self):
        return f"{self.title} · {self.starts_at:%d/%m %H:%M}"

    def save(self, *args, **kwargs):
        if self.provider == "jitsi" and not self.jitsi_room:
            import secrets
            from django.utils.text import slugify
            self.jitsi_room = f"maxquiz-{slugify(self.space.slug)[:20]}-{secrets.token_hex(6)}"
        super().save(*args, **kwargs)

    @property
    def ends_at(self):
        from datetime import timedelta
        return self.starts_at + timedelta(minutes=self.duration_min)

    @property
    def live_video_id(self):
        return youtube_id(self.stream_url) if self.provider == "youtube" else ""

    @property
    def replay_video_id(self):
        return youtube_id(self.replay_url) or self.live_video_id


class SessionBooking(models.Model):
    """Inscription payante d'un élève à une séance (direct, qui inclut le
    différé, ou différé seul). Paiement mobile money validé à la main."""
    KINDS = [("live", "Direct + différé"), ("replay", "Différé seul")]
    STATUS = [("pending", "En attente de validation"), ("active", "Validée"), ("rejected", "Refusée")]
    session = models.ForeignKey(LiveSession, on_delete=models.CASCADE, related_name="bookings")
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE, related_name="bookings")
    kind = models.CharField("Formule", max_length=6, choices=KINDS)
    amount = models.PositiveIntegerField("Montant (F CFA)")
    payment_ref = models.CharField("Référence de la transaction", max_length=60, blank=True, default="")
    status = models.CharField("Statut", max_length=10, choices=STATUS, default="pending")
    validated_at = models.DateTimeField("Validée le", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Inscription à une séance"
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["session", "membership", "kind"],
                                               name="unique_booking_per_kind")]

    def __str__(self):
        return f"{self.membership} · {self.session} · {self.get_kind_display()}"


class PushDevice(models.Model):
    """Appareil qui reçoit les notifications push : navigateur ou APK de type
    TWA (Web Push), ou APK WebView/natif (jeton Firebase Cloud Messaging)."""
    KINDS = [("webpush", "Web Push (navigateur, APK TWA)"), ("fcm", "Firebase (APK)")]
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE, related_name="devices")
    teacher = models.ForeignKey("Teacher", null=True, blank=True, on_delete=models.CASCADE, related_name="devices")
    kind = models.CharField(max_length=8, choices=KINDS)
    endpoint = models.TextField("Adresse Web Push ou jeton FCM", unique=True)
    p256dh = models.CharField(max_length=200, blank=True, default="")
    auth = models.CharField(max_length=100, blank=True, default="")
    user_agent = models.CharField(max_length=200, blank=True, default="")
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_success_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Appareil (notifications)"

    def __str__(self):
        return f"{self.player or self.teacher} · {self.kind}"


class Notification(models.Model):
    """Notification conservée dans l'application (centre de notifications) :
    toujours créée, même si le push est refusé ou hors ligne."""
    player = models.ForeignKey(Player, null=True, blank=True, on_delete=models.CASCADE, related_name="notifications")
    teacher = models.ForeignKey("Teacher", null=True, blank=True, on_delete=models.CASCADE, related_name="notifications")
    kind = models.CharField("Type", max_length=30, default="info")
    title = models.CharField("Titre", max_length=120)
    body = models.CharField("Message", max_length=300, blank=True, default="")
    url = models.CharField("Lien", max_length=300, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    pushed = models.PositiveSmallIntegerField("Appareils atteints", default=0)

    class Meta:
        verbose_name = "Notification"
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["player", "read_at"]), models.Index(fields=["teacher", "read_at"])]

    def __str__(self):
        return self.title
