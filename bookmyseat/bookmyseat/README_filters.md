# Movies filtering, paging, and indexing rationale

## What we added
- Server-side multi-select filtering for genres (M2M) and languages (enum) with facet counts that respect active filters.
- Pagination + sorting (`rating_desc` default) on the same queries.
- Prefetch of `genres` to avoid N+1 on result rendering.
- Composite indexes on:
  - `movies_movie (language, id)` → speeds language filter with stable pagination.
  - `movies_movie (-rating, id)` → supports rating sort with deterministic tie-breaker.
  - `movies_movie_genres (genre_id, movie_id)` and `(movie_id, genre_id)` → speeds genre filters and faceting by enabling index joins on the M2M table.

## Query shape (high level)
1) Base queryset:
   - `Movie.objects.prefetch_related("genres")`
   - `filter(genres__id__in=GENRES)` when provided (uses `genre_id` index).
   - `filter(language__in=LANGS)` when provided (uses `(language, id)` index).
   - `order_by("-rating", "-id")` (uses rating index).
2) Facet counts:
   - Genres: `Genre.objects.filter(movies__in=filtered_movies).annotate(count=Count(...))`
   - Languages: same filtered movies grouped by `language`.
3) Pagination: `Paginator` with capped `page_size` (max 50).

## Trade-offs
- Extra indexes increase write cost slightly but keep read time low for catalogs in the 5k–50k range.
- Using `prefetch_related` adds one extra query but prevents per-row genre lookups.
- `distinct()` only used when genre filter is active to avoid duplicate rows from the M2M join.

## How to validate
- Run `python manage.py test movies.tests` (covers genre/lang filters, sorting, facet counts).
- For Postgres, you can inspect plans: `EXPLAIN ANALYZE SELECT ... WHERE genre_id IN (...)` to confirm index usage on `movies_movie_genres`.
