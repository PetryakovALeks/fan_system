from django.contrib import admin
from .models import CustomUser, Role, Sport, League, Team, UserPreference, Match

class MatchAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "opponent":
            if request.method == 'POST' and 'team' in request.POST:
                team_id = request.POST.get('team')
            elif hasattr(request, '_saved_team_id'):
                team_id = request._saved_team_id
            else:
                return kwargs

            if team_id:
                team = Team.objects.get(pk=team_id)
                kwargs["queryset"] = Team.objects.filter(league=team.league).exclude(id=team_id)
                request._saved_team_id = team_id
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(CustomUser)
admin.site.register(Role)
admin.site.register(Sport)
admin.site.register(League)
admin.site.register(Team)
admin.site.register(UserPreference)
admin.site.register(Match, MatchAdmin)