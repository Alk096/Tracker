from django.contrib import admin
from . import models

admin.site.register(models.Projet)
admin.site.register(models.Utilisateur)
admin.site.register(models.Client)
admin.site.register(models.Prestation)
admin.site.register(models.Note)
admin.site.register(models.Questionnaire)
admin.site.register(models.ReponseQuestionnaire)
admin.site.register(models.ReponsePapi)