from django.shortcuts import reverse
from django.contrib.auth import get_user_model

from django.test import TestCase

User = get_user_model()


class UserLoginTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_login_valid(self):
        response = self.client.post(reverse('login'),
                                    {
                                        'username': 'test',
                                        'password': 'test',
                                    },
                                    follow=True,)
        self.assertTrue(response.context['user'].is_active)

    def test_login_invalid(self):
        response = self.client.post(reverse('login'),
                                    {
                                        'username': 'invalid',
                                        'password': 'invalid',
                                    },
                                    follow=True, )
        self.assertFalse(response.context['user'].is_active)


class UserRegistryTest(TestCase):
    def setUp(self):
        self.existing_user = User.objects.create_user(username='test', email='test@test.com', password='test')
        self.invalid_user = {
            'username': 'invalid',
            'email': 'invalid@test.com',
                             }
        self.test_user_data = {
                                        'username': 'tester',
                                        'first_name': 'testing',
                                        'last_name': 'testing',
                                        'email': 'testong@test.com',
                                        'weight': 70,
                                        'height': 180,
                                        'activity': 'BMR',
                                        'gender': 'f',
                                        'age': 14
                            }

    def test_register_valid(self):
        response = self.client.post(reverse('register'),
                                    self.test_user_data,
                                    follow=True)
        # as there is no profile data provided, the profile form is invalid, not registering the user
        self.assertEqual(User.objects.filter(username=self.test_user_data['username']).count(), 1)
        self.assertFalse(User.objects.filter(username=self.invalid_user['username']).count(), 1)
