[![Open in Codespaces](https://classroom.github.com/assets/launch-codespace-2972f46106e565e64193e422d61a12cf1da4916b45550586e14ef0a7c637dd04.svg)](https://classroom.github.com/open-in-codespaces?assignment_repo_id=21451842)

Site URL: https://info523-fall25-101-201.github.io/final-project-juan-nadal-solo/

# Are Movie Stars Worth Their Premiums?
## Predictive Analysis of Movie Financial Performance

**Course:** INFO 523 - Data Mining and Discovery, Fall 2025

**Author:** Juan Nadal

**Institution:** College of Information Science, University of Arizona

---

## Abstract

This project investigates whether high-profile movie stars justify their expensive salaries compared to other factors that drive movie success. Using comprehensive datasets from TMDB and IMDb, I analyzed 5,311 films spanning 1915-2017 to determine what truly makes a movie financially successful.

**Primary Research Question:** Are expensive movie stars worth their premiums, or do factors like budget discipline, release timing, and franchise status drive success more effectively?

**Key Finding:** Star power accounts for only 1.12% of ROI prediction importance (Rank #29 of 51 features), while budget discipline accounts for 30.4%.

**Success Metric:** Return on Investment (ROI) = (Revenue - Budget) / Budget x 100

---

## Key Results

| Metric | Value |
|--------|-------|
| Movies analyzed | 5,311 |
| Total revenue | $485.6 billion |
| Total budget | $167.2 billion |
| Features engineered | 60 |
| Best model R-squared | 33.7% (XGBoost) |
| Star power correlation | r = 0.078 (weak) |
| Star power importance | 1.12% (Rank #29) |
| Budget importance | 30.4% (Rank #1) |

**Conclusion:** Stars are NOT worth their premiums based on ROI data. Budget discipline is 27x more important than star power for predicting financial returns.

---

## Datasets

Three Kaggle datasets were merged and processed:

### 1. TMDB Movies Daily Updates
- **Source:** `alanvourch/tmdb-movies-daily-updates`
- **Description:** Current dataset with daily updates from TMDB API

### 2. The Movies Dataset
- **Source:** `rounakbanik/the-movies-dataset`
- **Description:** Comprehensive metadata with user ratings, cast/crew information

### 3. TMDB Movies Dataset 2023
- **Source:** `asaniczka/tmdb-movies-dataset-2023-930k-movies`
- **Description:** Historical movie database through 2023

### Data Quality Challenges Addressed
- Budget errors: Removed 52 movies with budget < $1,000
- ROI capping: 99th percentile at 6,620.4%
- Missing cast data: Only 640 movies (12%) have complete actor ROI history
- Final clean dataset: 5,311 movies

---

## Methodology

### Statistical Analysis
- **Correlation Analysis:** Measured linear relationships between features and ROI
- **ANOVA:** Compared mean ROI across star tiers (Superstar, A-list, B-list, Unknown)
- **T-test:** Direct comparison of A-list/Superstar vs. other films
- **Effect Sizes:** Cohen's d and eta-squared for practical significance

### Machine Learning
Six regression models trained to predict ROI:

| Model | R-squared Score |
|-------|-----------------|
| XGBoost | 33.7% (Best) |
| Lasso Regression | 31.5% |
| Linear Regression | 31.5% |
| Ridge Regression | 31.5% |
| Gradient Boosting | 30.3% |
| Random Forest | 29.9% |

**Note:** Revenue was excluded from features to prevent target leakage. Original models with revenue achieved 93.2% R-squared but were invalid.

---

## Key Variables

### Target Variable
- **ROI:** (Revenue - Budget) / Budget x 100

### Star Power Metrics
- `cast_avg_roi`: Average historical ROI of cast members
- `star_tier`: Superstar, A-list, B-list, or Unknown/C-list
- `num_top_actors`: Count of high-performing actors in cast

### Financial Variables
- `budget`: Production budget
- `budget_micro`: Binary flag for micro-budget films (< $1M)
- `revenue`: Box office earnings

### Content Variables
- `vote_average`: Audience rating (0-10)
- `vote_count`: Number of ratings (popularity proxy)
- `runtime`: Film length in minutes
- `is_franchise`: Whether part of a franchise
- Genre flags (18 one-hot encoded genres)

### Temporal Variables
- `release_month`: Month of release (1-12)
- `release_year`: Year of release

---

## Statistical Findings

### Correlation with ROI
| Feature | Correlation | Interpretation |
|---------|-------------|----------------|
| vote_average | 0.171 | Strongest positive |
| revenue | 0.146 | Positive but circular |
| budget | -0.135 | Negative (higher budgets reduce ROI) |
| cast_avg_roi | 0.078 | Very weak |
| runtime | -0.029 | Negligible |

### T-Test Results
- **Top-tier stars (A-list + Superstar):** Mean ROI 458.2% (n=293)
- **All other films:** Mean ROI 337.2% (n=5,018)
- **Difference:** +121.0% ROI
- **P-value:** 0.024 (statistically significant)
- **Cohen's d:** 0.14 (negligible effect size)

The statistically significant p-value is misleading. The negligible effect size (d=0.14) indicates distributions overlap heavily, meaning stars don't consistently outperform.

### Feature Importance (Top 5)
1. budget_micro: 30.4%
2. runtime_long: 8.2%
3. vote_count: 5.3%
4. num_top_actors: 5.0%
5. is_franchise: 4.7%

Star power (cast_avg_roi): 1.12% - Rank #29 of 51

---

## Technologies Used

### Programming
- **Python 3.11:** Primary analysis language
- **Jupyter Notebooks:** Data preparation and analysis

### Python Libraries
- pandas, numpy (data processing)
- matplotlib, seaborn (visualization)
- scikit-learn (machine learning)
- xgboost (gradient boosting)
- scipy (statistical tests)

### Publishing
- **Quarto:** Literate programming and website generation
- **GitHub Pages:** Automated deployment via GitHub Actions
- **RevealJS:** Presentation slides

---

## Project Structure

```
final-project-juan-nadal-solo/
├── index.qmd                 # Main analysis and writeup
├── presentation.qmd          # RevealJS presentation slides
├── about.qmd                 # Author information
├── _quarto.yml               # Quarto configuration
├── data/
│   ├── processed/            # Cleaned datasets
│   │   ├── full_dataset.csv
│   │   ├── feature_importance_fixed.csv
│   │   └── model_comparison_fixed.csv
│   └── customtheming.scss    # Presentation theme
├── notebooks/
│   ├── 01_data_preparation.ipynb
│   └── 02_star_power_analysis.ipynb
├── images/
│   └── analysis/             # Generated visualizations
└── _freeze/                  # Quarto computation cache
```

---

## Limitations

- **Limited cast data:** Only 12% of movies (640) have complete actor ROI history
- **Modest model accuracy:** Best R-squared = 33.7% (66% of variance unexplained)
- **Pre-streaming era:** Data spans 1915-2017, predating Netflix dominance
- **No marketing data:** Marketing spend not included in analysis
- **Correlation vs. causation:** Statistical relationships don't prove causation

---

## Future Research

- Add streaming platform data (Netflix, Disney+, etc.)
- Include social media influence metrics
- Test with 2020-2025 releases
- Analyze marketing spend impact
- Expand cast data coverage

---

## References

**Datasets:**
- Kaggle Dataset 1: https://www.kaggle.com/datasets/alanvourch/tmdb-movies-daily-updates
- Kaggle Dataset 2: https://www.kaggle.com/datasets/rounakbanik/the-movies-dataset
- Kaggle Dataset 3: https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies

**Related Research:**
- Movie success prediction: Sharda & Delen (2006)
- Star power analysis: Elberse (2007)
- Box office forecasting: Basuroy et al. (2003)

---

#### Disclosure:
Derived from the original data viz course by Mine Cetinkaya-Rundel @ Duke University
