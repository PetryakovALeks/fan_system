from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import CustomUser, UserPreference, Sport, League, Team

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    patronymic = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ['last_name', 'first_name', 'patronymic', 'email', 'password']


class UserPreferenceCreateForm(forms.ModelForm):
    sport = forms.ModelChoiceField(queryset=Sport.objects.all(), empty_label="---------")
    league = forms.ModelChoiceField(queryset=League.objects.none(), empty_label="---------")
    team = forms.ModelChoiceField(queryset=Team.objects.none(), empty_label="---------")

    class Meta:
        model = UserPreference
        fields = ['team', 'custom_color_left', 'custom_color_right']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user

        self.fields['sport'].required = True
        self.fields['league'].required = True
        self.fields['team'].required = True

        # Если форма используется для редактирования существующих предпочтений
        instance = kwargs.get('instance')
        if instance:
            sport = instance.team.league.sport
            league = instance.team.league

            self.fields['sport'].initial = sport
            self.fields['league'].queryset = League.objects.filter(sport=sport)
            self.fields['league'].initial = league
            self.fields['team'].queryset = Team.objects.filter(league=league)
            self.fields['team'].initial = instance.team

        # Если форма отправляется пользователем (POST)
        elif self.data:
            sport_id = self.data.get('sport')
            league_id = self.data.get('league')

            if sport_id:
                self.fields['league'].queryset = League.objects.filter(sport_id=sport_id)

            if league_id:
                self.fields['team'].queryset = Team.objects.filter(league_id=league_id)

    def clean(self):
        cleaned_data = super().clean()
        sport = cleaned_data.get('sport')
        league = cleaned_data.get('league')
        team = cleaned_data.get('team')

        # Проверка соответствия лиги выбранному виду спорта
        if sport and league:
            if not League.objects.filter(id=league.id, sport_id=sport.id).exists():
                raise forms.ValidationError("The selected league does not match the selected sport.")

        # Проверка соответствия команды выбранной лиге
        if league and team:
            if not Team.objects.filter(id=team.id, league_id=league.id).exists():
                raise forms.ValidationError("The selected team does not match the selected league.")

        return cleaned_data


class UserPreferenceUpdateForm(UserPreferenceCreateForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
