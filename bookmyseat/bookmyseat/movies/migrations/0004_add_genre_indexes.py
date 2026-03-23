from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("movies", "0003_alter_movie_language"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS movies_movie_genres_genre_id_movie_id_idx
                ON movies_movie_genres (genre_id, movie_id);
                CREATE INDEX IF NOT EXISTS movies_movie_genres_movie_id_genre_id_idx
                ON movies_movie_genres (movie_id, genre_id);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS movies_movie_genres_genre_id_movie_id_idx;
                DROP INDEX IF EXISTS movies_movie_genres_movie_id_genre_id_idx;
            """,
        ),
    ]
