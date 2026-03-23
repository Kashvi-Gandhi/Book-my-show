from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True, db_index=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Movie(models.Model):
    LANG_CHOICES = [
        ("English", "English"),
        ("Hindi", "Hindi"),
        ("Gujarati", "Gujarati"),
        ("Marathi", "Marathi"),
        ("Other", "Other"),
    ]

    name = models.CharField(max_length=250, db_index=True)
    image = models.ImageField(upload_to="movies/")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    language = models.CharField(max_length=20, choices=LANG_CHOICES, default="English", db_index=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    cast = models.TextField()
    description = models.TextField(blank=True, null=True)

    class Meta:
        # Indexes chosen to support common filters/sorts at scale (language filter + id pagination,
        # rating sort fallback) and combined with explicit M2M indexes in migrations for genre filters.
        indexes = [
            models.Index(fields=["language", "id"]),
            models.Index(fields=["-rating", "id"]),
        ]

    def __str__(self):
        return self.name


class Theater(models.Model):
    name = models.CharField(max_length=250)
    Movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="theaters")
    time = models.DateTimeField()

    def __str__(self):
        return f"{self.name} - {self.Movie.name} at {self.time}"


class Seat(models.Model):
    Theater = models.ForeignKey(Theater, on_delete=models.CASCADE, related_name="seats")
    seat_number = models.CharField(max_length=10)
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat_number} in {self.Theater.name} "


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    seat = models.OneToOneField(Seat, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    theater = models.ForeignKey(Theater, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.seat.seat_number} at {self.theater.name}"
