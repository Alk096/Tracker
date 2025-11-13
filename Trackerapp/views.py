from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from . import models, forms

from django.http import FileResponse, Http404
import os
import calendar
import json
from django.db.models import Count,Q
from django.db.models.functions import ExtractMonth,ExtractWeekDay
from django.utils import timezone
from datetime import date,timedelta

#Vue des Dashboards

'''
@login_required(login_url='Connexion')
def dashboard_view(request):
    directions = [
        d[0] for d in models.Utilisateur.mes_directions
        if d[0] not in [
            'Administration - Comptabilite - Finance',
            'Direction Generale'
        ]
    ]
    projets_groupes = {}
    projets_count = {}

    for direction in directions:
        projets = models.Projet.objects.filter(direction=direction).exclude(statut=True)
        projets_groupes[direction] = projets
        projets_count[direction] = projets.count()  # le count ici

    context = {
        'projets_groupes': projets_groupes,
        'projets_count': projets_count
    }

    return render(request, "Tracker/dashboard.html", context=context)
'''



@login_required(login_url='Connexion')
def dashboard2_view(request):
    directions = [d[0] for d in models.Utilisateur.mes_directions]
    n_presta = models.Prestation.objects.filter(statut=False).count()
    n_palive = models.Projet.objects.filter(statut=False).count()
    n_pended = models.Projet.objects.filter(statut=True).count()
    n_rapport = models.Rapport.objects.count()

    # Calcule des ratio d'evolution
    
    mois_actu = timezone.now().month
    annee_actuelle = timezone.now().year
    
    mois_passe = timezone.now().month -1
    annee_passe = timezone.now().year
    
    # if mois_passe == 0 Comment marche le systeme de mois des orm Django ??
    # Ratio projet en cours
    palive_mois_passe_count = (models.Projet.objects
        .filter(
            statut=False,
            date_debut__year=annee_passe,
            date_debut__month=mois_passe
        ).count()
    )
    
    palive_mois_actu_count = (models.Projet.objects
        .filter(
            statut=False,
            date_debut__year=annee_actuelle,
            date_debut__month=mois_actu
        ).count()
    )
    
    if palive_mois_passe_count > 0:
        p_projet = ((palive_mois_actu_count - palive_mois_passe_count) / palive_mois_passe_count)*100
    else:
        p_projet = 0
        
    p_projet = round(p_projet, 1)
    
    # Ratio Projet termine
    pended_mois_passe_count = (models.Projet.objects
        .filter(
            statut = True,
            date_debut__year=annee_passe,
            date_debut__month=mois_passe
        ).count()
    )
    
    pended_mois_actu_count = (models.Projet.objects
        .filter(
            statut = True,
            date_debut__year=annee_actuelle,
            date_debut__month=mois_actu
        ).count()
    )
    
    if pended_mois_passe_count > 0:
        p_projet_termine = ((pended_mois_actu_count - pended_mois_passe_count) / pended_mois_passe_count) * 100
    else:
        p_projet_termine = 0
        
    p_projet_termine = round(p_projet_termine, 1)
    
    # Ratio taches en cours
    talive_mois_passe_count = (models.Prestation.objects
        .filter(
            statut = False,
            date_fin__year=annee_passe,
            date_fin__month=mois_passe
        ).count()
    )
    
    talive_mois_actu_count = (models.Prestation.objects
        .filter(
            statut = False,
            date_fin__year=annee_actuelle,
            date_fin__month=mois_actu
        ).count() 
    )
    
    if talive_mois_passe_count > 0:
        p_talive = ((talive_mois_actu_count - talive_mois_passe_count) / talive_mois_passe_count ) * 100
    else:
        p_talive = 0
    
    p_talive = round(p_talive, 1)
    
    # Ratio Rapport
    rapport_mois_passe_count = (
        models.Rapport.objects
        .filter(
            date_debut__year=annee_passe,
            date_debut__month=mois_passe
        ).count()
    )
    
    rapport_mois_actu_count = (models.Rapport.objects
        .filter(
            date_debut__year=annee_actuelle,
            date_debut__month=mois_actu
        ).count()
    )
    
    if rapport_mois_passe_count > 0:
        p_rapport = ((rapport_mois_actu_count - rapport_mois_passe_count)) * 100
    else:
        p_rapport = 0
    
    p_rapport = round(p_rapport, 1)
    
        
    projets_groupes = {}
    projets_count = {}
    projets = models.Projet.objects.filter(statut=False)
    for direction in directions:
        #projets = models.Projet.objects.filter(direction=direction).exclude(statut=True)
        projets_groupes[direction] = projets
        projets_count[direction] = projets.count()  # le count ici
        
    today = date.today()
    start_week = today - timedelta(days=today.weekday())
    end_week = start_week + timedelta(days=6)
    taches_journalier_terminer = (
        models.Prestation.objects
        .filter(
            date_fin__gte=start_week,
            date_fin__lte=end_week,
            statut = True
            
        )
        .annotate(jour=ExtractWeekDay('date_fin'))
        .values('jour')
        .annotate(nombre=Count('id'))
        .order_by('jour')
    )


    # Construire les labels et les données
    presta_jours_data = []
    presta_jours_labels = []
    jours_fr = {
        0:"Dim",
        1:"Lun",
        2:"Mer",
        3:"Jeu",
        4:"Ven",
        5:"Sam"
    }
    for item in taches_journalier_terminer:
        jour_num = item['jour'] - 2
        presta_jours_labels.append(jours_fr[jour_num])
        presta_jours_data.append(item['jour'])
        
        
    prestations_terminees = (
        models.Prestation.objects
        .filter(statut=True)
        .annotate(mois=ExtractMonth('date_fin'))
        .values('mois')
        .annotate(nombre=Count('id'))
        .order_by('mois')
    )

    # Construire les labels et les données
    presta_mois_labels = []
    presta_data_values = []

    for item in prestations_terminees:
        mois_num = item['mois']
        presta_mois_labels.append(calendar.month_abbr[mois_num])  # ex: 'Jan', 'Feb'
        presta_data_values.append(item['nombre'])

    projets_par_mois = (
        models.Projet.objects
        .filter(date_debut__year=annee_actuelle)
        .annotate(mois=ExtractMonth('date_debut'))
        .values('mois')
        .annotate(nombre=Count('id'))
        .order_by('mois')
    )

    # Génération des labels et des données
    projet_mois_labels = []
    projet_data_values = []
    
    for item in projets_par_mois:
        projet_mois_labels.append(calendar.month_abbr[item['mois']])  # ex: "Jan", "Feb"
        projet_data_values.append(item['nombre'])
    
    # Classement des client
    client_top = (models.Client.objects
        .annotate(
            projets=Count('projet')
        )
        .order_by('-projets')[:5]
    )

    context = {
        'projets': projets,
        'projets_groupes': projets_groupes,
        'projets_count': projets_count,
        'presta_labels_json': json.dumps(presta_mois_labels),
        'presta_data_json': json.dumps(presta_data_values),
        'n_presta': n_presta,
        'n_palive': n_palive,
        'n_rapport': n_rapport,
        'n_pended': n_pended,
        'p_projet': p_projet,
        'p_projet_termine':p_projet_termine,
        'p_talive': p_talive,
        'p_rapport': p_rapport,
        'client_top': client_top,
        'presta_jours_labels_json': json.dumps(presta_jours_labels),
        'presta_jours_data_json': json.dumps(presta_jours_data),
        'projet_labels_json': json.dumps(projet_mois_labels),
        'projet_data_json': json.dumps(projet_data_values),
    }

    return render(request, "Tracker/dashboard2.html", context=context)


#Gestion des Clients
@login_required(login_url='Connexion')
def clients_view(request):
    clients = models.Client.objects.all()
    context = {
        'clients': clients
    }
    return render(request, "Tracker/clients_liste.html", context=context)

@login_required(login_url='Connexion')
def client_add_view(request):
    form1 = forms.ClientF()
    mes_forms = {'form1': form1}
    if request.method == 'POST':
        form1 = forms.ClientF(request.POST)
        if form1.is_valid():
            client = form1.save(commit=False)
            client.save()
            return redirect('clients_liste')
        else:
            print(form1.errors)
    return render(request, 'Tracker/client_add.html', context=mes_forms)

@login_required(login_url='Connexion')
def client_update_view(request, id):
    mon_client = models.Client.objects.get(id=id)
    if request.method == 'POST':
        form = forms.ClientF(request.POST, instance=mon_client)
        if form.is_valid():
            form.save()
            return redirect('clients_liste')
    else:
        mon_client = get_object_or_404(models.Client, id=id)
        form = forms.ClientF(instance=mon_client)

    context = {
        'form': form,
        'mon_client': mon_client
    }
    return render(request, 'Tracker/client_update.html', context=context)

@login_required(login_url='Connexion')
def client_supp_view(request, id):
    mon_client = get_object_or_404(models.Client, id=id)
    mon_client.delete()
    return redirect('clients_liste')

#Gestion des Projets

@login_required(login_url='Connexion')
def projets_view(request):
    projets = models.Projet.objects.filter(direction=request.user.utilisateur.direction)
    context = {
        'projets': projets
    }
    return render(request, "Tracker/projets_liste.html", context=context)


@login_required(login_url='Connexion')
def telecharger_qr_code(request, id):
    try:
        projet = models.Projet.objects.get(id=id)
    except models.Projet.DoesNotExist:
        raise Http404("Projet introuvable")

    if not projet.qr_code:
        raise Http404("Ce projet n'a pas de QR code")

    file_path = projet.qr_code.path
    if not os.path.exists(file_path):
        raise Http404("Fichier QR code introuvable")

    # Téléchargement
    return FileResponse(open(file_path, "rb"), as_attachment=True, filename=os.path.basename(file_path))


@login_required(login_url='Connexion')
def projet_add_view(request):
    form1 = forms.ProjetF()
    mes_forms = {'form1': form1}
    if request.method == 'POST':
        form1 = forms.ProjetF(request.POST)
        if form1.is_valid():
            projet = form1.save(commit=False)
            projet.direction = request.user.utilisateur.direction
            projet.utilisateur = request.user.utilisateur
            projet.save()
            return redirect('prestations_add', id=projet.id)
        else:
            print(form1.errors)
    return render(request, 'Tracker/projet_add.html', context=mes_forms)

@login_required(login_url='Connexion')
def projet_details_view(request, id):
    mon_projet = models.Projet.objects.get(id=id)
    prestations = models.Prestation.objects.filter(projet=mon_projet)
    notes = models.Note.objects.filter(prestation__projet=mon_projet)

    context = {
        'prestations': prestations,
        'notes': notes,
        'mon_projet': mon_projet
    }
    return render(request, 'Tracker/projet_details.html', context=context)

@login_required(login_url='Connexion')
def projet_update_view(request, id):
    mon_projet = models.Projet.objects.get(id=id)
    if request.method == 'POST':
        form = forms.ProjetF(request.POST, instance=mon_projet)
        if form.is_valid():
            form.save()
            return redirect('projets_liste')
    else:
        ma_permission = get_object_or_404(models.Projet, id=id)
        form = forms.ProjetF(instance=ma_permission)

    context = {
        'form': form,
        'mon_projet': mon_projet
    }
    return render(request, 'Tracker/projet_update.html', context=context)

@login_required(login_url='Connexion')
def projet_supp_view(request, id):
    mon_projet = get_object_or_404(models.Projet, id=id)
    mon_projet.delete()
    return redirect('projets_liste')

@login_required(login_url='Connexion')
def projet_end_view(request, id):
    mon_projet = get_object_or_404(models.Projet, id=id)
    mon_projet.statut = True
    prestations = models.Prestation.objects.filter(projet=mon_projet)
    for p in prestations:
        p.statut = True
        p.save()
    mon_projet.save()
    return redirect('projets_liste')

# Gestion des prestations

@login_required(login_url='Connexion')
def prestations_add_view(request, id):
    mon_projet = models.Projet.objects.get(id=id)
    if request.method == 'POST':
        form = forms.PrestationF(request.POST)
        if form.is_valid():
            prestation = form.save(commit=False)
            prestation.projet = mon_projet
            prestation.save()
            if "save_quit" in request.POST:
                return redirect('projet_details', id=mon_projet.id)
            elif "save_add" in request.POST:
                return redirect('prestations_add', id=mon_projet.id)
        else:
             print(form.errors)        
    else:
        form = forms.PrestationF()
       

    return render(request, 'Tracker/prestation_add.html', {
        'mon_projet': mon_projet,
        'form': form
    })


@login_required(login_url='Connexion')
def prestation_update_view(request, id):
    ma_presta = models.Prestation.objects.get(id=id)
    if request.method == 'POST':
        form = forms.PrestationF(request.POST, instance=ma_presta)
        if form.is_valid():
            form.save()
            return redirect('projet_details', id=ma_presta.projet.id)
    else:
        ma_presta = get_object_or_404(models.Prestation, id=id)
        form = forms.PrestationF(instance=ma_presta)
    return render(request, 'Tracker/prestation_update.html',
              {'form': form, 'ma_presta': ma_presta})

@login_required(login_url='Connexion')
def prestation_supp_view(request, id):
    ma_prestation = get_object_or_404(models.Prestation, id=id)
    projet = ma_prestation.projet
    ma_prestation.delete()
    return redirect('projet_details', id=projet.id)

@login_required(login_url='Connexion')
def prestation_end_view(request, id):
    ma_prestation = get_object_or_404(models.Prestation, id=id)
    projet = ma_prestation.projet
    ma_prestation.statut = True
    ma_prestation.date_fin = timezone.now().date()
    ma_prestation.save()
    # Vérifier si toutes les prestations de ce projet sont terminées
    toutes_terminees = not models.Prestation.objects.filter(projet=projet, statut=False).exists()

    if toutes_terminees:
        projet.statut = True
        projet.save()
    return redirect('projet_details', id=projet.id)

# Gestion des Notes

@login_required(login_url='Connexion')
def note_add_view(request, id):
    ma_prestation = models.Prestation.objects.get(id=id)
    if request.method == 'POST':
        form = forms.NoteF(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.prestation = ma_prestation
            note.auteur = request.user.utilisateur
            note.save()
            return redirect('projet_details', id=ma_prestation.projet.id)
    else:
        form = forms.NoteF()

    return render(request, 'Tracker/note_add.html', {
        'ma_prestation': ma_prestation,
        'form': form
    })

@login_required(login_url='Connexion')
def note_update_view(request, id):
    ma_note = models.Note.objects.get(id=id)
    projet = ma_note.prestation.projet
    if request.method == 'POST':
        form = forms.NoteF(request.POST, instance=ma_note)
        if form.is_valid():
            form.save()
            return redirect('projet_details', id=projet.id)
    else:
        ma_note = get_object_or_404(models.Note, id=id)
        form = forms.NoteF(instance=ma_note)

    context = {
        'form': form,
        'ma_note': ma_note
    }
    return render(request, 'Tracker/note_update.html', context=context)

@login_required(login_url='Connexion')
def note_supp_view(request, id):
    ma_note = get_object_or_404(models.Note, id=id)
    projet = ma_note.prestation.projet
    ma_note.delete()
    return redirect('projet_details', id=projet.id)

# Questionnaire

def questionnaire_form_view(request, projet_id):
    projet = get_object_or_404(models.Projet, id=projet_id)
    questionnaire = get_object_or_404(models.Questionnaire, projet=projet)
    if request.method == "POST":
        form = forms.ReponseQuestionnaireForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.questionnaire = questionnaire
            reponse.raison = questionnaire.projet.client.raison
            reponse.save()
            return render(request, "Tracker/Dashboard.html", {"projet": projet})
    else:
        form = forms.ReponseQuestionnaireForm()

    return render(
        request,
        "Tracker/Questionnaire.html",
        {"projet": projet, "questionnaire": questionnaire, "form": form},
    )
    
# Gestion Papi

def papi_form_view(request, client_id):
    client = get_object_or_404(models.Client, id=client_id)
    questionnaire = get_object_or_404(models.Papi, client=client)
    if request.method == "POST":
        form = forms.ReponsePapiForm(request.POST)
        if form.is_valid():
            reponse = form.save(commit=False)
            reponse.questionnaire = questionnaire
            reponse.raison = questionnaire.client.raison
            reponse.save()
            return render(request, "Tracker/Dashboard.html", {"client": client})
    else:
        form = forms.ReponsePapiForm()

    return render(
        request,
        "Tracker/Questionnaire.html",
        {"client": client, "questionnaire": questionnaire, "form": form},
    )

def creer_questionnaire_view(request, id):
    projet = get_object_or_404(models.Projet, id=id)

    # Vérifier si le questionnaire existe déjà
    if hasattr(projet, "questionnaire"):
        questionnaire = projet.questionnaire
    else:
        questionnaire = models.Questionnaire.objects.create(projet=projet)

    # Générer le QR code via la méthode du modèle
    qr_file = questionnaire.generate_qr_code()

    # Retourner le QR code en téléchargement
    response = HttpResponse(qr_file, content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="{qr_file.name}"'
    return response

def creer_papi_view(request, id):
    client = get_object_or_404(models.Client, id=id)

    # Vérifier si le questionnaire existe déjà
    if hasattr(client, "papi"):
        questionnaire = client.papi
    else:
        questionnaire = models.Papi.objects.create(client=client)

    # Générer le QR code via la méthode du modèle
    qr_file = questionnaire.generate_qr_code()

    # Retourner le QR code en téléchargement
    response = HttpResponse(qr_file, content_type="image/png")
    response["Content-Disposition"] = f'attachment; filename="{qr_file.name}"'
    return response

# Gestion des Rapports

@login_required(login_url='Connexion')
def rapports_view(request):
    profil = request.user.utilisateur.poste
    profils = ['CDN', 'CG', 'VIP', 'CDV', 'CDM']
    if profil == "CDN":
        rapports = models.Rapport.objects.filter(utilisateur__direction="Transformation Numerique")
    elif profil == "VIP":
        rapports = models.Rapport.objects.filter(utilisateur__direction="Visibilite - Infrastructure - Production")
    elif profil == "CG":
        rapports = models.Rapport.objects.filter(utilisateur__direction="Administration - Comptabilite - Finance")
    elif profil == "CDV":
        rapports = models.Rapport.objects.filter(utilisateur__direction="Ventes et Clientele")
    elif profil == "CDM":
        rapports = models.Rapport.objects.filter(utilisateur__direction="Marketing et Developpement")
    elif profil == "DG":
        rapports = models.Rapport.objects.filter(utilisateur__poste__in=profils)
    else:
        rapports = models.Rapport.objects.filter(utilisateur=request.user.utilisateur)

    context = {
        'rapports': rapports
    }
    return render(request, "Tracker/rapports_liste.html", context=context)

@login_required(login_url='Connexion')
def rapport_add_view(request):
    form1 = forms.RapportF()
    mes_forms = {'form1': form1}
    if request.method == 'POST':
        form1 = forms.RapportF(request.POST, request.FILES)
        if form1.is_valid():
            rapport = form1.save(commit=False)
            rapport.utilisateur = request.user.utilisateur
            rapport.save()
            return redirect('rapports_liste')
        else:
            print(form1.errors)
    return render(request, 'Tracker/rapport_add.html', context=mes_forms)

@login_required(login_url='Connexion')
def rapport_update_view(request, id):
    mon_rapport = models.Rapport.objects.get(id=id)
    if request.method == 'POST':
        form = forms.RapportF(request.POST, instance=mon_rapport)
        if form.is_valid():
            form.save()
            return redirect('rapports_liste')
    else:
        mon_rapport = get_object_or_404(models.Rapport, id=id)
        form = forms.RapportF(instance=mon_rapport)

    context = {
        'form': form,
        'mon_rapport': mon_rapport
    }
    return render(request, 'Tracker/rapport_update.html', context=context)

@login_required(login_url='Connexion')
def rapport_supp_view(request, id):
    mon_rapport = get_object_or_404(models.Rapport, id=id)
    mon_rapport.delete()
    return redirect('rapports_liste')

