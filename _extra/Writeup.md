# Are Movie Stars Worth Their Premiums? A Data Mining Analysis of ROI Predictors in Cinema

**Author:** Juan Nadal
**Course:** INFO 523 - Data Mining and Discovery, Fall 2025
**Institution:** College of Information Science, University of Arizona

---

## Introduction

The entertainment industry spends billions annually on celebrity salaries, operating under the assumption that star power drives box office success. Yet this assumption warrants empirical scrutiny: do expensive movie stars actually deliver higher returns on investment, or do other factors matter more?

This project investigates a fundamental business question: **Are movie stars worth their premium salaries?** Using data mining techniques, I analyzed whether star power—measured as cast members' historical ROI performance—predicts a film's financial success better than competing factors such as budget discipline, release timing, genre, and franchise status.

### Dataset Description

The analysis draws from three Kaggle datasets merged into a unified dataset of 5,311 movies spanning 1915 to 2017. The combined data represents $485.6 billion in total revenue and $167.2 billion in production budgets.

**Key Variables:**

| Variable | Description | Type |
|----------|-------------|------|
| `roi` | Return on Investment: (Revenue - Budget) / Budget * 100 | Target (continuous) |
| `cast_avg_roi` | Average historical ROI of a film's cast members | Predictor (continuous) |
| `budget` | Production budget in USD | Predictor (continuous) |
| `budget_micro` | Binary flag for micro-budget films (<$1M) | Predictor (binary) |
| `revenue` | Total box office revenue in USD | Excluded (target leakage) |
| `vote_average` | Audience rating (0-10 scale) | Predictor (continuous) |
| `vote_count` | Number of user votes/ratings | Predictor (continuous) |
| `runtime` | Film length in minutes | Predictor (continuous) |
| `is_franchise` | Whether the film is part of a franchise | Predictor (binary) |
| `num_top_actors` | Count of high-profile actors in cast | Predictor (integer) |
| `release_month` | Month of theatrical release | Predictor (categorical) |
| `star_tier` | Categorization: Superstar, A-list, B-list, Unknown | Predictor (categorical) |

The dataset contains 60 total features after engineering, including genre indicators, release year bins, and budget categories.

**Important Limitation:** Only 640 movies (12%) contain complete historical ROI data for cast members, representing the subset where star power analysis is most reliable.

---

## Justification of Approach

I selected a two-pronged analytical approach combining traditional statistical methods with machine learning, chosen specifically because of the research question's complexity.

### Statistical Methods Justification

**Correlation Analysis** was selected to measure the linear relationship between star power (`cast_avg_roi`) and film ROI. Pearson correlation provides a standardized measure (-1 to +1) that quantifies relationship strength without assuming causation.

**ANOVA (Analysis of Variance)** was used to compare mean ROI across star tiers (Superstar, A-list, B-list, Unknown). ANOVA is appropriate when comparing means across multiple categorical groups, testing whether observed differences exceed what random chance would produce.

**Independent T-Test** compared top-tier stars (A-list and Superstar combined) against all other films. This binary comparison directly addresses whether premium talent delivers measurably different returns. Cohen's d effect size was calculated to assess practical significance beyond statistical significance.

### Machine Learning Justification

Six regression models were trained to predict ROI from pre-release features:

1. **Linear Regression** - Baseline model assuming linear relationships
2. **Ridge Regression** - L2 regularization to handle multicollinearity among features
3. **Lasso Regression** - L1 regularization for automatic feature selection
4. **Random Forest** - Ensemble method capturing non-linear interactions
5. **Gradient Boosting** - Sequential ensemble for complex patterns
6. **XGBoost** - Optimized gradient boosting with regularization

This ensemble approach was chosen because (a) no single algorithm consistently outperforms others across all datasets, and (b) comparing models provides confidence in findings—if multiple models agree that star power ranks low in importance, the conclusion is robust.

**Train-Test Split:** 80/20 split with cross-validation ensured models generalize to unseen data rather than memorizing training examples.

---

## Data Preparation and Quality

Raw data contained significant quality issues requiring systematic cleaning.

### Outlier Handling

The dataset contained 52 movies with budgets under $1,000, including some listed at $1. These data errors produced mathematically absurd ROI values exceeding 1 billion percent. Such outliers would dominate statistical measures and distort model training.

**Solution:** Movies with budgets below $1,000 were removed. ROI values were capped at the 99th percentile (6,620.4%) to ensure analysis reflected realistic business scenarios while retaining legitimate high-performers.

### Missing Data

Cast financial history was unavailable for 88% of films (4,671 movies). Rather than imputation—which would introduce artificial patterns—the star power analysis focuses on the 640-movie subset with complete data. This represents films where detailed casting records were preserved, likely higher-profile productions where star power would matter most.

### Feature Engineering

Star tiers were created based on `cast_avg_roi`:
- **Superstar:** >300% historical ROI (124 movies, 2.3%)
- **A-list:** 150-300% historical ROI (169 movies, 3.2%)
- **B-list:** 50-150% historical ROI (225 movies, 4.2%)
- **Unknown/C-list:** <50% or missing data (4,793 movies, 90.2%)

---

## Results

### Statistical Findings

**Correlation Analysis** revealed that star power has a weak positive correlation with ROI (r = 0.078, p < 0.001). This correlation coefficient indicates that `cast_avg_roi` explains only 0.61% of variance in film ROI (r-squared = 0.006). By comparison, `vote_average` showed stronger correlation (r = 0.171), while `budget` showed negative correlation (r = -0.135), suggesting higher budgets tend to reduce ROI percentage.

**ANOVA Results** showed statistically significant differences across star tiers (F = 19.1, p < 0.001):
- Superstar films: 788.5% mean ROI
- A-list films: 215.8% mean ROI
- B-list films: 62.6% mean ROI
- Unknown/C-list films: 350.1% mean ROI

The paradoxically high Unknown category ROI is explained by micro-budget films: a $10,000 production earning $1 million generates 10,000% ROI, inflating this category's average.

**T-Test Results** comparing top-tier stars against others found a difference of +121% ROI (t = 2.25, p = 0.024). However, Cohen's d = 0.14 indicates negligible effect size—the distributions overlap substantially, meaning stars do not guarantee higher returns despite the average difference.

### Machine Learning Findings

**Critical Methodological Correction:** Initial models achieved R-squared of 93.2% with star power dominating feature importance. Upon review, I discovered **target leakage**—the model included `revenue` as a predictor. Since ROI = (Revenue - Budget) / Budget, using revenue to predict ROI constitutes circular logic.

After removing revenue and retraining all models, XGBoost achieved the best performance with R-squared = 33.7%. The corrected feature importance rankings:

| Rank | Feature | Importance |
|------|---------|------------|
| 1 | budget_micro | 30.4% |
| 2 | runtime_long | 8.2% |
| 3 | vote_count | 5.3% |
| 4 | num_top_actors | 5.0% |
| 5 | is_franchise | 4.7% |
| ... | ... | ... |
| 29 | cast_avg_roi | 1.12% |

Budget category emerged as the dominant predictor at 30.4% importance—approximately **27 times more important** than star power's 1.12%.

---

## Discussion

The convergence of statistical and machine learning evidence supports a clear conclusion: **movie stars are not worth their premium salaries based on ROI data.**

The weak correlation (r = 0.078) and low feature importance (1.12%, rank 29 of 51) indicate that star power has minimal predictive value for film profitability. While the t-test showed stars associated with +121% higher average ROI, the negligible effect size (d = 0.14) reveals this average is driven by outliers rather than consistent outperformance. High variance in star-driven films means premium talent provides no reliable return guarantee.

The finding that budget discipline ranks first (30.4% importance) aligns with industry observations: micro-budget productions like horror films or independent dramas require smaller returns to achieve profitability. A $2 million film earning $10 million represents 400% ROI, while a $200 million blockbuster earning $400 million achieves only 100% ROI despite generating far more absolute profit.

**Limitations:** The 33.7% R-squared indicates that 66% of ROI variance remains unexplained by available features—likely driven by marketing spend, word-of-mouth, critical reception timing, and cultural factors not captured in the dataset. Additionally, the analysis uses pre-streaming era data (ending 2017), and the industry has transformed significantly since.

---

## Conclusion

Across 5,311 films analyzed using six machine learning models and multiple statistical tests, the evidence demonstrates that movie stars do not justify their salary premiums based on return on investment.

Budget discipline is 27 times more important than star power in predicting film ROI. Studios seeking to maximize returns should prioritize production cost management, franchise development, and audience engagement metrics over celebrity casting. The data suggests that talented unknown actors may offer better risk-adjusted returns than expensive A-list talent.

Future research should incorporate marketing budgets, streaming platform data (Netflix, Disney+, etc.), and social media metrics to capture the full spectrum of factors driving modern film success.

---

*Word Count: ~1,450 words*
