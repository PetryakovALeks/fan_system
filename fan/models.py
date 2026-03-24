from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Поле Email должно быть заполнено')
        email = self.normalize_email(email).lower()  # Приводим email к нижнему регистру
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Хешируем пароль
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    last_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    role = models.ForeignKey('Role', on_delete=models.SET_NULL, null=True)
    is_active = models.BooleanField(default=True)  # Добавляем поле is_active
    is_staff = models.BooleanField(default=False)  # Добавляем поле is_staff

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['last_name', 'first_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'fan_customuser'

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)  # Добавляем уникальность

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fan_role'

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Добавляем уникальность

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fan_sport'

class League(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='leagues')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fan_league'
        unique_together = [['name', 'sport']]  # Уникальность связки name + sport

class Team(models.Model):
    name = models.CharField(max_length=100)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='teams')
    color_left = models.CharField(max_length=7, default='#ffffff')
    color_right = models.CharField(max_length=7, default='#ffffff')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'fan_team'
        unique_together = [['name', 'league']]  # Уникальность связки name + league

class UserPreference(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    custom_color_left = models.CharField(max_length=7, blank=True, null=True)
    custom_color_right = models.CharField(max_length=7, blank=True, null=True)

    def __str__(self):
        return f"{self.user.email} - {self.team.name}"

    class Meta:
        db_table = 'fan_userpreference'
        unique_together = [['user', 'team']]  # Пользователь не может иметь два одинаковых предпочтения

class Match(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='home_matches')
    opponent = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='away_matches')
    date = models.DateTimeField()
    location = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.team.name} vs {self.opponent.name} on {self.date}"

    class Meta:
        db_table = 'fan_match'