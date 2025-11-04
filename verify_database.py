import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Connect to database
conn = psycopg2.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_DATABASE'),
    port=os.getenv('DB_PORT')
)

cur = conn.cursor()

# Check movies with complete financial data
cur.execute('SELECT COUNT(*) FROM "Movies_dataset".movies WHERE budget > 0 AND revenue > 0')
count = cur.fetchone()[0]
print(f'Movies with complete financial data: {count:,}')

# Get top 5 movies by revenue
cur.execute('''
    SELECT title, budget, revenue
    FROM "Movies_dataset".movies
    WHERE budget > 0 AND revenue > 0
    ORDER BY revenue DESC
    LIMIT 5
''')

print('\nTop 5 movies by revenue:')
for row in cur.fetchall():
    title, budget, revenue = row
    print(f'  {title}: ${revenue:,} (budget: ${budget:,})')

# Check table counts
queries = [
    ('Genres', 'SELECT COUNT(*) FROM "Movies_dataset".genres'),
    ('Cast Members', 'SELECT COUNT(*) FROM "Movies_dataset".cast_members'),
    ('Keywords', 'SELECT COUNT(*) FROM "Movies_dataset".keywords'),
]

print('\nTable Counts:')
for name, query in queries:
    cur.execute(query)
    count = cur.fetchone()[0]
    print(f'  {name}: {count:,}')

conn.close()
print('\nDatabase connection verified successfully!')
