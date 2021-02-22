from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserViewSetTest(APITestCase):
    def setUp(self):
        """
        Method that provides preparation before testing User model's view.
        """
        self.custom_user = User.objects.create(
            pk=111,
            username="custom_user",
            password='1111',
            email='user@mail.com',
            first_name="First",
            last_name="Last",
            birthday="2021-03-01",
            is_active=True,
        )
        self.custom_user.save()

    def test_get_users_without_permission(self):
        """
        Ensure we do not get all users without SuperUser permission
        """
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_users_with_super_user_permission(self):
        """
        Ensure we get all users with SuperUser permission
        """
        self.user = get_user_model().objects.create_superuser(
            "admintest",
            "admintest@admintest.com",
            "admintest"
        )
        self.client.login(username='admintest', password='admintest')
        response = self.client.get('/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Two users including admin
        self.assertEqual(len(response.json()['results']), 2)
        self.assertEqual(response.json()['count'], 2)

    def test_get_users_with_pagination(self):
        """
        Ensure we get users list with pagination
        """
        self.user = get_user_model().objects.create_superuser(
            "admintest",
            "admintest@admintest.com",
            "admintest"
        )
        self.client.login(username='admintest', password='admintest')
        # Create additional users
        User.objects.bulk_create(
            [User(username="user" + str(i)) for i in range(10)]
        )

        response = self.client.get('/users/')

        self.assertEqual(response.json()['count'], 12)
        self.assertEqual(len(response.json()['results']), 10)
        self.assertIsNotNone(response.json()['next'])
