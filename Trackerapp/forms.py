from django import forms
from . import models

class ClientF(forms.ModelForm):
    class Meta:
        model = models.Client
        fields = '__all__'

# Projet Form

class ProjetF(forms.ModelForm):
    class Meta:
        model = models.Projet
        exclude = ['statut', 'qr_code', 'direction', 'utilisateur']

        widget = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'utilisateur': forms.HiddenInput()
        }

# Rapport Form

class RapportF(forms.ModelForm):
    class Meta:
        model = models.Rapport
        fields = ['date_debut', 'date_fin', 'fichier']

        widget = {
            'date_debut': forms.DateInput(attrs={'type': 'date'}),
            'date_fin': forms.DateInput(attrs={'type': 'date'}),
            'utilisateur': forms.HiddenInput()
        }        

# Prestation Form

class PrestationF(forms.ModelForm):
    class Meta:
        model = models.Prestation
        exclude = ['statut', 'projet']


# Note Form

class NoteF(forms.ModelForm):
    class Meta:
        model = models.Note
        fields = ['contenu']
        widget = {
            'prestation': forms.HiddenInput(),
        }

# Questionnaire Forn 

class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = models.Questionnaire
        fields = ["lien"]  # uniquement le champ modifiable
        widgets = {
            "lien": forms.URLInput(attrs={"class": "form-control", "placeholder": "Lien du questionnaire"}),
        }

# Response Questionnaire Form

class ReponseQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = models.ReponseQuestionnaire
        fields = [
            "nom", "raison", "fonction", "telephone",
            "r1", "r2", "r2_autre",
            "r3", "r3_non",
            "r4",
            "r5", "r5_raison",
            "r6", "r6_raison",
        ]
        widgets = {
            "r1": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
            "r2": forms.CheckboxSelectMultiple,
            "r3": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
            "r4": forms.CheckboxSelectMultiple,
            "r5": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
            "r6": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
        }

# Reponse Papi Form

class ReponsePapiForm(forms.ModelForm):
    class Meta:
        model = models.ReponsePapi
        fields = [
            "nom", "raison", "fonction", "telephone",
            "r1", "r2", "r2_autre",
            "r3", "r3_non",
            "r4",
            "r5", "r5_raison",
            "r6", "r6_raison",
        ]
        widgets = {
            "r1": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
            "r2": forms.CheckboxSelectMultiple,
            "r3": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
            "r4": forms.CheckboxSelectMultiple,
            "r5": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
            "r6": forms.RadioSelect(choices=[(True, "Oui"), (False, "Non")]),
        }
