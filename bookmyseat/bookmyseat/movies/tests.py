from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Movie, Genre


class MovieFilterTests(TestCase):
    def setUp(self):
        g_action = Genre.objects.create(name="Action")
        g_drama = Genre.objects.create(name="Drama")
        g_comedy = Genre.objects.create(name="Comedy")

        dummy_img = SimpleUploadedFile("test.jpg", b"\x47\x49\x46\x38\x37\x61\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;")

        m1 = Movie.objects.create(name="A", rating=8.5, language="English", cast="A", description="", image=dummy_img)
        m2 = Movie.objects.create(name="B", rating=7.0, language="Hindi", cast="B", description="", image=dummy_img)
        m3 = Movie.objects.create(name="C", rating=9.0, language="English", cast="C", description="", image=dummy_img)

        m1.genres.add(g_action)
        m2.genres.add(g_drama)
        m3.genres.add(g_action, g_comedy)

        self.g_action_id = g_action.id
        self.g_drama_id = g_drama.id

    def test_filter_by_single_genre(self):
        url = reverse("movie_list")
        resp = self.client.get(url, {"genres": [self.g_action_id]})
        self.assertEqual(resp.status_code, 200)
        movies = resp.context["movies"]
        names = {m.name for m in movies}
        self.assertSetEqual(names, {"A", "C"})

    def test_filter_by_language(self):
        url = reverse("movie_list")
        resp = self.client.get(url, {"languages": ["Hindi"]})
        self.assertEqual(resp.status_code, 200)
        movies = resp.context["movies"]
        self.assertEqual(movies.paginator.count, 1)
        self.assertEqual(movies[0].name, "B")

    def test_sort_rating_desc(self):
        url = reverse("movie_list")
        resp = self.client.get(url, {"sort": "rating_desc"})
        movies = list(resp.context["movies"])
        ratings = [m.rating for m in movies]
        self.assertEqual(ratings, sorted(ratings, reverse=True))

    def test_facet_counts_respect_filters(self):
        url = reverse("movie_list")
        resp = self.client.get(url, {"genres": [self.g_action_id]})
        language_facets = list(resp.context["language_options"])
        english_row = next((row for row in language_facets if row[0] == "English"), None)
        self.assertIsNotNone(english_row)
        self.assertEqual(english_row[1], 2)  # two English movies after genre filter
