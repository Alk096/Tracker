from django.db import models
from django.contrib.auth.models import User
from io import BytesIO
from django.core.files import File
import qrcode

from django.urls import reverse
from django.conf import settings
from multiselectfield import MultiSelectField

class Utilisateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    mes_profils = [('AD', 'AD'),
                   ('CDM', 'CDM'),
                   ('CDN', 'CDN'),
                   ('CDV', 'CDV'),
                   ('CG', 'CG'),
                   ('DG', 'DG'),
                   ('Employé', 'Employé'),
                   ('VIP', 'VIP'),
                   ]
    mes_directions = [
        ('Administration - Comptabilite - Finance', 'Administration - Comptabilite - Finance'),
        ('Direction Generale', 'Direction Generale'),
        ('Marketing et Developpement', 'Marketing et Developpement'),
        ('Transformation Numerique', 'Transformation Numerique'),
        ('Visibilite - Infrastructure - Production', 'Visibilite - Infrastructure - Production'),
        ('Ventes et Clientele', 'Ventes et Clientele'),

    ]
    poste = models.CharField(max_length=30, choices=mes_profils, default='Employé')
    direction = models.CharField(max_length=50, choices=mes_directions, default='Employé')
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} - {self.poste} - {self.direction}"

# Modele Client

class Client(models.Model):
    raison = models.CharField(max_length=100, null=False, blank=False)
    nif = models.CharField(max_length=100, null=False, blank=False)
    adresse = models.CharField(max_length=100, null=False, blank=False)
    mail = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return f"{self.raison}"

# Model Projet

class Projet(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    intitule = models.CharField(max_length=100, null=False, blank=False)
    direction = models.CharField(
        max_length=100,
        choices=Utilisateur.mes_directions,
        default='Direction Generale'
    )
    date_debut = models.DateField()
    statut = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='QR_codes/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = self.generate_qr_code()
        super().save(*args, **kwargs)

    def generate_qr_code(self):
        data = f"{self.client.raison}-{self.intitule}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"{self.client.raison}_projet_{self.intitule}_qr.png"
        return File(buffer, name=file_name)

    @property
    def progression(self):
        total = self.prestation_set.count()
        if total == 0:
            return 0
        terminees = self.prestation_set.filter(statut=True).count()
        return round((terminees / total) * 100)    

    def __str__(self):
        return f"Projet : {self.intitule} - Client : {self.client.raison} - {self.statut}"

# Modele Prestation

class Prestation(models.Model):

    mes_directions = [
        ('Administration - Comptabilite - Finance', 'Administration - Comptabilite - Finance'),
        ('Marketing et Developpement', 'Marketing et Developpement'),
        ('Transformation Numerique', 'Transformation Numerique'),
        ('Visibilite - Infrastructure - Production', 'Visibilite - Infrastructure - Production'),
        ('Ventes et Clientele', 'Ventes et Clientele'),

    ]

    projet = models.ForeignKey(Projet, on_delete=models.CASCADE)
    designation = models.CharField(max_length=100, null=False, blank=False)
    charge = models.CharField(max_length=50, choices=mes_directions, default='Ventes et Clientele')
    description = models.TextField(null=True, blank=True)
    statut = models.BooleanField(default=False)
    date_fin = models.DateField()

    def __str__(self):
        return f"Projet : {self.projet.intitule} ({self.projet.client.raison}) - Prestation : {self.designation} - Sous : {self.charge} - Statut : {self.statut} - {self.date_fin} "

# Modele Note

class Note(models.Model):
    prestation = models.ForeignKey(Prestation, on_delete=models.CASCADE)
    auteur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    contenu = models.TextField(null=False, blank=False)

# Modele Papi

class Papi(models.Model):
    client = models.OneToOneField(Client, on_delete=models.CASCADE, related_name="papi")
    lien = models.URLField(blank=True, null=True)  # URL vers le questionnaire (Google Forms ou interne)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Questionnaire pour {self.client.raison}"

    def generate_qr_code(self):
        questionnaire_url = f"{settings.SITE_URL}{reverse('papi', args=[self.client.id])}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(questionnaire_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"Papi_{self.client.raison}_qr.png"
        return File(buffer, name=file_name)


# Modele Questionnaire

class Questionnaire(models.Model):
    projet = models.OneToOneField(Projet, on_delete=models.CASCADE, related_name="questionnaire")
    lien = models.URLField(blank=True, null=True)  # URL vers le questionnaire (Google Forms ou interne)
    date_creation = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Questionnaire pour {self.projet.intitule}"

    def generate_qr_code(self):
        questionnaire_url = f"{settings.SITE_URL}{reverse('Questionnaire', args=[self.projet.id])}"
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(questionnaire_url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f"{self.projet.client.raison}_projet_{self.projet.intitule}_qr.png"
        return File(buffer, name=file_name)

# Modele Reponse Questionnaire

class ReponseQuestionnaire(models.Model):
    PRESTATIONS_CHOICES = (
        ('location', 'Location panneaux'),
        ('confection', 'Confection support de communication'),
        ('evenementiel', 'Événementiel'),
        ('etude', 'Étude de marché'),
        ('impression', 'Impression/production de gadgets'),
        ('media', 'Travaux médias'),
        ('autres', 'Autres (précisez)'),
    )

    ELEMENTS_CHOICES = (
        ('Qualité promise', 'Qualité promise'),
        ('Délais de livraison promis ', 'Délais de livraison promis '),
        ('Respect des engagements de l’agence', 'Respect des engagements de l’agence'),
    )


    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="reponses")
    date_reponse = models.DateTimeField(auto_now_add=True)

    nom = models.CharField(max_length=100, null=True, blank=True)
    raison = models.CharField(max_length=100, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)

    r1 = models.BooleanField(default=True)  # Réponse à Q1
    r2 = MultiSelectField(choices=PRESTATIONS_CHOICES, max_length=100, blank=True)  # Réponse Q2
    r2_autre = models.CharField(max_length=255, blank=True, null=True)

    r3 = models.BooleanField(default=True)
    r3_non = models.CharField(max_length=255, blank=True, null=True)

    r4 = MultiSelectField(choices=ELEMENTS_CHOICES, max_length=100, blank=True)

    r5 = models.BooleanField(default=True)
    r5_raison = models.CharField(max_length=255, blank=True, null=True)

    r6 = models.BooleanField(default=True)
    r6_raison = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Réponse au questionnaire {self.questionnaire.id} ({self.date_reponse.date()})"

# Modele Reponse Papi

class ReponsePapi(models.Model):
    PRESTATIONS_CHOICES = (
        ('location', 'Location panneaux'),
        ('confection', 'Confection support de communication'),
        ('evenementiel', 'Événementiel'),
        ('etude', 'Étude de marché'),
        ('impression', 'Impression/production de gadgets'),
        ('media', 'Travaux médias'),
        ('autres', 'Autres (précisez)'),
    )

    ELEMENTS_CHOICES = (
        ('Qualité promise', 'Qualité promise'),
        ('Délais de livraison promis ', 'Délais de livraison promis '),
        ('Respect des engagements de l’agence', 'Respect des engagements de l’agence'),
    )


    questionnaire = models.ForeignKey(Papi, on_delete=models.CASCADE, related_name="reponsespapi")
    date_reponse = models.DateTimeField(auto_now_add=True)

    nom = models.CharField(max_length=100, null=True, blank=True)
    raison = models.CharField(max_length=100, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)
    telephone = models.CharField(max_length=100, null=True, blank=True)

    r1 = models.BooleanField(default=True)  # Réponse à Q1
    r2 = MultiSelectField(choices=PRESTATIONS_CHOICES, max_length=100, blank=True)  # Réponse Q2
    r2_autre = models.CharField(max_length=255, blank=True, null=True)

    r3 = models.BooleanField(default=True)
    r3_non = models.CharField(max_length=255, blank=True, null=True)

    r4 = MultiSelectField(choices=ELEMENTS_CHOICES, max_length=100, blank=True)

    r5 = models.BooleanField(default=True)
    r5_raison = models.CharField(max_length=255, blank=True, null=True)

    r6 = models.BooleanField(default=True)
    r6_raison = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Réponse au questionnaire {self.questionnaire.id} ({self.date_reponse.date()})"

# Modele Prestation

'''
class Presta(models.Model):
    PRESTATIONS_CHOICES = (
        ('location', 'Location panneaux'),
        ('confection', 'Confection support de communication'),
        ('evenementiel', 'Événementiel'),
        ('etude', 'Étude de marché'),
        ('impression', 'Impression/production de gadgets'),
        ('media', 'Travaux médias'),
        ('autres', 'Autres (précisez)'),
    )

    ELEMENTS_CHOICES = (
        ('Qualité promise', 'Qualité promise'),
        ('Délais de livraison promis ', 'Délais de livraison promis '),
        ('Respect des engagements de l’agence', 'Respect des engagements de l’agence'),
    )


    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE, related_name="reponses2")
    date_reponse = models.DateTimeField(auto_now_add=True)

    nom = models.CharField(max_length=100, null=True, blank=True)
    raison = models.CharField(max_length=100, null=True, blank=True)
    fonction = models.CharField(max_length=100, null=True, blank=True)

    r1 = models.BooleanField(default=True)  # Réponse à Q1
    r2 = models.BooleanField(default=True)  # Réponse à Q1
    r2 = models.BooleanField(default=True)  # Réponse à Q1
    r2 = MultiSelectField(choices=PRESTATIONS_CHOICES, max_length=100, blank=True)  # Réponse Q2
    r2_autre = models.CharField(max_length=255, blank=True, null=True)

    r3 = models.BooleanField(default=True)
    r3_non = models.CharField(max_length=255, blank=True, null=True)

    r4 = MultiSelectField(choices=ELEMENTS_CHOICES, max_length=100, blank=True)

    r5 = models.BooleanField(default=True)
    r5_raison = models.CharField(max_length=255, blank=True, null=True)

    r6 = models.BooleanField(default=True)
    r6_raison = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Réponse au questionnaire {self.questionnaire.id} ({self.date_reponse.date()})"
'''

# Modele Rapport

class Rapport(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    fichier = models.FileField(upload_to='rapports/', null=False, blank=False)
    date_debut = models.DateField()
    date_fin = models.DateField()

    def __str__(self):
        return f"Rapport {self.utilisateur.user.first_name} - du {self.date_debut} au {self.date_fin} - {self.statut}"
