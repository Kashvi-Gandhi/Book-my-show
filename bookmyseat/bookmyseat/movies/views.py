from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.core.paginator import Paginator

from .models import Movie, Theater, Seat, Booking, Genre


def movie_list(request):
    """
    Server-side movie listing with multi-select genre/language filters,
    pagination, sorting, and facet counts.
    """
    genre_ids = [g for g in request.GET.getlist("genres") if g]  # list of non-empty strings
    languages = [l for l in request.GET.getlist("languages") if l]
    search_query = request.GET.get("search")
    sort = request.GET.get("sort", "rating_desc")
    page_number = request.GET.get("page", 1)
    page_size = request.GET.get("page_size", 9)

    try:
        page_size = max(1, min(int(page_size), 50))  # cap page size
    except ValueError:
        page_size = 9

    order_map = {
        "rating_desc": ("-rating", "-id"),
        "rating_asc": ("rating", "id"),
        "name": ("name", "id"),
        "newest": ("-id",),
    }
    ordering = order_map.get(sort, ("-rating", "-id"))

    # Prefetch genres to avoid N+1 on result cards; keeps facet queries separate.
    base_qs = Movie.objects.prefetch_related("genres").all()

    if search_query:
        base_qs = base_qs.filter(name__icontains=search_query)

    cleaned_genre_ids = [int(g) for g in genre_ids if g.isdigit()]
    if cleaned_genre_ids:
        base_qs = base_qs.filter(genres__id__in=cleaned_genre_ids).distinct()

    if languages:
        base_qs = base_qs.filter(language__in=languages)

    base_qs = base_qs.order_by(*ordering)

    paginator = Paginator(base_qs, page_size)
    page_obj = paginator.get_page(page_number)
    total_count = paginator.count
    start_index = page_obj.start_index() if total_count else 0
    end_index = page_obj.end_index() if total_count else 0
    query_params = request.GET.copy()
    query_params.pop("page", None)
    base_querystring = query_params.urlencode()

    # Facet counts
    genre_facet_qs = Movie.objects.all()
    if search_query:
        genre_facet_qs = genre_facet_qs.filter(name__icontains=search_query)
    if languages:
        genre_facet_qs = genre_facet_qs.filter(language__in=languages)
    genre_facets = (
        Genre.objects.filter(movies__in=genre_facet_qs)
        .annotate(count=Count("movies", distinct=True))
        .order_by("name")
    )
    genre_count_map = {g.id: g.count for g in genre_facets}
    all_genres = Genre.objects.all().order_by("name")
    genre_list = [(g, genre_count_map.get(g.id, 0)) for g in all_genres]

    language_facet_qs = Movie.objects.all()
    if search_query:
        language_facet_qs = language_facet_qs.filter(name__icontains=search_query)
    if cleaned_genre_ids:
        language_facet_qs = language_facet_qs.filter(genres__id__in=cleaned_genre_ids).distinct()
    language_facets = (
        language_facet_qs.values("language")
        .annotate(count=Count("id"))
        .order_by("language")
    )
    language_counts = {row["language"]: row["count"] for row in language_facets}
    language_choices_with_counts = [
        (lang, language_counts.get(lang, 0)) for lang, _ in Movie.LANG_CHOICES
    ]

    context = {
        "movies": page_obj,
        "total_count": total_count,
        "start_index": start_index,
        "end_index": end_index,
        "genres": genre_list,
        "selected_genres": cleaned_genre_ids,
        "selected_languages": languages,
        "language_facets": language_facets,
        "language_counts": language_counts,
        "language_options": language_choices_with_counts,
        "sort": sort,
        "page_size": page_size,
        "page_sizes": [6, 9, 12, 18, 24, 36],
        "search_query": search_query or "",
        "base_querystring": base_querystring,
    }
    return render(request, "movies/movie_list.html", context)

def theater_list(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    theater = Theater.objects.filter(Movie=movie)
    return render(request, 'movies/theater_list.html', {'movie': movie, 'theaters': theater})

@login_required(login_url='/login/')
def book_seats(request, theater_id):
    theater = get_object_or_404(Theater, id=theater_id)
    seats = Seat.objects.filter(Theater=theater)
    if request.method == 'POST':
        selected_seats = request.POST.getlist('seats')
        error_seats = []
        if not selected_seats:
            return render(request, 'movies/seat_selection.html', {'theater': theater, 'seats': seats, 'error': 'Please select at least one seat.'})
        for seat_id in selected_seats:
            seat = get_object_or_404(Seat, id=seat_id, Theater=theater)
            if seat.is_booked:
                error_seats.append(seat.seat_number)
                continue
            try:
                Booking.objects.create(user=request.user, seat=seat, movie=theater.Movie, theater=theater)
                seat.is_booked = True
                seat.save()
            except IntegrityError:
                error_seats.append(seat.seat_number)
        if error_seats:
            error_message = f"The following seats are already booked: {', '.join(error_seats)}. Please select different seats."
            return render(request, 'movies/seat_selection.html', {'theater': theater, 'seats': seats, 'error': error_message})
        return redirect('profile')
    return render(request, 'movies/seat_selection.html', {'theater': theater, 'seats': seats})
