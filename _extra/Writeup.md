**Project Narrative: Star Power Analysis – Do Movie Stars Justify Their Premiums?**

**Author:** Juan Nadal

**Course:** INFO 523 – Data Mining and Discovery, Fall 2025

**Date:** November 2025

---

### Introduction and Motivation

At the outset of this project, I approached the idea of “star power” with skepticism. The assumption that high-profile actors inherently boost a movie’s revenue seemed oversimplified. To test this, I sourced three large datasets from Kaggle: one containing over a million movies, another focused on revenue and ROI, and a third detailing cast members. My goal was to integrate these datasets to uncover whether star power truly influences profitability.

---

### Data Quality Challenges

The initial analysis revealed significant data integrity issues that threatened to distort results.

**Budget Inaccuracies:**
For example, Robert Downey Jr. appeared in the 1987 movie "Less Than Zero" where the dataset showed a \$1 budget (actual budget was \$8 million) with \$20 million in revenue, making the ROI appear abnormally high. Many smaller films lacked any budget information, making comparisons unreliable.

**Incomplete Cost and Revenue Data:**
Some budgets excluded marketing expenses, which can match or exceed production costs. Revenue often reflected only theatrical sales, ignoring merchandise or streaming income, which is important for franchises like Marvel.

**Actor Compensation Gaps:**
Data on actor salaries is difficult to obtain. Compensation structures vary widely, including bonuses, profit-sharing, and backend revenue. These hidden variables complicated attempts to quantify “cost versus return” for specific stars.

---

### Methodology

To overcome missing or inconsistent salary data, I focused on **budget-relative ROI** as a measure of success:

$$
ROI = \frac {Revenue - Budget}{Budget} \times 100
$$

This ratio allowed meaningful comparisons across both low- and high-budget productions. For instance:

* A \$150M movie earning \$112.5M has an ROI of –25%.
* A \$10M film earning \$50M has an ROI of 400%.

This normalized success across production sizes and time periods.

---

### Findings and Statistical Results

After cleaning and merging data, I analyzed **5,311 movies (1915–2017)** with full financial records.

**Overall Results:**

* Total revenue: $485.6B
* Total budget: $167.2B
* Mean ROI: 343.9%
* Median ROI: 106.7%

**Key Outcome:** Star power accounted for **85.05%** of ROI prediction in machine learning models, far exceeding other variables.

* Correlation between cast ROI and movie ROI: **r = 0.441 (p < 0.001)**
* A-list films: 458.2% average ROI
* Non-A-list films: 337.2% average ROI
* Difference: **+121 percentage points (p = 0.024)**

Other factors—budget, release timing, and genre. Each contributed less than 4% to the ROI prediction.

| Star Tier             | Avg ROI | Movie Count | % of Total |
| --------------------- | ------- | ----------- | ---------- |
| Superstar (300%+)     | 788.5%  | 124         | 2.3%       |
| A-list (150–300%)     | 215.8%  | 169         | 3.2%       |
| B-list (50–150%)      | 62.6%   | 225         | 4.2%       |
| Unknown/C-list (<50%) | 350.1%  | 4,793       | 90.2%      |

---

### Why Star Power Matters

Analysis suggests stars influence success through several mechanisms:

* **Risk Mitigation:** Recognizable actors reassure investors and executives.
* **Marketing Efficiency:** Established stars reduce advertising costs.
* **Cross-Media Presence:** Many stars carry fan bases from television or social media.
* **Career Trajectories:** Early hits elevate actors, compounding future ROI potential.

---

### Case Studies

**Robert Downey Jr. – *Iron Man (2008)*:**
Budget \$140M, revenue \$585M (ROI 318%). RDJ’s \$600K salary evolved into \$75M per film post-success, proving how a single breakout role can generate immense career and studio returns.

**Robin Williams – *Mrs. Doubtfire (1993)*:**
Budget \$25M, revenue \$441M (ROI 1,665%). Williams’s average ROI across films (504%) demonstrates peak star profitability.

**The Hangover (2009):**
Despite an unknown cast, the film achieved 1,234% ROI on a $35M budget. This is an exception proving that great scripts and timing can sometimes offset lack of star power.

**Red One (2024):**
Even with Dwayne Johnson and Chris Evans, the film underperformed ROI (–25.6%), underscoring that celebrity alone cannot rescue weak storytelling.

**Argylle (2024):**
Despite an ensemble cast, ROI was (–55.8%), showing diminishing returns when high costs meet poor narrative reception.

---

### Data Limitations

The absence of cast data for major franchises like the Marvel Cinematic Universe weakened coverage.

* 88% of total films lacked cast ROI data.
* Notable omissions: *Iron Man*, *The Avengers*, *Deadpool*.

This likely means the 85% feature-importance estimate for star power is conservative.
More access to datasets like IMDB Pro or verified compensation databases could refine results further.

---

### Conclusions

The evidence strongly supports that **movie stars justify their pay premiums.**

* Cast ROI explained 85% of profitability prediction.
* A-list involvement added 121 percentage points to ROI.
* Budget and release timing effects were marginal.

However, star power cannot compensate for poor scripts or misaligned concepts. High salaries increase downside risk if the film fails.

---

### Recommendations

**For Studio Executives:**

* Prioritize proven stars (300%+ historical ROI).
* Combine strong stories with recognizable talent.

**For Producers:**

* Allocate budgets strategically; stars first, production second.
* Avoid overreliance on star names when scripts are weak.

**For Investors:**

* Focus on A-list or Superstar tier projects.
* Seek optimal release windows for maximum ROI.

---

### Future Research

Enhanced datasets could explore:

* 2008–2024 MCU and streaming-era films.
* Verified actor pay scales.
* Marketing cost breakdowns and merchandise revenue.
* Social media followers could count as an emerging star power proxy.

---

### Final Summary

Across 5,311 films analyzed with machine learning and statistical tests (ANOVA F = 19.1, t = 2.25, R² = 93.2%), the conclusion is:

**Yes, movie stars are worth their pay premiums.**

Star power remains the strongest predictor of return on investment. When coupled with compelling storytelling and production execution.
