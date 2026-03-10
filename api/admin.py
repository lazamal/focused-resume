from django.contrib import admin
from .models import Skill

# Register your models here.

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'alt_name', 'description']
    search_fields = ['name', 'alt_name']