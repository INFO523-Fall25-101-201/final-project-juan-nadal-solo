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
  - Numerical: budget, release_month, release_year
  - Categorical: genres, franchise_status, top_actor_presence
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



### Phase 3: Advanced Deep Dive Analysis

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
