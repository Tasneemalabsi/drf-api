from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Character

class CharacterModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        test_user = get_user_model().objects.create_user(username='tasneem',password='pass')
        test_user.save()

        test_character = Character.objects.create(
            writer = test_user,
            name = 'name',
            description = 'about the character',
            death_year = '1999',
        )
        test_character.save()

    def test_blog_content(self):
        character = Character.objects.get(id=1)

        self.assertEqual(str(character.writer), 'tasneem')
        self.assertEqual(character.name, 'name')
        self.assertEqual(character.description, 'about the character')
        self.assertEqual(character.death_year, '1999')
        

class APITest(APITestCase):
    def test_list(self):
        response = self.client.get(reverse('characters_list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_detail(self):

        test_user = get_user_model().objects.create_user(username='tester',password='pass')
        test_user.save()

        test_character = Character.objects.create(
            writer = test_user,
            name = 'name',
            description = 'about the character',
            death_year = '1999',
        )
        test_character.save()

        response = self.client.get(reverse('characters_detail', args=[1]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

    def test_create(self):
        test_user = get_user_model().objects.create_user(username='tasneem',password='pass')
        test_user.save()

        url = reverse('characters_list')
        data = {
            "name": 'anything',
            'description': 'whatever',
            'death_year': '2000',
            "writer":test_user.id,
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED, test_user.id)

        self.assertEqual(Character.objects.count(), 1)
        self.assertEqual(Character.objects.get().name, data["name"])

    def test_update(self):
        test_user = get_user_model().objects.create_user(username='tasneem',password='pass')
        test_user.save()

        test_character = Character.objects.create(
            writer = test_user,
            name = 'any',
            description = '...',
            death_year = '2000',
        )

        test_character.save()

        url = reverse('characters_detail',args=[test_character.id])
        data = {
            "name":"any",
            "writer":test_character.writer.id,
            "description":test_character.description,
            'death_year':test_character.death_year
        }

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK, url)

        self.assertEqual(Character.objects.count(), test_character.id)
        self.assertEqual(Character.objects.get().name, data['name'])


    def test_delete(self):
        """Test the api can delete a character."""

        test_user = get_user_model().objects.create_user(username='tasneem',password='pass')
        test_user.save()

        test_character = Character.objects.create(
            writer = test_user,
            name = 'any',
            description = '...',
            death_year = '2000',
        )

        test_character.save()

        character = Character.objects.get()

        url = reverse('characters_detail', kwargs={'pk': character.id})


        response = self.client.delete(url)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT, url)
