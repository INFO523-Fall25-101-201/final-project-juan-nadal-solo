import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from typing import Set, Dict, List
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection parameters
DB_CONFIG = {
    'dbname': os.environ.get('DB_DATABASE'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'host': os.environ.get('DB_HOST'),
    'port': os.environ.get('DB_PORT'),
}

# File paths
BASE_PATH = r'data\raw\the-movies-dataset'
SCHEMA_NAME = "Movies_dataset"


def create_schema(conn):
    """Create the normalized database schema"""
    cursor = conn.cursor()

    schema_sql = f"""
    -- Create schema if it doesn't exist
    CREATE SCHEMA IF NOT EXISTS "{SCHEMA_NAME}";

    -- Set search path to use the schema
    SET search_path TO "{SCHEMA_NAME}";

    -- Drop tables if they exist (in correct order due to foreign keys)
    DROP TABLE IF EXISTS movie_genres CASCADE;
    DROP TABLE IF EXISTS movie_keywords CASCADE;
    DROP TABLE IF EXISTS movie_production_companies CASCADE;
    DROP TABLE IF EXISTS movie_production_countries CASCADE;
    DROP TABLE IF EXISTS movie_spoken_languages CASCADE;
    DROP TABLE IF EXISTS movie_cast CASCADE;
    DROP TABLE IF EXISTS movie_crew CASCADE;
    DROP TABLE IF EXISTS movie_collections_junction CASCADE;
    DROP TABLE IF EXISTS ratings CASCADE;

    DROP TABLE IF EXISTS genres CASCADE;
    DROP TABLE IF EXISTS keywords CASCADE;
    DROP TABLE IF EXISTS production_companies CASCADE;
    DROP TABLE IF EXISTS production_countries CASCADE;
    DROP TABLE IF EXISTS spoken_languages CASCADE;
    DROP TABLE IF EXISTS cast_members CASCADE;
    DROP TABLE IF EXISTS crew_members CASCADE;
    DROP TABLE IF EXISTS departments CASCADE;
    DROP TABLE IF EXISTS jobs CASCADE;
    DROP TABLE IF EXISTS movie_collections CASCADE;
    DROP TABLE IF EXISTS movie_ids CASCADE;
    DROP TABLE IF EXISTS users CASCADE;
    DROP TABLE IF EXISTS movies CASCADE;

    -- Main movies table
    CREATE TABLE movies (
        id INTEGER PRIMARY KEY,
        title TEXT,
        original_title TEXT,
        overview TEXT,
        release_date DATE,
        runtime INTEGER,
        budget BIGINT,
        revenue BIGINT,
        vote_average NUMERIC(4, 2),
        vote_count INTEGER,
        popularity NUMERIC(10, 6),
        status TEXT,
        tagline TEXT,
        homepage TEXT,
        adult BOOLEAN,
        video BOOLEAN,
        imdb_id TEXT,
        original_language TEXT,
        poster_path TEXT,
        backdrop_path TEXT
    );

    -- Movie collections lookup table
    CREATE TABLE movie_collections (
        collection_id INTEGER PRIMARY KEY,
        name TEXT,
        poster_path TEXT,
        backdrop_path TEXT
    );

    -- Lookup tables with natural IDs from the dataset
    CREATE TABLE genres (
        genre_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE keywords (
        keyword_id INTEGER PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE production_companies (
        company_id INTEGER PRIMARY KEY,
        name TEXT
    );

    -- Lookup tables with auto-generated IDs
    CREATE TABLE production_countries (
        country_id SERIAL PRIMARY KEY,
        iso_code TEXT UNIQUE,
        name TEXT
    );

    CREATE TABLE spoken_languages (
        language_id SERIAL PRIMARY KEY,
        iso_code TEXT UNIQUE,
        name TEXT
    );

    CREATE TABLE cast_members (
        person_id INTEGER PRIMARY KEY,
        name TEXT,
        gender INTEGER,
        profile_path TEXT
    );

    CREATE TABLE crew_members (
        person_id INTEGER PRIMARY KEY,
        name TEXT,
        gender INTEGER,
        profile_path TEXT
    );

    CREATE TABLE departments (
        department_id SERIAL PRIMARY KEY,
        name TEXT UNIQUE
    );

    CREATE TABLE jobs (
        job_id SERIAL PRIMARY KEY,
        title TEXT UNIQUE
    );

    CREATE TABLE movie_ids (
        movie_id INTEGER PRIMARY KEY,
        imdb_id TEXT,
        tmdb_id INTEGER
    );

    CREATE TABLE users (
        user_id INTEGER PRIMARY KEY
    );

    -- Ratings table
    CREATE TABLE ratings (
        rating_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
        movie_id INTEGER,
        rating NUMERIC(2, 1),
        timestamp BIGINT
    );

    -- Junction tables
    CREATE TABLE movie_genres (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        genre_id INTEGER REFERENCES genres(genre_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, genre_id)
    );

    CREATE TABLE movie_keywords (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        keyword_id INTEGER REFERENCES keywords(keyword_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, keyword_id)
    );

    CREATE TABLE movie_production_companies (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        company_id INTEGER REFERENCES production_companies(company_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, company_id)
    );

    CREATE TABLE movie_production_countries (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        country_id INTEGER REFERENCES production_countries(country_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, country_id)
    );

    CREATE TABLE movie_spoken_languages (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        language_id INTEGER REFERENCES spoken_languages(language_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, language_id)
    );

    CREATE TABLE movie_cast (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        person_id INTEGER REFERENCES cast_members(person_id) ON DELETE CASCADE,
        character_name TEXT,
        cast_order INTEGER,
        credit_id TEXT,
        PRIMARY KEY (movie_id, person_id, credit_id)
    );

    CREATE TABLE movie_crew (
        credit_id TEXT PRIMARY KEY,
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        person_id INTEGER REFERENCES crew_members(person_id) ON DELETE CASCADE,
        department_id INTEGER REFERENCES departments(department_id) ON DELETE CASCADE,
        job_id INTEGER REFERENCES jobs(job_id) ON DELETE CASCADE
    );

    CREATE TABLE movie_collections_junction (
        movie_id INTEGER REFERENCES movies(id) ON DELETE CASCADE,
        collection_id INTEGER REFERENCES movie_collections(collection_id) ON DELETE CASCADE,
        PRIMARY KEY (movie_id, collection_id)
    );

    -- Create indexes for better query performance
    CREATE INDEX idx_movies_title ON movies(title);
    CREATE INDEX idx_movies_release_date ON movies(release_date);
    CREATE INDEX idx_movies_vote_average ON movies(vote_average);

    CREATE INDEX idx_movie_genres_movie_id ON movie_genres(movie_id);
    CREATE INDEX idx_movie_genres_genre_id ON movie_genres(genre_id);

    CREATE INDEX idx_movie_keywords_movie_id ON movie_keywords(movie_id);
    CREATE INDEX idx_movie_keywords_keyword_id ON movie_keywords(keyword_id);

    CREATE INDEX idx_movie_cast_movie_id ON movie_cast(movie_id);
    CREATE INDEX idx_movie_cast_person_id ON movie_cast(person_id);

    CREATE INDEX idx_movie_crew_movie_id ON movie_crew(movie_id);
    CREATE INDEX idx_movie_crew_person_id ON movie_crew(person_id);

    CREATE INDEX idx_ratings_user_id ON ratings(user_id);
    CREATE INDEX idx_ratings_movie_id ON ratings(movie_id);
    """

    cursor.execute(schema_sql)
    conn.commit()
    print("OK: Schema created successfully!")


def parse_json_safely(json_str):
    """Safely parse JSON string, return None on error or if not a list/dict"""
    if not isinstance(json_str, str) or pd.isna(json_str):
        return None
    try:
        # Try standard JSON first
        result = json.loads(json_str)
        # Only return if it's a list or dict (not a number, string, etc.)
        if isinstance(result, (list, dict)):
            return result
        return None
    except (json.JSONDecodeError, TypeError):
        try:
            # Try replacing single quotes with double quotes
            result = json.loads(json_str.replace("'", '"'))
            # Only return if it's a list or dict
            if isinstance(result, (list, dict)):
                return result
            return None
        except (json.JSONDecodeError, TypeError):
            return None


def insert_lookup_data(conn, table_name: str, values: Set[tuple]) -> Dict:
    """Insert unique values into lookup table and return mapping"""
    cursor = conn.cursor()

    if not values:
        return {}

    values_list = list(values)

    # Different handling based on table structure
    if table_name == 'genres':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (genre_id, name) VALUES %s ON CONFLICT (genre_id) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT genre_id, name FROM "{SCHEMA_NAME}".{table_name}')
        return {name: id for id, name in cursor.fetchall()}

    elif table_name == 'keywords':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (keyword_id, name) VALUES %s ON CONFLICT (keyword_id) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT keyword_id, name FROM "{SCHEMA_NAME}".{table_name}')
        return {name: id for id, name in cursor.fetchall()}

    elif table_name == 'production_companies':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (company_id, name) VALUES %s ON CONFLICT (company_id) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT company_id, name FROM "{SCHEMA_NAME}".{table_name}')
        return {name: id for id, name in cursor.fetchall()}

    elif table_name == 'production_countries':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (iso_code, name) VALUES %s ON CONFLICT (iso_code) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT country_id, iso_code FROM "{SCHEMA_NAME}".{table_name}')
        return {iso: id for id, iso in cursor.fetchall()}

    elif table_name == 'spoken_languages':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (iso_code, name) VALUES %s ON CONFLICT (iso_code) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT language_id, iso_code FROM "{SCHEMA_NAME}".{table_name}')
        return {iso: id for id, iso in cursor.fetchall()}

    elif table_name == 'movie_collections':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (collection_id, name, poster_path, backdrop_path) VALUES %s ON CONFLICT (collection_id) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        return {}

    elif table_name == 'cast_members':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (person_id, name, gender, profile_path) VALUES %s ON CONFLICT (person_id) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        return {}

    elif table_name == 'crew_members':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (person_id, name, gender, profile_path) VALUES %s ON CONFLICT (person_id) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        return {}

    elif table_name == 'departments':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (name) VALUES %s ON CONFLICT (name) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT department_id, name FROM "{SCHEMA_NAME}".{table_name}')
        return {name: id for id, name in cursor.fetchall()}

    elif table_name == 'jobs':
        insert_query = f'INSERT INTO "{SCHEMA_NAME}".{table_name} (title) VALUES %s ON CONFLICT (title) DO NOTHING'
        execute_values(cursor, insert_query, values_list)
        conn.commit()
        cursor.execute(f'SELECT job_id, title FROM "{SCHEMA_NAME}".{table_name}')
        return {title: id for id, title in cursor.fetchall()}

    return {}


def process_movies_metadata(conn):
    """Process movies_metadata.csv"""
    csv_path = f'{BASE_PATH}/movies_metadata.csv'
    print("\n" + "="*60)
    print("PROCESSING MOVIES METADATA")
    print("="*60)
    print(f"Reading CSV file: {csv_path}")

    chunk_size = 1000

    # Collections for unique values
    all_genres = set()
    all_companies = set()
    all_countries = set()
    all_languages = set()
    all_collections = set()

    # First pass: collect all unique lookup values
    print("\n[PHASE 1/3] Collecting unique values from CSV...")
    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            for _, row in chunk.iterrows():
                # Genres
                genre_data = parse_json_safely(row.get('genres'))
                if genre_data:
                    for g in genre_data:
                        if g.get('id') and g.get('name'):
                            all_genres.add((int(g['id']), g['name']))

                # Production Companies
                company_data = parse_json_safely(row.get('production_companies'))
                if company_data:
                    for c in company_data:
                        if c.get('id') and c.get('name'):
                            all_companies.add((int(c['id']), c['name']))

                # Production Countries
                country_data = parse_json_safely(row.get('production_countries'))
                if country_data:
                    for c in country_data:
                        iso_code = c.get('iso_3166_1')
                        name = c.get('name')
                        if iso_code and name:
                            all_countries.add((iso_code, name))

                # Spoken Languages
                language_data = parse_json_safely(row.get('spoken_languages'))
                if language_data:
                    for l in language_data:
                        iso_code = l.get('iso_639_1')
                        name = l.get('name')
                        if iso_code and name:
                            all_languages.add((iso_code, name))

                # Collections
                collection_data = parse_json_safely(row.get('belongs_to_collection'))
                if collection_data:
                    coll_id = collection_data.get('id')
                    coll_name = collection_data.get('name')
                    if coll_id and coll_name:
                        all_collections.add((
                            int(coll_id),
                            coll_name,
                            collection_data.get('poster_path'),
                            collection_data.get('backdrop_path')
                        ))

        print(f"  OK: Found {len(all_genres):,} unique genres")
        print(f"  OK: Found {len(all_companies):,} unique production companies")
        print(f"  OK: Found {len(all_countries):,} unique production countries")
        print(f"  OK: Found {len(all_languages):,} unique spoken languages")
        print(f"  OK: Found {len(all_collections):,} unique collections")

    except Exception as e:
        print(f"  ERROR: Error during first pass: {e}")
        raise

    # Insert lookup data and get mappings
    print("\n[PHASE 2/3] Inserting lookup data...")
    try:
        genre_map = insert_lookup_data(conn, 'genres', all_genres)
        print(f"  OK: Inserted genres")

        company_map = insert_lookup_data(conn, 'production_companies', all_companies)
        print(f"  OK: Inserted production companies")

        country_map = insert_lookup_data(conn, 'production_countries', all_countries)
        print(f"  OK: Inserted production countries")

        language_map = insert_lookup_data(conn, 'spoken_languages', all_languages)
        print(f"  OK: Inserted spoken languages")

        insert_lookup_data(conn, 'movie_collections', all_collections)
        print(f"  OK: Inserted collections")

    except Exception as e:
        print(f"  ERROR: Error inserting lookup data: {e}")
        raise

    # Second pass: insert movies and relationships
    print("\n[PHASE 3/3] Inserting movies and relationships...")
    cursor = conn.cursor()

    movies_inserted = 0
    movies_skipped = 0
    errors = []

    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            # Clean release_date
            chunk['release_date'] = pd.to_datetime(chunk['release_date'], errors='coerce').dt.date

            movies_data = []
            movie_genres_data = []
            movie_companies_data = []
            movie_countries_data = []
            movie_languages_data = []
            movie_collections_data = []

            for _, row in chunk.iterrows():
                try:
                    movie_id = row.get('id')
                    if pd.isna(movie_id):
                        movies_skipped += 1
                        continue

                    # Convert to int, handle bad IDs
                    try:
                        movie_id = int(float(movie_id))
                    except (ValueError, TypeError):
                        movies_skipped += 1
                        continue

                    # Prepare movie data
                    movie_record = (
                        movie_id,
                        str(row.get('title', '')) if not pd.isna(row.get('title')) else '',
                        str(row.get('original_title', '')) if not pd.isna(row.get('original_title')) else '',
                        str(row.get('overview', '')) if not pd.isna(row.get('overview')) else None,
                        row.get('release_date') if not pd.isna(row.get('release_date')) else None,
                        int(row.get('runtime')) if not pd.isna(row.get('runtime')) else None,
                        int(row.get('budget')) if not pd.isna(row.get('budget')) else None,
                        int(row.get('revenue')) if not pd.isna(row.get('revenue')) else None,
                        float(row.get('vote_average')) if not pd.isna(row.get('vote_average')) else None,
                        int(row.get('vote_count')) if not pd.isna(row.get('vote_count')) else None,
                        float(row.get('popularity')) if not pd.isna(row.get('popularity')) else None,
                        str(row.get('status')) if not pd.isna(row.get('status')) else None,
                        str(row.get('tagline')) if not pd.isna(row.get('tagline')) else None,
                        str(row.get('homepage')) if not pd.isna(row.get('homepage')) else None,
                        bool(row.get('adult')) if not pd.isna(row.get('adult')) else False,
                        bool(row.get('video')) if not pd.isna(row.get('video')) else False,
                        str(row.get('imdb_id')) if not pd.isna(row.get('imdb_id')) else None,
                        str(row.get('original_language')) if not pd.isna(row.get('original_language')) else None,
                        str(row.get('poster_path')) if not pd.isna(row.get('poster_path')) else None,
                        str(row.get('backdrop_path')) if not pd.isna(row.get('backdrop_path')) else None
                    )
                    movies_data.append(movie_record)

                    # Process relationships
                    genre_data = parse_json_safely(row.get('genres'))
                    if genre_data:
                        for g in genre_data:
                            genre_name = g.get('name')
                            if genre_name and genre_name in genre_map:
                                movie_genres_data.append((movie_id, genre_map[genre_name]))

                    company_data = parse_json_safely(row.get('production_companies'))
                    if company_data:
                        for c in company_data:
                            company_name = c.get('name')
                            if company_name and company_name in company_map:
                                movie_companies_data.append((movie_id, company_map[company_name]))

                    country_data = parse_json_safely(row.get('production_countries'))
                    if country_data:
                        for c in country_data:
                            iso_code = c.get('iso_3166_1')
                            if iso_code and iso_code in country_map:
                                movie_countries_data.append((movie_id, country_map[iso_code]))

                    language_data = parse_json_safely(row.get('spoken_languages'))
                    if language_data:
                        for l in language_data:
                            iso_code = l.get('iso_639_1')
                            if iso_code and iso_code in language_map:
                                movie_languages_data.append((movie_id, language_map[iso_code]))

                    collection_data = parse_json_safely(row.get('belongs_to_collection'))
                    if collection_data:
                        coll_id = collection_data.get('id')
                        if coll_id:
                            movie_collections_data.append((movie_id, int(coll_id)))

                except Exception as e:
                    movies_skipped += 1
                    if len(errors) < 10:
                        errors.append(f"Error processing movie ID {movie_id if 'movie_id' in locals() else 'unknown'}: {e}")
                    continue

            # Insert movies
            if movies_data:
                movies_query = f"""
                    INSERT INTO "{SCHEMA_NAME}".movies
                    (id, title, original_title, overview, release_date, runtime, budget, revenue,
                     vote_average, vote_count, popularity, status, tagline, homepage, adult, video,
                     imdb_id, original_language, poster_path, backdrop_path)
                    VALUES %s
                    ON CONFLICT (id) DO NOTHING
                """
                execute_values(cursor, movies_query, movies_data)

            # Insert relationships
            if movie_genres_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_genres VALUES %s ON CONFLICT DO NOTHING',
                    movie_genres_data)
            if movie_companies_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_production_companies VALUES %s ON CONFLICT DO NOTHING',
                    movie_companies_data)
            if movie_countries_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_production_countries VALUES %s ON CONFLICT DO NOTHING',
                    movie_countries_data)
            if movie_languages_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_spoken_languages VALUES %s ON CONFLICT DO NOTHING',
                    movie_languages_data)
            if movie_collections_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_collections_junction VALUES %s ON CONFLICT DO NOTHING',
                    movie_collections_data)

            conn.commit()
            movies_inserted += len(movies_data)
            print(f"  Progress: {movies_inserted:,} movies inserted...", end='\r')

        print(f"\n  OK: Total movies inserted: {movies_inserted:,}")
        if movies_skipped > 0:
            print(f"  WARNING: Movies skipped: {movies_skipped:,}")
        if errors:
            print(f"  WARNING: Sample errors:")
            for error in errors[:10]:
                print(f"    - {error}")

    except Exception as e:
        print(f"\n  ERROR: Error during movie insertion: {e}")
        raise


def process_credits(conn):
    """Process credits.csv (cast and crew)"""
    csv_path = f'{BASE_PATH}/credits.csv'
    print("\n" + "="*60)
    print("PROCESSING CREDITS")
    print("="*60)
    print(f"Reading CSV file: {csv_path}")

    chunk_size = 1000

    # Collections for unique values
    all_cast = set()
    all_crew = set()
    all_departments = set()
    all_jobs = set()

    # First pass: collect all unique lookup values
    print("\n[PHASE 1/3] Collecting unique values from CSV...")
    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            for _, row in chunk.iterrows():
                # Cast
                cast_data = parse_json_safely(row.get('cast'))
                if cast_data:
                    for c in cast_data:
                        person_id = c.get('id')
                        if person_id:
                            all_cast.add((
                                int(person_id),
                                c.get('name'),
                                c.get('gender'),
                                c.get('profile_path')
                            ))

                # Crew
                crew_data = parse_json_safely(row.get('crew'))
                if crew_data:
                    for c in crew_data:
                        person_id = c.get('id')
                        department = c.get('department')
                        job = c.get('job')

                        if person_id:
                            all_crew.add((
                                int(person_id),
                                c.get('name'),
                                c.get('gender'),
                                c.get('profile_path')
                            ))

                        if department:
                            all_departments.add((department,))

                        if job:
                            all_jobs.add((job,))

        print(f"  OK: Found {len(all_cast):,} unique cast members")
        print(f"  OK: Found {len(all_crew):,} unique crew members")
        print(f"  OK: Found {len(all_departments):,} unique departments")
        print(f"  OK: Found {len(all_jobs):,} unique jobs")

    except Exception as e:
        print(f"  ERROR: Error during first pass: {e}")
        raise

    # Insert lookup data and get mappings
    print("\n[PHASE 2/3] Inserting lookup data...")
    try:
        insert_lookup_data(conn, 'cast_members', all_cast)
        print(f"  OK: Inserted cast members")

        insert_lookup_data(conn, 'crew_members', all_crew)
        print(f"  OK: Inserted crew members")

        department_map = insert_lookup_data(conn, 'departments', all_departments)
        print(f"  OK: Inserted departments")

        job_map = insert_lookup_data(conn, 'jobs', all_jobs)
        print(f"  OK: Inserted jobs")

    except Exception as e:
        print(f"  ERROR: Error inserting lookup data: {e}")
        raise

    # Second pass: insert relationships
    print("\n[PHASE 3/3] Inserting cast and crew relationships...")
    cursor = conn.cursor()

    cast_inserted = 0
    crew_inserted = 0
    errors = []

    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            movie_cast_data = []
            movie_crew_data = []

            for _, row in chunk.iterrows():
                try:
                    movie_id = row.get('id')
                    if pd.isna(movie_id):
                        continue

                    movie_id = int(float(movie_id))

                    # Process cast
                    cast_data = parse_json_safely(row.get('cast'))
                    if cast_data:
                        for c in cast_data:
                            person_id = c.get('id')
                            credit_id = c.get('credit_id')
                            if person_id and credit_id:
                                movie_cast_data.append((
                                    movie_id,
                                    int(person_id),
                                    c.get('character'),
                                    c.get('order'),
                                    credit_id
                                ))

                    # Process crew
                    crew_data = parse_json_safely(row.get('crew'))
                    if crew_data:
                        for c in crew_data:
                            person_id = c.get('id')
                            credit_id = c.get('credit_id')
                            department = c.get('department')
                            job = c.get('job')

                            if person_id and credit_id and department and job:
                                dept_id = department_map.get(department)
                                job_id = job_map.get(job)

                                if dept_id and job_id:
                                    movie_crew_data.append((
                                        credit_id,
                                        movie_id,
                                        int(person_id),
                                        dept_id,
                                        job_id
                                    ))

                except Exception as e:
                    if len(errors) < 10:
                        errors.append(f"Error processing credits for movie ID {movie_id if 'movie_id' in locals() else 'unknown'}: {e}")
                    continue

            # Insert cast relationships
            if movie_cast_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_cast VALUES %s ON CONFLICT DO NOTHING',
                    movie_cast_data)
                cast_inserted += len(movie_cast_data)

            # Insert crew relationships
            if movie_crew_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_crew VALUES %s ON CONFLICT DO NOTHING',
                    movie_crew_data)
                crew_inserted += len(movie_crew_data)

            conn.commit()
            print(f"  Progress: {cast_inserted:,} cast, {crew_inserted:,} crew inserted...", end='\r')

        print(f"\n  OK: Total cast relationships inserted: {cast_inserted:,}")
        print(f"  OK: Total crew relationships inserted: {crew_inserted:,}")
        if errors:
            print(f"  WARNING: Sample errors:")
            for error in errors[:10]:
                print(f"    - {error}")

    except Exception as e:
        print(f"\n  ERROR: Error during credits insertion: {e}")
        raise


def process_keywords(conn):
    """Process keywords.csv"""
    csv_path = f'{BASE_PATH}/keywords.csv'
    print("\n" + "="*60)
    print("PROCESSING KEYWORDS")
    print("="*60)
    print(f"Reading CSV file: {csv_path}")

    chunk_size = 1000

    # Collections for unique values
    all_keywords = set()

    # First pass: collect all unique keywords
    print("\n[PHASE 1/3] Collecting unique values from CSV...")
    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            for _, row in chunk.iterrows():
                keyword_data = parse_json_safely(row.get('keywords'))
                if keyword_data:
                    for k in keyword_data:
                        keyword_id = k.get('id')
                        keyword_name = k.get('name')
                        if keyword_id and keyword_name:
                            all_keywords.add((int(keyword_id), keyword_name))

        print(f"  OK: Found {len(all_keywords):,} unique keywords")

    except Exception as e:
        print(f"  ERROR: Error during first pass: {e}")
        raise

    # Insert lookup data and get mappings
    print("\n[PHASE 2/3] Inserting lookup data...")
    try:
        keyword_map = insert_lookup_data(conn, 'keywords', all_keywords)
        print(f"  OK: Inserted keywords")

    except Exception as e:
        print(f"  ERROR: Error inserting lookup data: {e}")
        raise

    # Second pass: insert relationships
    print("\n[PHASE 3/3] Inserting keyword relationships...")
    cursor = conn.cursor()

    keywords_inserted = 0
    errors = []

    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            movie_keywords_data = []

            for _, row in chunk.iterrows():
                try:
                    movie_id = row.get('id')
                    if pd.isna(movie_id):
                        continue

                    movie_id = int(float(movie_id))

                    keyword_data = parse_json_safely(row.get('keywords'))
                    if keyword_data:
                        for k in keyword_data:
                            keyword_name = k.get('name')
                            if keyword_name and keyword_name in keyword_map:
                                movie_keywords_data.append((movie_id, keyword_map[keyword_name]))

                except Exception as e:
                    if len(errors) < 10:
                        errors.append(f"Error processing keywords for movie ID {movie_id if 'movie_id' in locals() else 'unknown'}: {e}")
                    continue

            # Insert keyword relationships
            if movie_keywords_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_keywords VALUES %s ON CONFLICT DO NOTHING',
                    movie_keywords_data)
                keywords_inserted += len(movie_keywords_data)

            conn.commit()
            print(f"  Progress: {keywords_inserted:,} keyword relationships inserted...", end='\r')

        print(f"\n  OK: Total keyword relationships inserted: {keywords_inserted:,}")
        if errors:
            print(f"  WARNING: Sample errors:")
            for error in errors[:10]:
                print(f"    - {error}")

    except Exception as e:
        print(f"\n  ERROR: Error during keyword insertion: {e}")
        raise


def process_links(conn):
    """Process links.csv"""
    csv_path = f'{BASE_PATH}/links.csv'
    print("\n" + "="*60)
    print("PROCESSING LINKS")
    print("="*60)
    print(f"Reading CSV file: {csv_path}")

    chunk_size = 5000
    links_inserted = 0
    cursor = conn.cursor()

    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size, low_memory=False):
            chunk = chunk.where(pd.notnull(chunk), None)
            links_data = []

            for _, row in chunk.iterrows():
                movie_id = row.get('movieId')
                if not pd.isna(movie_id):
                    links_data.append((
                        int(movie_id),
                        str(row.get('imdbId')) if not pd.isna(row.get('imdbId')) else None,
                        int(row.get('tmdbId')) if not pd.isna(row.get('tmdbId')) else None
                    ))

            if links_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".movie_ids VALUES %s ON CONFLICT DO NOTHING',
                    links_data)
                links_inserted += len(links_data)
                conn.commit()
                print(f"  Progress: {links_inserted:,} links inserted...", end='\r')

        print(f"\n  OK: Total links inserted: {links_inserted:,}")

    except Exception as e:
        print(f"  ERROR: Error during links insertion: {e}")
        raise


def process_ratings(conn):
    """Process ratings.csv (or ratings_small.csv for faster testing)"""
    # Use ratings_small.csv for faster processing, change to ratings.csv for full dataset
    csv_path = f'{BASE_PATH}/ratings_small.csv'
    print("\n" + "="*60)
    print("PROCESSING RATINGS")
    print("="*60)
    print(f"Reading CSV file: {csv_path}")

    chunk_size = 5000

    # First pass: collect unique users
    print("\n[PHASE 1/2] Collecting unique users...")
    all_users = set()
    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            all_users.update(chunk['userId'].unique())

        print(f"  OK: Found {len(all_users):,} unique users")

        # Insert users
        cursor = conn.cursor()
        users_data = [(int(u),) for u in all_users]
        execute_values(cursor,
            f'INSERT INTO "{SCHEMA_NAME}".users VALUES %s ON CONFLICT DO NOTHING',
            users_data)
        conn.commit()
        print(f"  OK: Inserted users")

    except Exception as e:
        print(f"  ERROR: Error during user insertion: {e}")
        raise

    # Second pass: insert ratings
    print("\n[PHASE 2/2] Inserting ratings...")
    cursor = conn.cursor()
    ratings_inserted = 0

    try:
        for chunk in pd.read_csv(csv_path, chunksize=chunk_size):
            ratings_data = []

            for _, row in chunk.iterrows():
                ratings_data.append((
                    int(row['userId']),
                    int(row['movieId']),
                    float(row['rating']),
                    int(row['timestamp'])
                ))

            if ratings_data:
                execute_values(cursor,
                    f'INSERT INTO "{SCHEMA_NAME}".ratings (user_id, movie_id, rating, timestamp) VALUES %s',
                    ratings_data)
                ratings_inserted += len(ratings_data)
                conn.commit()
                print(f"  Progress: {ratings_inserted:,} ratings inserted...", end='\r')

        print(f"\n  OK: Total ratings inserted: {ratings_inserted:,}")

    except Exception as e:
        print(f"  ERROR: Error during ratings insertion: {e}")
        raise


def display_summary(conn):
    """Display database summary statistics"""
    cursor = conn.cursor()

    print("\n" + "="*60)
    print("DATABASE SUMMARY")
    print("="*60)

    tables = [
        ('movies', 'Total Movies'),
        ('genres', 'Total Genres'),
        ('keywords', 'Total Keywords'),
        ('production_companies', 'Total Production Companies'),
        ('production_countries', 'Total Production Countries'),
        ('spoken_languages', 'Total Spoken Languages'),
        ('movie_collections', 'Total Collections'),
        ('cast_members', 'Total Cast Members'),
        ('crew_members', 'Total Crew Members'),
        ('departments', 'Total Departments'),
        ('jobs', 'Total Jobs'),
        ('users', 'Total Users')
    ]

    for table_name, label in tables:
        cursor.execute(f'SELECT COUNT(*) FROM "{SCHEMA_NAME}".{table_name}')
        count = cursor.fetchone()[0]
        print(f"{label:.<45} {count:>10,}")

    print("="*60)

    print("\nRelationship Counts:")
    relationship_tables = [
        ('movie_genres', 'Movie-Genre Links'),
        ('movie_keywords', 'Movie-Keyword Links'),
        ('movie_production_companies', 'Movie-Company Links'),
        ('movie_production_countries', 'Movie-Country Links'),
        ('movie_spoken_languages', 'Movie-Language Links'),
        ('movie_cast', 'Movie-Cast Links'),
        ('movie_crew', 'Movie-Crew Links'),
        ('ratings', 'User Ratings')
    ]

    for table_name, label in relationship_tables:
        cursor.execute(f'SELECT COUNT(*) FROM "{SCHEMA_NAME}".{table_name}')
        count = cursor.fetchone()[0]
        print(f"{label:.<45} {count:>10,}")

    print("="*60)


def main():
    """Main execution function"""
    conn = None
    try:
        print("\n" + "="*60)
        print("MOVIES DATASET - DATABASE CREATION SCRIPT")
        print("="*60)
        print("Connecting to database...")

        conn = psycopg2.connect(**DB_CONFIG)
        print("Connected successfully!")

        # Set the search_path for this connection
        with conn.cursor() as cursor:
            cursor.execute(f'SET search_path TO "{SCHEMA_NAME}";')
        conn.commit()

        # Create schema
        create_schema(conn)

        # Process all CSV files
        process_movies_metadata(conn)
        process_credits(conn)
        process_keywords(conn)
        process_links(conn)
        process_ratings(conn)

        # Display summary
        display_summary(conn)

        print("\n" + "="*60)
        print("DATABASE POPULATION COMPLETED SUCCESSFULLY!")
        print("="*60)
        print(f"\nYou can now query the {SCHEMA_NAME} schema using SQL.")
        print("\nExample query:")
        print(f"""
SELECT m.title, g.name as genre, m.vote_average
FROM "{SCHEMA_NAME}".movies m
JOIN "{SCHEMA_NAME}".movie_genres mg ON m.id = mg.movie_id
JOIN "{SCHEMA_NAME}".genres g ON mg.genre_id = g.id
WHERE m.vote_average > 8.0
ORDER BY m.vote_average DESC
LIMIT 10;
        """)

    except FileNotFoundError as e:
        print(f"\nERROR: CSV file not found: {e}")
        print("Please check the file paths and try again.")
    except psycopg2.Error as e:
        print(f"\nDATABASE ERROR: {e}")
        if conn:
            conn.rollback()
    except Exception as e:
        print(f"\nUNEXPECTED ERROR: {e}")
        if conn:
            conn.rollback()
        raise
    finally:
        if conn:
            conn.close()
            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
