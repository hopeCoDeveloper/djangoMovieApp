from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from watchlist_app.api import serializers
from watchlist_app import models

class StreamPlatfromTestCase(APITestCase):

    def setUp(self):
        #create a user and login
        self.user = User.objects.create_user(username='test',password='Password@123')
        self.token = Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        #create a stream platform
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                            about= "Just Netflix",
                                                            website="http://www.netflix.com")

    def test_streamplatform_create(self):
        data = {
            "name":"Netflix",
            "about":"Just Netflix",
            "website":"https://netflix.com"
        }

        response = self.client.post(reverse("streamplatform-list"), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_streamplatform_list(self):
        response = self.client.get(reverse("streamplatform-list"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_streamplatform_ind(self):
        response = self.client.get(reverse("streamplatform-detail", args = (self.stream.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

class WatchListTestCase(APITestCase):

    def setUp(self):
        #create a user and login
        self.user = User.objects.create_user(username='test',password='Password@123')
        self.token = Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        #create a stream platform
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                            about= "Just Netflix",
                                                            website="http://www.netflix.com")
        #create a watchlist
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                            title="test3",
                                                            storyline="test3",
                                                            active=True)
       

    def test_watchlist_create(self):
        data = {
            "platform":self.stream,
            "title":"test",
            "storyline":"test2",
            "active":True
        }
        response = self.client.post(reverse("movie-list"), data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse("movie-list"))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse("movie-detail", args = (self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class ReviewTestCase(APITestCase):

    def setUp(self):
         #create a user and login
        self.user = User.objects.create_user(username='test',password='Password@123')
        self.token = Token.objects.get(user__username= self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        #create a stream platform
        self.stream = models.StreamPlatform.objects.create(name="Netflix",
                                                            about= "Just Netflix",
                                                            website="http://www.netflix.com")
        #create a watchlist
        self.watchlist = models.WatchList.objects.create(platform=self.stream,
                                                            title="test3",
                                                            storyline="test3",
                                                            active=True)
        self.watchlist2 = models.WatchList.objects.create(platform=self.stream,
                                                            title="test4",
                                                            storyline="test4",
                                                            active=True)                                                   

         #create a review
        self.review = models.Review.objects.create(review_user= self.user,rating=5,description="Just",
                                                    watchlist=self.watchlist2,active=True)


    def test_review_create(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"just good",
            "watchlist":self.watchlist,
            "active":True
        }
        response = self.client.post(reverse("review_create",args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(models.Review.objects.count(),2)

        response = self.client.post(reverse("review_create",args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_review_create_unauth(self):
        data = {
            "review_user":self.user,
            "rating":5,
            "description":"just good",
            "watchlist":self.watchlist,
            "active":True
        }
        #to log out
        self.client.force_authenticate(user=None)
        
        response = self.client.post(reverse("review_create",args=(self.watchlist.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)


    def test_review_update(self):
        data = {
            "review_user":self.user,
            "rating":4,
            "description":"just good --updated",
            "watchlist":self.watchlist,
            "active":False
        }
        response = self.client.put(reverse("review_detail",args=(self.review.id,)), data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse("review_list",args=(self.watchlist.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse("review_detail",args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_delete(self):
        response = self.client.delete(reverse("review_detail",args=(self.review.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response = self.client.get('/watch/reviews/?username=' + self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)