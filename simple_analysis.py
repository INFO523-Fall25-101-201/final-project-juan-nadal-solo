"""
Movie Financial Performance Analysis - Simple Version
Connects to local PostgreSQL and runs exploratory analysis
"""
import psycopg2
from dotenv import load_dotenv
import os


# Load environment variables
load_dotenv()

# Database connection parameters
DB_PARAMS = {
    'host': os.getenv('DB_HOST'),
    'user': os.getenv('DB_USER'),
    'database': os.getenv('DB_DATABASE'),
    'password': os.getenv('DB_PASSWORD'),
    'port': os.getenv('DB_PORT')
}

def connect_db():
    """Create database connection"""
    try:
        conn = psycopg2.connect(**DB_PARAMS)
        print(f"[OK] Connected to database: {DB_PARAMS['database']}")
        return conn
    except Exception as e:
        print(f"[ERROR] Connection failed: {e}")
        return None

def run_query(conn, query, description):
    """Execute query and print results"""
    print(f"\n{'='*80}")
    print(f"Query: {description}")
    print(f"{'='*80}")
    try:
        cursor = conn.cursor()
        cursor.execute(query)

        # Get column names
        colnames = [desc[0] for desc in cursor.description]
        print("\t".join(colnames))
        print("-" * 80)

        # Fetch and print rows
        rows = cursor.fetchall()
        for row in rows:
            print("\t".join(str(val) if val is not None else "NULL" for val in row))

        print(f"\nRows returned: {len(rows)}")
        cursor.close()
        return rows
    except Exception as e:
        print(f"[ERROR] Query failed: {e}")
        return None

def main():
    conn = connect_db()
    if not conn:
        return

    # Query 1: Check available schemas
    query_schemas = """
    SELECT schema_name
    FROM information_schema.schemata
    WHERE schema_name NOT IN ('pg_catalog', 'information_schema')
    ORDER BY schema_name;
    """
    run_query(conn, query_schemas, "Available Schemas")

    # Query 2: Check Movies_dataset schema tables
    query_tables = """
    SELECT table_name
    FROM information_schema.tables
    WHERE table_schema = 'Movies_dataset'
    ORDER BY table_name;
    """
    run_query(conn, query_tables, "Tables in Movies_dataset Schema")

    # Query 3: Data completeness check
    query_completeness = """
    SELECT
        COUNT(*) as total_movies,
        COUNT(budget) as movies_with_budget,
        COUNT(revenue) as movies_with_revenue,
        COUNT(CASE WHEN budget > 0 AND revenue > 0 THEN 1 END) as movies_with_both_financial,
        COUNT(release_date) as movies_with_release_date,
        ROUND(COUNT(CASE WHEN budget > 0 AND revenue > 0 THEN 1 END)::NUMERIC /
              COUNT(*)::NUMERIC * 100, 2) as pct_complete_financial
    FROM "Movies_dataset".movies;
    """
    run_query(conn, query_completeness, "Data Completeness Assessment")

    # Query 4: ROI distribution (top 20 movies)
    query_roi = """
    SELECT
        title,
        release_date,
        budget,
        revenue,
        revenue - budget as profit,
        ROUND(((revenue - budget)::NUMERIC / budget * 100)::NUMERIC, 2) as roi_percentage
    FROM "Movies_dataset".movies
    WHERE budget > 0 AND revenue > 0
    ORDER BY roi_percentage DESC
    LIMIT 20;
    """
    run_query(conn, query_roi, "Top 20 Movies by ROI")

    # Query 5: Genre performance analysis
    query_genres = """
    SELECT
        g.name as genre,
        COUNT(DISTINCT m.id) as movie_count,
        ROUND(AVG((m.revenue - m.budget)::NUMERIC / NULLIF(m.budget, 0) * 100)::NUMERIC, 2) as avg_roi,
        ROUND(AVG(m.vote_average)::NUMERIC, 2) as avg_rating,
        ROUND(AVG(m.budget)::NUMERIC, 0) as avg_budget,
        ROUND(AVG(m.revenue)::NUMERIC, 0) as avg_revenue
    FROM "Movies_dataset".genres g
    JOIN "Movies_dataset".movie_genres mg ON g.genre_id = mg.genre_id
    JOIN "Movies_dataset".movies m ON mg.movie_id = m.id
    WHERE m.budget > 0 AND m.revenue > 0
    GROUP BY g.genre_id, g.name
    HAVING COUNT(DISTINCT m.id) >= 10
    ORDER BY avg_roi DESC;
    """
    run_query(conn, query_genres, "Genre Performance Analysis")

    # Query 6: Release month seasonality
    query_seasonality = """
    SELECT
        EXTRACT(MONTH FROM release_date) as release_month,
        TO_CHAR(release_date, 'Month') as month_name,
        COUNT(*) as movie_count,
        ROUND(AVG((revenue - budget)::NUMERIC / NULLIF(budget, 0) * 100)::NUMERIC, 2) as avg_roi,
        ROUND(AVG(revenue)::NUMERIC, 0) as avg_revenue
    FROM "Movies_dataset".movies
    WHERE release_date IS NOT NULL
    AND budget > 0
    AND revenue > 0
    GROUP BY EXTRACT(MONTH FROM release_date), TO_CHAR(release_date, 'Month')
    ORDER BY release_month;
    """
    run_query(conn, query_seasonality, "Release Month Seasonality Analysis")

    # Query 7: Top actors by average ROI
    query_actors = """
    SELECT
        cm.name as actor_name,
        COUNT(DISTINCT mc.movie_id) as movie_count,
        ROUND(AVG((m.revenue - m.budget)::NUMERIC / NULLIF(m.budget, 0) * 100)::NUMERIC, 2) as avg_roi,
        ROUND(SUM(m.revenue)::NUMERIC, 0) as total_box_office
    FROM "Movies_dataset".cast_members cm
    JOIN "Movies_dataset".movie_cast mc ON cm.person_id = mc.person_id
    JOIN "Movies_dataset".movies m ON mc.movie_id = m.id
    WHERE mc.cast_order <= 3
    AND m.budget > 0
    AND m.revenue > 0
    GROUP BY cm.person_id, cm.name
    HAVING COUNT(DISTINCT mc.movie_id) >= 5
    ORDER BY avg_roi DESC
    LIMIT 20;
    """
    run_query(conn, query_actors, "Top 20 Actors by Average ROI (Star Power)")

    # Query 8: Franchise vs Standalone
    query_franchise = """
    SELECT
        CASE WHEN mc.collection_id IS NOT NULL THEN 'Franchise' ELSE 'Standalone' END as movie_type,
        COUNT(*) as movie_count,
        ROUND(AVG((m.revenue - m.budget)::NUMERIC / NULLIF(m.budget, 0) * 100)::NUMERIC, 2) as avg_roi,
        ROUND(AVG(m.budget)::NUMERIC, 0) as avg_budget,
        ROUND(AVG(m.revenue)::NUMERIC, 0) as avg_revenue
    FROM "Movies_dataset".movies m
    LEFT JOIN "Movies_dataset".movie_collections_junction mc ON m.id = mc.movie_id
    WHERE m.budget > 0 AND m.revenue > 0
    GROUP BY CASE WHEN mc.collection_id IS NOT NULL THEN 'Franchise' ELSE 'Standalone' END;
    """
    run_query(conn, query_franchise, "Franchise vs Standalone Performance")

    conn.close()
    print("\n" + "="*80)
    print("Analysis complete! Connection closed.")

if __name__ == "__main__":
    main()
