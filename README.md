[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=21451842)



Site URL: https://info523-fall25-101-201.github.io/final-project-juan-nadal-solo/
# Are Movie Stars Worth Their Premiums?
## Predictive Analysis of Movie Financial Performance

**Course:** INFO 523 - Data Mining and Discovery, Fall 2025

**Author:** Juan Nadal

**Institution:** College of Information Science, University of Arizona

---

## Abstract

This project investigates whether high-profile movie stars justify their expensive salaries compared to other factors that drive movie success. Using comprehensive datasets from TMDB and IMDb covering over 1 million movies, we will conduct a multi-phase analysis combining data visualization, predictive modeling, and advanced analytics to determine what truly makes a movie financially successful.

**Primary Research Question:** Are expensive movie stars worth their premiums, or do factors like storytelling, release timing, genre, and streaming platforms drive success more effectively?

**Success Metric:** Return on Investment (ROI) = (Total Revenue - Production Budget) / Production Budget × 100

## Datasets

This analysis will leverage three comprehensive Kaggle datasets totaling approximately 770 MB:

### 1. TMDB Movies Daily Updates
- **Source:** `alanvourch/tmdb-movies-daily-updates`
- **Size:** 960,000+ movies, 295.6 MB
- **Description:** Most current dataset with daily updates from TMDB API
- **Key Features:** Recent movie data, up-to-date financial metrics, current ratings

### 2. The Movies Dataset
- **Source:** `rounakbanik/the-movies-dataset`
- **Size:** 45,000 movies with 26M+ ratings, 238.86 MB
- **Description:** Comprehensive metadata with user ratings
- **Key Features:** Detailed financial data, cast/crew information, user ratings, keywords, production companies

### 3. TMDB Movies Dataset 2023
- **Source:** `asaniczka/tmdb-movies-dataset-2023-930k-movies`
- **Size:** 1 million movies, 238 MB
- **Description:** Comprehensive historical movie database through 2023
- **Key Features:** Broad historical coverage, genre classifications, release dates

### Dataset Rationale

These three datasets provide complementary perspectives: recency (daily updates), depth (ratings and detailed metadata), and breadth (1M+ movies across decades). Together, they enable robust analysis of star power versus other success factors while ensuring data quality through cross-validation and triangulation.


## Data Processing Pipeline

### Data Quality Challenges

The raw Kaggle datasets present several preprocessing challenges:

- **Nested JSON structures:** Many CSV columns contain JSON objects (cast lists, genres, production companies)
- **Comma-separated values within cells:** Individual fields contain comma-delimited lists that conflict with CSV parsing
- **Inconsistent data types:** Mixed formats for dates, currencies, and categorical variables
- **Missing values:** Sparse data for older films and international releases
- **Denormalized structure:** Redundant information across datasets requiring careful joins and deduplication

### ETL Process

To address these challenges, the project will implement a structured Extract-Transform-Load (ETL) pipeline:

**1. Extract**
- Download raw CSV files from Kaggle (via kagglehub or Kaggle API)
- Store original files in `/data/raw` directory (gitignored)

**2. Transform**
Custom Python scripts (`/scripts/data_cleaning/`) will handle:
- **JSON parsing:** Extract nested JSON into relational tables (separate movies, cast, genres tables)
- **Data normalization:** Split denormalized data into proper relational schema
- **Type conversion:** Standardize dates, currencies, and categorical encodings
- **Deduplication:** Identify and merge duplicate movie entries across datasets
- **Validation:** Check for logical inconsistencies (e.g., revenue < budget, invalid dates)

**3. Load**
- Import cleaned data into PostgreSQL database
- Create normalized schema with foreign key relationships
- Build indexes on frequently queried columns (movie_id, release_date, genre, etc.)
- Generate materialized views for complex aggregations

### Database Architecture

PostgreSQL will serve as the central data platform for all analysis:

```
Database: movie_analysis

Planned Tables:
├── movies              # Core movie metadata (title, release_date, budget, revenue, runtime)
├── cast                # Actor information and roles
├── crew                # Directors, producers, writers
├── genres              # Movie genre classifications
├── production_companies
├── ratings             # User ratings (TMDB, IMDb)
└── platforms           # Streaming availability (Netflix, Apple TV, YouTube)
```

**Benefits of PostgreSQL Approach:**
- **Query Performance:** Fast aggregations over 1M+ rows using indexes
- **Data Integrity:** Foreign key constraints ensure referential integrity
- **Reproducibility:** SQL queries are version-controlled and auditable
- **Scalability:** Handles complex multi-table joins efficiently
- **Integration:** Python analysis connects via psycopg2 or SQLAlchemy

### Analysis Workflow

```
Raw CSV Files → Python Cleaning Scripts → PostgreSQL Database → Python Analysis (Jupyter) → Quarto Reports
```

All statistical analysis, machine learning models, and visualizations will query the PostgreSQL database using Python libraries (pandas, SQLAlchemy, psycopg2, scikit-learn).

## Research Questions

### Primary Question
**Do movies with high-paid stars generate better returns than movies focusing on other success factors?**

### Secondary Questions
1. Which factors most reliably predict movie success in the modern era?
2. Do sequels and franchises outperform original films financially?
3. Is there an optimal budget range that maximizes ROI?
4. Does release timing (month, competitive landscape) significantly impact financial outcomes?

## Methodology: 5-Phase Analysis Plan

### Phase 1: Exploratory Data Visualization

**Objective:** Understand patterns, distributions, and relationships in the movie dataset through visual exploration.

**Planned Visualizations:**
1. Genre Performance Analysis (revenue vs ROI comparison)
2. Seasonality Analysis (release timing impact on box office)
3. Star Power Analysis (top actors by average ROI)
4. Budget vs Revenue Scatter Plot (risk/reward relationship)
5. ROI Distribution Histogram (profitability patterns)
6. Yearly Trends (historical budget and revenue evolution)

**Tools:** Python (matplotlib, seaborn, plotly), SQL queries for data aggregation

**Expected Outcomes:**
- Visual evidence of which genres, release months, and content types drive ROI
- Identification of optimal release timing strategies
- Quantification of "star power" effect on financial performance
- Understanding of franchise economics vs standalone film risks

---

### Phase 2: Predictive Modeling

**Objective:** Build machine learning models to predict ROI and identify the most important success factors.

**Approach:**
- **Feature Engineering:** Create 50+ features from database (numerical, categorical, derived)
  - Numerical: budget, release_month, release_year, vote_average, runtime
  - Categorical: genres (one-hot encoded), franchise_status, top_actor_presence
  - Derived: budget_log, budget_category, cast_avg_roi, competition_index

- **Models to Train:**
  - Linear Regression (baseline interpretability)
  - Ridge/Lasso Regression (regularization for feature selection)
  - Random Forest Regressor (handles non-linearity and feature interactions)
  - Gradient Boosting (XGBoost or LightGBM for high accuracy)

- **Evaluation Metrics:**
  - R² (coefficient of determination) - target: >50%
  - RMSE (root mean squared error)
  - MAE (mean absolute error)
  - 5-fold cross-validation for robustness

**Deliverables:**
- Trained model files (.pkl) for each algorithm
- Performance comparison report (R², RMSE, MAE)
- Feature importance visualization (top 15-20 ROI drivers)
- Prediction tool for new movie concepts
- SHAP values for model interpretation

**Hypotheses to Test:**
- H1: Release month has significant impact on ROI (seasonality effect)
- H2: Budget has diminishing returns (non-linear relationship)
- H3: Franchise status affects revenue positively but ROI negatively
- H4: Actor historical ROI predicts current film's ROI
- H5: Genre interactions exist (hybrid genres perform differently)

---

### Phase 3: Data Export for Business Intelligence

**Objective:** Export cleaned, aggregated data to CSV files for Tableau/Excel dashboards and stakeholder reporting.

**Planned Exports:**
1. movies_roi_analysis.csv - Complete movie list with ROI metrics
2. genre_performance.csv - Aggregated genre statistics
3. actor_star_power.csv - Actor rankings by ROI
4. release_seasonality.csv - Month-by-month revenue and ROI patterns
5. franchise_comparison.csv - Franchise vs standalone metrics
6. yearly_trends.csv - Historical trends in budget, revenue, release volume


**Use Cases:**
- Tableau/Power BI dashboard creation
- Executive presentation slides with pivot tables
- Collaboration with non-technical stakeholders
- Academic paper appendices

---

### Phase 4: Custom Query Analysis

**Objective:** Answer specific research questions with targeted SQL queries.

**Planned Analyses:**

1. **Sequel Performance Analysis**
   - Question: Do sequels outperform original films financially?
   - Approach: Classify films using title patterns and collections

2. **Director Impact Study**
   - Question: Which directors consistently deliver high ROI?
   - Approach: Analyze director track records (minimum 3 films)

3. **Optimal Budget Sweet Spot**
   - Question: Is there an optimal budget range that maximizes ROI?
   - Approach: Analyze ROI by budget deciles

4. **Genre Combination Analysis**
   - Question: Are hybrid genres more profitable than pure genres?
   - Approach: Compare single-genre vs multi-genre films

**Deliverables:**
- Custom SQL query scripts (.sql files)
- Results documentation with findings
- Statistical significance testing (p-values, confidence intervals)
- Visualizations of query outputs
- Executive summary answering each question

---

### Phase 5: Advanced Deep Dive Analysis

**Objective:** Conduct advanced analytics using graph theory, network analysis, and machine learning techniques.

**Planned Components:**

**5.1 Actor Collaboration Network Analysis**
- Build graph where nodes = actors, edges = collaborations
- Calculate centrality metrics (betweenness, degree, eigenvector, PageRank)
- Community detection (Louvain algorithm)
- Visualize force-directed network graphs
- Identify "connector" actors who bridge different communities

**5.2 Competitive Landscape Analysis**
- Define competition as movies released within same week + overlapping genres
- Calculate competition intensity scores
- Measure market saturation by genre and time period
- Analyze first-mover advantage and counterprogramming strategies

**5.3 Criteria for "Hidden Gems":**
- Budget < $5M AND ROI > 1000%
- No A-list actors AND revenue > $50M
- High critical reception (vote_average > 7) AND budget < $10M

**5.4 Time Series Forecasting**
- Model historical trends in average budget, revenue, ROI
- Identify structural breaks (e.g., streaming era impact)


**Deliverables:**
- Interactive actor network graph (HTML via Plotly/NetworkX)
- Keyword theme report with topic distributions
- Competitive landscape dashboard
- Hidden gems case study document
- Time series forecast with 5-year projections
- Deep dive Jupyter notebook with all analyses

## Key Variables

### Star Power Metrics
- Cast prominence and billing order (cast_order)
- Actor historical average ROI (cast_avg_roi)
- Previous box office performance
- Awards and nominations
- Number of collaborations (network centrality)

### Financial Variables
- Production budget
- Total revenue (domestic + international)
- ROI (calculated)
- Profit (revenue - budget)
- Budget category (low/medium/high)

### Content Variables
- Genre classification (18 genres, one-hot encoded)
- Keyword themes (extracted from plot keywords)
- Runtime (minutes)
- Franchise/sequel status
- Production companies

### Temporal Variables
- Release date
- Release month (1-12)
- Release year
- Day of week
- Holiday proximity
- Competition index (same-week releases)

### Quality Metrics
- TMDB vote average (1-10 scale)
- TMDB vote count (popularity proxy)
- IMDb ratings (when available)
- Critical reception scores

## Expected Outcomes

### Quantitative Results
- Predictive model achieving 75%+ R² for ROI forecasting
- Ranked list of feature importance (identify top 5 success drivers)
- Statistical significance testing for all hypotheses

### Qualitative Insights
- Evidence-based answer to primary research question
- Identification of optimal production strategies (budget, timing, casting)
- Discovery of counterintuitive patterns in movie economics
- Actionable recommendations for studio decision-makers
- Understanding of industry evolution and future trends

### Deliverables
- Quarto website with full analysis and interactive visualizations
- 500 - 1000 word write-up with methodology and findings
- 5-minute presentation summarizing key insights
- 10+ CSV exports for stakeholder dashboards
- Reproducible code repository with documentation


## Technologies

### Database
- **PostgreSQL 18:** Primary data storage and querying platform
- **psycopg2:** Python database adapter
- **SQLAlchemy:** ORM for complex queries

### Programming Languages
- **Python 3.11:** Primary analysis language
- **SQL:** Database queries and transformations
- **Markdown:** Documentation

### Python Libraries

**Data Processing:**
- pandas (DataFrames and data manipulation)
- numpy (numerical computing)
- json (parsing nested JSON in CSV files)

**Machine Learning:**
- scikit-learn (Random Forest, Gradient Boosting, preprocessing, cross-validation)
- xgboost (gradient boosting implementation)
- lightgbm (alternative gradient boosting)

**Model Interpretation:**
- shap (SHAP values for feature importance)
- eli5 (model explanation)

**Visualization:**
- matplotlib (static charts)
- seaborn (statistical visualizations)
- plotly (interactive visualizations)

**Advanced Analysis:**
- networkx (graph theory and network analysis)
- nltk, spacy (NLP for keyword analysis)
- statsmodels (time series analysis)


**Data Acquisition:**
- kagglehub (Kaggle dataset downloads)
- Kaggle API (alternative download method)

### Publishing and Deployment
- **Quarto:** Literate programming and website generation
- **GitHub Pages:** Automated deployment via GitHub Actions
- **RevealJS:** Presentation slides (via Quarto)


### Website Publishing

```bash
# Preview website with live reload
quarto preview

# Render entire site
quarto render

# Render specific document
quarto render index.qmd
quarto render presentation.qmd

# Render presentation to PDF
quarto render presentation.qmd --to pdf
```

### GitHub Deployment

The project auto-deploys to GitHub Pages via `.github/workflows/publish-site.yml`:
1. Push to `main` branch triggers the action
2. Installs dependencies, Quarto
3. Renders the site with `quarto render`
4. Deploys output to `gh-pages` branch

**Important:** Test locally with `quarto preview` before pushing.


## References and Data Sources

**Datasets:**
- TMDB API Documentation: https://developers.themoviedb.org/3
- Kaggle Dataset 1: https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates
- Kaggle Dataset 2: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
- Kaggle Dataset 3: https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies

**Methodology References:**
- Feature importance analysis: SHAP (Lundberg & Lee, 2017)
- Network analysis: Newman, M.E.J. (2010). Networks: An Introduction
- Time series forecasting: Taylor & Letham (2018). Forecasting at Scale (Prophet)

**Related Research:**
- Movie success prediction: Sharda & Delen (2006)
- Star power analysis: Elberse (2007)
- Box office forecasting: Basuroy et al. (2003)


---

#### Disclosure:
Derived from the original data viz course by Mine Çetinkaya-Rundel @ Duke University
