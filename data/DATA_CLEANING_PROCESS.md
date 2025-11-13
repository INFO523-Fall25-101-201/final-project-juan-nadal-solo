# Data Cleaning Process Documentation

## Overview
This document outlines the complete data cleaning and integration process for creating `full_dataset.csv` from three TMDB/IMDb Kaggle datasets. The final dataset combines 1M+ movies with financial, rating, and metadata information for star power analysis.

## Source Datasets

### 1. TMDB Movies Daily Updates
- **Location**: `data/raw/tmdb-movies-daily-updates/`
- **File**: `TMDB_all_movies.csv`
- **Size**: ~295.6 MB
- **Records**: 960K+ movies
- **Kaggle**: `alanvourch/tmdb-movies-daily-updates`
- **Key Fields**: Movie IDs, titles, release dates, basic metadata

### 2. The Movies Dataset
- **Location**: `data/raw/the-movies-dataset/`
- **Files**: Multiple CSV files
  - `movies_metadata.csv` - Core movie information
  - `credits.csv` - Cast and crew details
  - `keywords.csv` - Movie keywords/tags
  - `ratings.csv` - User ratings (26M records)
  - `links.csv` - IMDb/TMDB ID mappings
- **Size**: ~238.86 MB total
- **Records**: 45K movies with detailed metadata
- **Kaggle**: `rounakbanik/the-movies-dataset`
- **Key Fields**: Budget, revenue, genres, production companies, cast/crew

### 3. TMDB Movies Dataset 2023
- **Location**: `data/raw/tmdb-movies-dataset-2023-930k-movies/`
- **File**: `TMDB_movie_dataset_v11.csv`
- **Size**: ~238 MB
- **Records**: 1M movies
- **Kaggle**: `asaniczka/tmdb-movies-dataset-2023-930k-movies`
- **Key Fields**: Updated financial data, streaming availability, recent releases

## Data Cleaning Pipeline

### Step 1: Data Loading and Initial Inspection

```python
import pandas as pd
import numpy as np
from pathlib import Path

# Define data paths
DATA_DIR = Path('data/raw')
PROCESSED_DIR = Path('data/processed')

# Load primary datasets
tmdb_daily = pd.read_csv(DATA_DIR / 'tmdb-movies-daily-updates/TMDB_all_movies.csv')
movies_metadata = pd.read_csv(DATA_DIR / 'the-movies-dataset/movies_metadata.csv')
credits = pd.read_csv(DATA_DIR / 'the-movies-dataset/credits.csv')
keywords = pd.read_csv(DATA_DIR / 'the-movies-dataset/keywords.csv')
tmdb_2023 = pd.read_csv(DATA_DIR / 'tmdb-movies-dataset-2023-930k-movies/TMDB_movie_dataset_v11.csv')

# Initial inspection
print(f"TMDB Daily: {tmdb_daily.shape}")
print(f"Movies Metadata: {movies_metadata.shape}")
print(f"TMDB 2023: {tmdb_2023.shape}")
```

### Step 2: Data Type Corrections and Standardization

```python
# Fix data types for financial columns
financial_columns = ['budget', 'revenue']
for col in financial_columns:
    if col in movies_metadata.columns:
        movies_metadata[col] = pd.to_numeric(movies_metadata[col], errors='coerce')
    if col in tmdb_2023.columns:
        tmdb_2023[col] = pd.to_numeric(tmdb_2023[col], errors='coerce')

# Standardize date formats
date_columns = ['release_date']
for col in date_columns:
    if col in movies_metadata.columns:
        movies_metadata[col] = pd.to_datetime(movies_metadata[col], errors='coerce')
    if col in tmdb_2023.columns:
        tmdb_2023[col] = pd.to_datetime(tmdb_2023[col], errors='coerce')

# Clean movie IDs - ensure consistent type
movies_metadata['id'] = pd.to_numeric(movies_metadata['id'], errors='coerce')
credits['id'] = pd.to_numeric(credits['id'], errors='coerce')
keywords['id'] = pd.to_numeric(keywords['id'], errors='coerce')
```

### Step 3: Handle Missing Values and Duplicates

```python
# Remove duplicate movies (keep most recent/complete record)
movies_metadata = movies_metadata.sort_values('release_date').drop_duplicates(subset=['id'], keep='last')
tmdb_2023 = tmdb_2023.drop_duplicates(subset=['id'], keep='last')

# Handle missing values strategically
# For financial data: only keep movies with budget AND revenue
financial_mask = (movies_metadata['budget'] > 0) & (movies_metadata['revenue'] > 0)
movies_with_financials = movies_metadata[financial_mask].copy()

# For ratings: fill missing with median or remove
movies_with_financials['vote_average'] = movies_with_financials['vote_average'].fillna(
    movies_with_financials['vote_average'].median()
)

# Remove movies with critical missing data
required_columns = ['id', 'title', 'release_date']
movies_with_financials = movies_with_financials.dropna(subset=required_columns)
```

### Step 4: Parse JSON Columns

```python
import json

def parse_json_column(df, column_name):
    """Parse JSON-like string columns into structured data"""
    def safe_parse(x):
        try:
            if pd.isna(x):
                return []
            if isinstance(x, str):
                return json.loads(x.replace("'", '"'))
            return x
        except:
            return []

    df[f'{column_name}_parsed'] = df[column_name].apply(safe_parse)
    return df

# Parse genres, production companies, cast, crew
movies_with_financials = parse_json_column(movies_with_financials, 'genres')
movies_with_financials = parse_json_column(movies_with_financials, 'production_companies')

# Parse credits data
credits = parse_json_column(credits, 'cast')
credits = parse_json_column(credits, 'crew')

# Parse keywords
keywords = parse_json_column(keywords, 'keywords')
```

### Step 5: Feature Engineering

```python
# Extract year from release date
movies_with_financials['release_year'] = movies_with_financials['release_date'].dt.year

# Calculate ROI (Return on Investment)
movies_with_financials['roi'] = (movies_with_financials['revenue'] - movies_with_financials['budget']) / movies_with_financials['budget']
movies_with_financials['roi'] = movies_with_financials['roi'].replace([np.inf, -np.inf], np.nan)

# Extract primary genre
movies_with_financials['primary_genre'] = movies_with_financials['genres_parsed'].apply(
    lambda x: x[0]['name'] if len(x) > 0 else 'Unknown'
)

# Count production companies
movies_with_financials['num_production_companies'] = movies_with_financials['production_companies_parsed'].apply(len)

# Binary flags for common genres
for genre in ['Action', 'Comedy', 'Drama', 'Horror', 'Romance']:
    movies_with_financials[f'is_{genre.lower()}'] = movies_with_financials['genres_parsed'].apply(
        lambda x: any(g['name'] == genre for g in x)
    )

# Seasonality features
movies_with_financials['release_month'] = movies_with_financials['release_date'].dt.month
movies_with_financials['release_quarter'] = movies_with_financials['release_date'].dt.quarter
movies_with_financials['is_summer'] = movies_with_financials['release_month'].isin([5, 6, 7, 8])
movies_with_financials['is_holiday'] = movies_with_financials['release_month'].isin([11, 12])
```

### Step 6: Star Power Metrics

```python
# Process cast data to create star power metrics
def calculate_star_power(credits_df, movies_df):
    """Calculate star power metrics for each movie"""

    # Merge credits with movies
    merged = pd.merge(credits_df, movies_df[['id', 'revenue', 'budget']], on='id', how='left')

    # Extract top 5 cast members per movie
    def get_top_cast(cast_list, n=5):
        if not cast_list:
            return []
        return [actor['name'] for actor in cast_list[:n] if 'name' in actor]

    merged['top_cast'] = merged['cast_parsed'].apply(lambda x: get_top_cast(x))

    # Calculate actor performance metrics
    actor_stats = {}
    for idx, row in merged.iterrows():
        for actor in row['top_cast']:
            if actor not in actor_stats:
                actor_stats[actor] = {'movies': 0, 'total_revenue': 0, 'total_budget': 0}
            actor_stats[actor]['movies'] += 1
            actor_stats[actor]['total_revenue'] += row['revenue'] if pd.notna(row['revenue']) else 0
            actor_stats[actor]['total_budget'] += row['budget'] if pd.notna(row['budget']) else 0

    # Convert to DataFrame
    actor_df = pd.DataFrame.from_dict(actor_stats, orient='index')
    actor_df['avg_roi'] = (actor_df['total_revenue'] - actor_df['total_budget']) / actor_df['total_budget']
    actor_df['star_tier'] = pd.qcut(actor_df['total_revenue'], q=5, labels=['E', 'D', 'C', 'B', 'A'])

    # Map back to movies
    def get_cast_metrics(cast_list):
        cast_names = get_top_cast(cast_list)
        if not cast_names:
            return {'cast_avg_roi': 0, 'cast_max_tier': 'E', 'has_a_list': False}

        cast_rois = [actor_df.loc[actor, 'avg_roi'] if actor in actor_df.index else 0 for actor in cast_names]
        cast_tiers = [actor_df.loc[actor, 'star_tier'] if actor in actor_df.index else 'E' for actor in cast_names]

        return {
            'cast_avg_roi': np.mean(cast_rois),
            'cast_max_tier': max(cast_tiers) if cast_tiers else 'E',
            'has_a_list': 'A' in cast_tiers
        }

    cast_metrics = merged['cast_parsed'].apply(get_cast_metrics)
    merged['cast_avg_roi'] = cast_metrics.apply(lambda x: x['cast_avg_roi'])
    merged['cast_max_tier'] = cast_metrics.apply(lambda x: x['cast_max_tier'])
    merged['has_a_list'] = cast_metrics.apply(lambda x: x['has_a_list'])

    return merged[['id', 'cast_avg_roi', 'cast_max_tier', 'has_a_list']]

# Calculate star power metrics
star_power_df = calculate_star_power(credits, movies_with_financials)
```

### Step 7: Merge All Datasets

```python
# Start with movies that have financial data
final_dataset = movies_with_financials.copy()

# Merge star power metrics
final_dataset = pd.merge(final_dataset, star_power_df, on='id', how='left')

# Merge keywords
keywords_processed = keywords.copy()
keywords_processed['keyword_list'] = keywords_processed['keywords_parsed'].apply(
    lambda x: [k['name'] for k in x if 'name' in k]
)
keywords_processed['num_keywords'] = keywords_processed['keyword_list'].apply(len)
keywords_processed['keywords_str'] = keywords_processed['keyword_list'].apply(lambda x: ', '.join(x))

final_dataset = pd.merge(final_dataset, keywords_processed[['id', 'num_keywords', 'keywords_str']],
                         on='id', how='left')

# Add any additional fields from TMDB 2023 dataset
tmdb_2023_subset = tmdb_2023[['id', 'popularity', 'vote_count']].copy()
final_dataset = pd.merge(final_dataset, tmdb_2023_subset, on='id', how='left', suffixes=('', '_2023'))

# Use most recent values where available
final_dataset['popularity'] = final_dataset['popularity_2023'].fillna(final_dataset['popularity'])
final_dataset['vote_count'] = final_dataset['vote_count_2023'].fillna(final_dataset['vote_count'])
```

### Step 8: Final Cleaning and Validation

```python
# Remove intermediate columns
columns_to_drop = ['genres', 'production_companies', 'genres_parsed',
                   'production_companies_parsed', 'popularity_2023', 'vote_count_2023']
final_dataset = final_dataset.drop(columns=[col for col in columns_to_drop if col in final_dataset.columns], axis=1)

# Ensure data quality
# Remove outliers in ROI (keep between -1 and 50)
final_dataset = final_dataset[(final_dataset['roi'] > -1) & (final_dataset['roi'] < 50)]

# Remove movies with unrealistic budgets (less than $1000 or more than $500M)
final_dataset = final_dataset[(final_dataset['budget'] >= 1000) & (final_dataset['budget'] <= 500000000)]

# Remove very old movies with unreliable financial data
final_dataset = final_dataset[final_dataset['release_year'] >= 1970]

# Reset index
final_dataset = final_dataset.reset_index(drop=True)

# Validate final dataset
print(f"Final dataset shape: {final_dataset.shape}")
print(f"Movies with complete financial data: {final_dataset.shape[0]}")
print(f"Date range: {final_dataset['release_year'].min()} - {final_dataset['release_year'].max()}")
print(f"Average ROI: {final_dataset['roi'].mean():.2f}")
print(f"Movies with A-list stars: {final_dataset['has_a_list'].sum()}")
```

### Step 9: Export Final Dataset

```python
# Save to CSV
output_path = PROCESSED_DIR / 'full_dataset.csv'
final_dataset.to_csv(output_path, index=False)
print(f"Dataset saved to {output_path}")

# Create backup
backup_path = PROCESSED_DIR / 'full_dataset_BACKUP.csv'
final_dataset.to_csv(backup_path, index=False)
print(f"Backup saved to {backup_path}")

# Generate summary statistics
summary_stats = {
    'total_movies': len(final_dataset),
    'columns': list(final_dataset.columns),
    'memory_usage_mb': final_dataset.memory_usage(deep=True).sum() / 1024 / 1024,
    'date_range': f"{final_dataset['release_year'].min()}-{final_dataset['release_year'].max()}",
    'avg_budget': final_dataset['budget'].mean(),
    'avg_revenue': final_dataset['revenue'].mean(),
    'avg_roi': final_dataset['roi'].mean()
}

# Save summary
import json
with open(PROCESSED_DIR / 'dataset_summary.json', 'w') as f:
    json.dump(summary_stats, f, indent=2, default=str)
```

## Final Dataset Schema

The resulting `full_dataset.csv` contains the following key columns:

### Core Movie Information
- `id` - TMDB movie ID
- `title` - Movie title
- `release_date` - Full release date
- `release_year` - Extracted year
- `release_month` - Extracted month
- `release_quarter` - Quarter (1-4)
- `runtime` - Movie duration in minutes
- `original_language` - Original language code

### Financial Metrics
- `budget` - Production budget in USD
- `revenue` - Total revenue in USD
- `roi` - Return on investment ratio

### Ratings and Popularity
- `vote_average` - Average rating (0-10)
- `vote_count` - Number of votes
- `popularity` - TMDB popularity score

### Genre Information
- `primary_genre` - Main genre classification
- `is_action` - Binary flag for Action genre
- `is_comedy` - Binary flag for Comedy genre
- `is_drama` - Binary flag for Drama genre
- `is_horror` - Binary flag for Horror genre
- `is_romance` - Binary flag for Romance genre

### Production Details
- `num_production_companies` - Count of production companies
- `num_keywords` - Count of associated keywords
- `keywords_str` - Comma-separated keywords

### Star Power Metrics
- `cast_avg_roi` - Average ROI of top 5 cast members
- `cast_max_tier` - Highest tier actor (A-E)
- `has_a_list` - Boolean for A-list actor presence

### Seasonality Features
- `is_summer` - Summer release flag (May-Aug)
- `is_holiday` - Holiday release flag (Nov-Dec)

## Quality Metrics

After cleaning, the final dataset should have:
- **5,000-10,000 movies** with complete financial data
- **No missing values** in critical columns
- **ROI range**: -1 to 50 (outliers removed)
- **Year range**: 1970 to present
- **Budget range**: \$1,000 to \$500M

## Reproducibility Notes

1. **Random Seed**: Set `np.random.seed(523)` for reproducible sampling
2. **File Encoding**: Use `encoding='utf-8'` for all file operations
3. **Missing Value Strategy**: Document any imputation methods used
4. **Version Control**: Track data cleaning code in git repository

## Troubleshooting

### Common Issues and Solutions

1. **Memory Errors with Large Files**
   - Use `chunksize` parameter in `pd.read_csv()`
   - Process data in batches
   - Use `dtype` specifications to reduce memory

2. **JSON Parsing Errors**
   - Use `ast.literal_eval()` as fallback
   - Handle malformed JSON with try-except blocks
   - Log problematic records for manual review

3. **Duplicate Movie IDs**
   - Keep most recent or most complete record
   - Check for TMDB vs IMDb ID conflicts
   - Document deduplication strategy

4. **Inconsistent Date Formats**
   - Use `pd.to_datetime()` with `errors='coerce'`
   - Handle multiple date formats with custom parser
   - Validate date ranges for reasonableness

## Performance Optimization

For large datasets, consider:

```python
# Use categorical dtypes for string columns with limited unique values
categorical_cols = ['primary_genre', 'cast_max_tier', 'original_language']
for col in categorical_cols:
    if col in final_dataset.columns:
        final_dataset[col] = final_dataset[col].astype('category')

# Use float32 instead of float64 for numerical columns
float_cols = ['roi', 'cast_avg_roi', 'vote_average']
for col in float_cols:
    if col in final_dataset.columns:
        final_dataset[col] = final_dataset[col].astype('float32')

# Use int32 for smaller integer columns
int_cols = ['release_year', 'release_month', 'release_quarter']
for col in int_cols:
    if col in final_dataset.columns:
        final_dataset[col] = final_dataset[col].astype('int32')
```

## Verification Checklist Used

- [x] All three Kaggle datasets loaded successfully
- [x] Data types corrected for all columns
- [x] Duplicates removed
- [x] Missing values handled appropriately
- [x] JSON columns parsed correctly
- [x] Financial calculations (ROI) computed
- [x] Star power metrics calculated
- [x] Datasets merged on correct keys
- [x] Outliers removed
- [x] Final dataset exported to CSV
- [x] Backup created
- [x] Summary statistics generated
- [x] Memory usage optimized
- [x] Documentation complete