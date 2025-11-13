from django.urls import path
from . import views
from django.conf.urls.static import static
from projectTracker import settings

urlpatterns = [

    path("Dashboard", views.dashboard2_view, name="Dashboard"),

    path('clients_liste', views.clients_view, name="clients_liste"),
    path('client_add', views.client_add_view, name="client_add"),
    path('client_update/<int:id>', views.client_update_view, name="client_update"),
    path('client_supp/<int:id>', views.client_supp_view, name="client_supp"),
    #path('client_details/<int:id>', views.client_details_view, name="client_details"),

    path('projets_liste', views.projets_view, name="projets_liste"),
    path('projet_add', views.projet_add_view, name="projet_add"),
    path('projet_update/<int:id>', views.projet_update_view, name="projet_update"),
    path('projet_supp/<int:id>', views.projet_supp_view, name="projet_supp"),
    path('projet_details/<int:id>', views.projet_details_view, name="projet_details"),
    path('projet_end/<int:id>', views.projet_end_view, name="projet_end"),
    path("down_qr/<int:id>", views.telecharger_qr_code, name="down_qr"),
    path("gen_qr/<int:id>", views.creer_questionnaire_view, name="gen_qr"),
    path("gen_papi_qr/<int:id>", views.creer_papi_view, name="gen_papi_qr"),
    path("Questionnaire/<int:projet_id>/", views.questionnaire_form_view, name="Questionnaire"),
    path("PAPI/<int:client_id>/", views.papi_form_view, name="papi"),


    path('prestations_add/<int:id>', views.prestations_add_view, name='prestations_add'),
    path('prestation_supp/<int:id>', views.prestation_supp_view, name='prestation_supp'),
    path('prestation_update/<int:id>', views.prestation_update_view, name='prestation_update'),
    path('prestation_end/<int:id>', views.prestation_end_view, name='prestation_end'),

    path('note_add/<int:id>', views.note_add_view, name="note_add"),
    path('note_update/<int:id>', views.note_update_view, name="note_update"),
    path('note_supp/<int:id>', views.note_supp_view, name="note_supp"),

    path('rapports_liste', views.rapports_view, name="rapports_liste"),
    path('rapport_add', views.rapport_add_view, name="rapport_add"),
    path('rapport_update/<int:id>', views.rapport_update_view, name="rapport_update"),
    path('rapport_supp/<int:id>', views.rapport_supp_view, name="rapport_supp"),

]
