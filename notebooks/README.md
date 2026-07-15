### 1. Data Cleaning Justification
- Missing continuous metrics are imputed via historical medians to avoid outlier skewing. Unmatched IP addresses are mapped to 'Unknown' to retain structural categorical values without losing vital behavioral context.
- Duplicate rows are systematically dropped to eliminate duplicate bias in validation sets.

### 2. Resampling Justification (SMOTE Choice)
- **Why SMOTE?** Traditional Random Undersampling risks discarding critical patterns within genuine transactions. Synthetic Minority Over-sampling Technique (SMOTE) generates continuous synthetic examples along the line segments joining k-nearest neighbors of fraud instances. This expands the minority decision boundary, ensuring algorithms focus on spatial anomaly clustering instead of prioritizing the majority class.
- **Leakage Prevention:** Resampling is applied strictly to `X_train_transformed`, preserving the unaltered natural distribution of `X_test` for objective evaluation.


### Model Selection & Justification Report

#### 1. Evaluation Context
In fraud detection modeling, standard classification accuracy is ineffective due to extreme class imbalance (e.g., 99.1% legit vs 0.9% fraud). A model guessing "0" (Legitimate) endlessly would score 99.1% accuracy but catch zero fraud. We prioritize **AUC-PR (Area Under the Precision-Recall Curve)** and **F1-Score** because they focus exclusively on minimizing both False Positives (wasted customer investigation time) and False Negatives (financial losses due to uncaught fraud).

#### 2. Quantitative Trade-offs
- **Logistic Regression (Baseline):** Offers maximum structural interpretability. Coefficients instantly reveal feature impact vectors. However, it struggles with non-linear relationships, interactive feature dynamics (e.g., specific browsers matching anomalous device velocities), leading to lower AUC-PR scores and higher False Negatives.
- **Random Forest (Ensemble):** Drastically outperforms the linear baseline on AUC-PR. By aggregating diverse bootstrap decision trees, it inherently handles non-linear boundaries and high-cardinality multi-collinear inputs without suffering from overfitting (guarded by the restricted `max_depth`). 

#### 3. Selection Final Decision
**Selected Model:** Random Forest Ensemble
**Justification:** The Random Forest model demonstrates optimal stability across all 5 folds of our Stratified Cross-Validation sequence (showing low standard deviations in both metrics). While it sacrifices row-level transparency relative to a basic linear regression, the substantial lift in **AUC-PR** guarantees significantly higher fraud captures while simultaneously protecting operational teams from navigating high volumes of False Positives. We will leverage post-hoc explainability engines (like SHAP, scheduled in Task 4) to bridge the interpretive deficit of this ensemble.