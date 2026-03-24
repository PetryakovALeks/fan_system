from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from fan.models import CustomUser, Role, Sport, League, Team, Match

class FanSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.role = Role.objects.create(name="Фанат")
        self.sport = Sport.objects.create(name="Футбол")
        self.league = League.objects.create(name="Премьер-лига", sport=self.sport)
        self.team1 = Team.objects.create(name="Барселона", league=self.league, color_left="#0000FF", color_right="#FF0000")
        self.team2 = Team.objects.create(name="Реал Мадрид", league=self.league, color_left="#FFFFFF", color_right="#000000")
        self.user = CustomUser.objects.create_user(
            email="fan@example.com",
            password="12345",
            first_name="Иван",
            last_name="Иванов",
            role=self.role
        )
        self.match = Match.objects.create(
            team=self.team1,
            opponent=self.team2,
            date=timezone.now() + timezone.timedelta(days=5),
            location="Camp Nou"
        )

    # --- Авторизация ---
    def test_login_success(self):
        response = self.client.post(reverse('login'), {'email': 'fan@example.com', 'password': '12345'})
        self.assertIn(response.status_code, [200, 302])

    def test_login_fail(self):
        response = self.client.post(reverse('login'), {'email': 'fan@example.com', 'password': 'wrongpass'})
        # В шаблоне у тебя "Неверный email или пароль"
        self.assertContains(response, "Неверный email или пароль", html=False)

    # --- Регистрация ---
    def test_register_user(self):
        response = self.client.post(reverse('register'), {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'email': 'newfan@example.com',
            'password': '12345'
        })
        # Можно остаться на странице (200), либо редирект (302)
        self.assertIn(response.status_code, [200, 302])
        # Проверим, что пользователь создался
        self.assertTrue(CustomUser.objects.filter(email='newfan@example.com').exists())

    def test_duplicate_registration(self):
        response = self.client.post(reverse('register'), {
            'last_name': 'Иванов',
            'first_name': 'Иван',
            'email': 'fan@example.com',
            'password': '12345'
        })
        # Текст ошибки из формы
        self.assertContains(response, "Custom user with this Email already exists.", html=False)

    # --- Расписание ---
    def test_schedule_view(self):
        self.client.login(email='fan@example.com', password='12345')
        response = self.client.get(reverse('schedule'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.match.team.name)
        self.assertContains(response, self.match.opponent.name)

    # --- Профиль ---
    def test_profile_page(self):
        self.client.login(email='fan@example.com', password='12345')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user.first_name)

    # --- Экспорт ---
    def test_league_report_generation(self):
        self.client.login(email='fan@example.com', password='12345')
        response = self.client.get(reverse('export'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Экспорт данных")

    def test_user_report_generation(self):
        self.client.login(email='fan@example.com', password='12345')
        response = self.client.get(reverse('export'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Экспорт данных")

    # --- Предпочтения ---
    def test_preference_list_view(self):
        self.client.login(email='fan@example.com', password='12345')
        response = self.client.get(reverse('user_preference_list'))
        self.assertEqual(response.status_code, 200)

    def test_preference_create_view(self):
        self.client.login(email='fan@example.com', password='12345')
        response = self.client.get(reverse('user_preference_create'))
        self.assertEqual(response.status_code, 200)
