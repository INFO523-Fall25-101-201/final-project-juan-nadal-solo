# Data

- **full_dataset.csv**: Processed movie dataset combining three Kaggle sources (TMDB Movies Daily Updates, The Movies Dataset, TMDB Movies Dataset 2023) with 5,311 movies containing complete financial and cast data from 1915-2017. Filtered for budget >= $1,000, revenue > 0, and runtime >= 40 minutes.

- **feature_importance.csv**: XGBoost feature importance rankings showing cast_avg_roi accounts for 85.05% of ROI prediction importance.

- **model_comparison.csv**: Performance metrics for 6 machine learning models (Linear, Ridge, Lasso, Random Forest, Gradient Boosting, XGBoost) with XGBoost achieving 93.2% R².

- **xgboost_improved_cap.pkl**: Trained XGBoost model for ROI prediction (located in data/models/).

- **scaler_improved_cap.pkl**: StandardScaler for feature normalization (located in data/models/).

# Codebook for full_dataset Dataset

## Variable Names and Descriptions:

### Financial Metrics
- **budget**: Production budget (USD)
- **revenue**: Total box office revenue (USD)
- **roi**: Return on Investment = (revenue - budget) / budget × 100 (capped at 99th percentile: 6,620.4%)
- **budget_log**: Log-transformed budget for modeling

### Star Power Metrics
- **cast_avg_roi**: Average historical ROI of top 3 billed actors (0 indicates no historical data available)
- **star_tier**: Classification based on cast_avg_roi (Unknown/C-list, B-list, A-list, Superstar)
- **is_alist**: Binary indicator for A-list/Superstar status (cast_avg_roi >= 150%)

### Temporal Features
- **release_date**: Original release date (YYYY-MM-DD format)
- **release_year**: Year of release (1915-2017)
- **release_month**: Month of release (1-12)
- **release_quarter**: Quarter of release (1-4)
- **release_day_of_week**: Day of week (0=Monday, 6=Sunday)

### Quality Metrics
- **vote_average**: TMDB average rating (0-10 scale)
- **vote_count**: Number of TMDB votes
- **vote_count_log**: Log-transformed vote count
- **runtime**: Movie duration (minutes)

### Content Features
- **title**: Movie title
- **original_language**: ISO 639-1 language code
- **franchise_status**: Binary indicator for franchise membership (1) or standalone (0)

### Genre Indicators
- **genre_Action**: Action genre (1=present, 0=absent)
- **genre_Adventure**: Adventure genre (1=present, 0=absent)
- **genre_Animation**: Animation genre (1=present, 0=absent)
- **genre_Comedy**: Comedy genre (1=present, 0=absent)
- **genre_Crime**: Crime genre (1=present, 0=absent)
- **genre_Documentary**: Documentary genre (1=present, 0=absent)
- **genre_Drama**: Drama genre (1=present, 0=absent)
- **genre_Family**: Family genre (1=present, 0=absent)
- **genre_Fantasy**: Fantasy genre (1=present, 0=absent)
- **genre_History**: History genre (1=present, 0=absent)
- **genre_Horror**: Horror genre (1=present, 0=absent)
- **genre_Music**: Music genre (1=present, 0=absent)
- **genre_Mystery**: Mystery genre (1=present, 0=absent)
- **genre_Romance**: Romance genre (1=present, 0=absent)
- **genre_Science Fiction**: Science Fiction genre (1=present, 0=absent)
- **genre_Thriller**: Thriller genre (1=present, 0=absent)
- **genre_War**: War genre (1=present, 0=absent)
- **genre_Western**: Western genre (1=present, 0=absent)

## Data Types:

- **budget**: float64
- **revenue**: float64
- **roi**: float64
- **budget_log**: float64
- **cast_avg_roi**: float64
- **vote_average**: float64
- **vote_count**: int64
- **vote_count_log**: float64
- **runtime**: int64
- **release_year**: int64
- **release_month**: int64
- **release_quarter**: int64
- **release_day_of_week**: int64
- **is_alist**: int64
- **franchise_status**: int64
- **title**: object
- **release_date**: object
- **original_language**: object
- **star_tier**: category
- **All genre indicators**: int64