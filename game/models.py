from django.db import models
from django.utils import timezone


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
    category = models.CharField("Catégorie", max_length=2, choices=CATEGORIES)
    sub_category = models.ForeignKey("SubCategory", null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="questions",
                                     verbose_name="Sous-catégorie (espace entreprise)")
    difficulty = models.PositiveSmallIntegerField("Difficulté", choices=DIFFICULTIES, default=1)
    text = models.TextField("Question")
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200)
    option_d = models.CharField(max_length=200)
    correct = models.PositiveSmallIntegerField("Bonne réponse (0-3)")
    explanation = models.TextField("Explication", blank=True, default="")
    active = models.BooleanField("Active", default=True)

    class Meta:
        verbose_name = "Question"

    def __str__(self):
        return f"[{self.get_difficulty_display()}] {self.text[:50]}"

    def options(self):
        return [self.option_a, self.option_b, self.option_c, self.option_d]


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


class Space(models.Model):
    """Espace cloisonné d'une entreprise cliente (multi-tenant)."""
    name = models.CharField("Nom de l'entreprise", max_length=80)
    slug = models.SlugField("Identifiant d'URL", unique=True)
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
    dashboard_code = models.CharField("Code d'accès au tableau de bord client", max_length=20)
    question_count = models.PositiveSmallIntegerField("Questions par partie", default=10)
    survey_every = models.PositiveSmallIntegerField("Un sondage toutes les N questions (0 = jamais)", default=4)
    elimination = models.BooleanField("Mode survie (élimination)", default=False)
    one_per_day = models.BooleanField("Une participation par jour", default=True)
    category_label = models.CharField("Libellé d'une catégorie (singulier)", max_length=30,
                                      blank=True, default="Catégorie")
    category_label_plural = models.CharField("Libellé des catégories (pluriel)", max_length=30,
                                              blank=True, default="Catégories")
    subcategory_label = models.CharField("Libellé d'une sous-catégorie (singulier)", max_length=30,
                                         blank=True, default="Sous-catégorie")
    subcategory_label_plural = models.CharField("Libellé des sous-catégories (pluriel)", max_length=30,
                                                 blank=True, default="Sous-catégories")
    logo_url = models.URLField("Logo (URL image, vide = emoji)", blank=True, default="")
    cover_url = models.URLField("Image de couverture (URL, vide = dégradé de couleur)", blank=True, default="")
    consent_required = models.BooleanField(
        "Consentement marketing requis",
        default=True,
        help_text="À désactiver pour un usage sans finalité marketing (ex. suivi pédagogique en école) : "
                  "la case à cocher n'est plus proposée aux participants et personne n'est anonymisé dans les exports.")
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
    phone = models.CharField("Téléphone (base établissement)", max_length=20)
    external_ref = models.CharField("Référence externe (matricule...)", max_length=60, blank=True, default="")
    matched_at = models.DateTimeField("Apparié le", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Membre de l'espace"
        unique_together = [("space", "phone", "license")]

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

    class Meta:
        verbose_name = "Catégorie"
        verbose_name_plural = "Catégories"
        unique_together = [("space", "slug")]
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.space} · {self.name}"


class SubCategory(models.Model):
    """Sous-catégorie (ex : matière, sous-famille de produits)."""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="subcategories")
    name = models.CharField("Nom", max_length=80)
    slug = models.SlugField("Identifiant d'URL", max_length=60)
    order = models.PositiveSmallIntegerField("Ordre", default=0)

    class Meta:
        verbose_name = "Sous-catégorie"
        verbose_name_plural = "Sous-catégories"
        unique_together = [("category", "slug")]
        ordering = ["order", "name"]

    def __str__(self):
        return f"{self.category.name} · {self.name}"


class Quiz(models.Model):
    """Quiz partageable par lien direct, rattaché à une catégorie/sous-catégorie."""
    space = models.ForeignKey(Space, on_delete=models.CASCADE, related_name="quizzes")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL,
                                 related_name="quizzes")
    sub_category = models.ForeignKey(SubCategory, null=True, blank=True, on_delete=models.SET_NULL,
                                     related_name="quizzes")
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
    joker_enabled = models.BooleanField(
        "Joker « pub vidéo » activé sur ce quiz", default=False,
        help_text="Nécessite que la licence de l'espace l'autorise (License.jokers_allowed).")
    reward_type = models.CharField("Type de récompense (vide = hérite de l'espace/licence)", max_length=10,
                                   choices=REWARD_TYPES, blank=True, default="")
    reward_text = models.CharField("Récompense (vide = hérite de l'espace/licence)", max_length=200,
                                   blank=True, default="")
    active = models.BooleanField("Actif", default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quiz"
        unique_together = [("space", "slug")]
        ordering = ["category__order", "sub_category__order", "name"]

    def __str__(self):
        return f"{self.space} · {self.name}"
