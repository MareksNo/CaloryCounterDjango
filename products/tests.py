from django.test import Client
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from products import models as products_models
from products import views

User = get_user_model()


class FoodTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")

    def test_create_food(self):
        response = self.client.post(reverse('add-food'),
                                    {'name': 'Banananaa', 'description': 'test', 'calories': 200},
                                    follow=True)
        self.assertEqual(products_models.Food.objects.last().description, "test")

    def test_get_no_perm(self):
        self.client.login(username='test', password='test')
        response = self.client.get(reverse('add-food'), follow=True)
        self.assertRedirects(response, '/users/login/')

    def test_get_perm(self):
        content_type = ContentType.objects.get_for_model(products_models.Food)
        permission = Permission.objects.get(content_type=content_type, codename='add_food')
        self.user.user_permissions.add(permission)

        self.client.login(username='test', password='test')
        response = self.client.get(reverse('add-food'), follow=True)
        self.assertEqual(response.status_code, 200)
