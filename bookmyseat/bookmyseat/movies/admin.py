from django.contrib import admin
from .models import Movie, Theater, Seat, Booking, Genre

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ['name', 'rating', 'language']
    list_filter = ['language', 'genres']
    search_fields = ['name', 'cast']

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ['name', 'Movie', 'time']

@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ['Theater', 'seat_number', 'is_booked']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['user', 'seat', 'movie', 'theater', 'booked_at']


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ['name']




