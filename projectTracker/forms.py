from django import forms
from Trackerapp.models import Utilisateur
from django.contrib.auth.models import User


class UtilisateurF(forms.ModelForm):
    class Meta:
        model = User
        exclude = ['password']
        fields = ['username', 'first_name', 'email']

class UtilisateurSupF(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['poste', 'direction']