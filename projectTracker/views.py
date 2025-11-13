from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from . import forms

def index_view(request):
    return redirect('Connexion')

def user_dashboard_view(request):
    return redirect('Tracker/Dashboard')

def register_view(request):
    form1 = forms.UtilisateurF()
    form2 = forms.UtilisateurSupF()
    mes_forms = {'form1': form1, 'form2': form2}
    if request.method == 'POST':
        form1 = forms.UtilisateurF(request.POST)
        form2 = forms.UtilisateurSupF(request.POST)
        if form1.is_valid() and form2.is_valid():
            form1_data = form1.cleaned_data
            email = form1_data['email']
            username = form1_data['username']
            password = "12345"

            user = User.objects.create_user(username=username, password=password,
                                            first_name=form1_data['first_name'], email=email)
            user.save()
            utilisateur = form2.save(commit=False)
            utilisateur.nom = form1_data['first_name']
            utilisateur.user = user
            utilisateur.save()

            return redirect('Connexion')

        else:
            print(form1.errors)
            print(form2.errors)
    return render(request, "Tracker/sign-up.html", context=mes_forms)

def deconnexion_view(request):
    logout(request)
    return HttpResponseRedirect('Connexion')