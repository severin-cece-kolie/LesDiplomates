from django.contrib import admin
from .models import RegulationChapter, SuccessStat, TeamMember, AdmissionExam, Actualite, SchoolLife

@admin.register(RegulationChapter)
class RegulationChapterAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)

@admin.register(SuccessStat)
class SuccessStatAdmin(admin.ModelAdmin):
    list_display = ('label', 'value', 'year', 'is_active')
    list_filter = ('is_active', 'year')
    list_editable = ('value', 'is_active')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)

@admin.register(AdmissionExam)
class AdmissionExamAdmin(admin.ModelAdmin):
    list_display = ('type', 'annee', 'total_candidats', 'total_admis', 'taux_reussite_display')
    
    def taux_reussite_display(self, obj):
        return f"{obj.taux_reussite:.1f}%"
    taux_reussite_display.short_description = "Taux de Réussite"

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_pub', 'is_published')
    list_filter = ('is_published', 'date_pub')
    prepopulated_fields = {'slug': ('title',)}

@admin.register(SchoolLife)
class SchoolLifeAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'order')
    list_editable = ('order',)
