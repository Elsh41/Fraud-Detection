### 1. Data Cleaning Justification
- Missing continuous metrics are imputed via historical medians to avoid outlier skewing. Unmatched IP addresses are mapped to 'Unknown' to retain structural categorical values without losing vital behavioral context.
- Duplicate rows are systematically dropped to eliminate duplicate bias in validation sets.

### 2. Resampling Justification (SMOTE Choice)
- **Why SMOTE?** Traditional Random Undersampling risks discarding critical patterns within genuine transactions. Synthetic Minority Over-sampling Technique (SMOTE) generates continuous synthetic examples along the line segments joining k-nearest neighbors of fraud instances. This expands the minority decision boundary, ensuring algorithms focus on spatial anomaly clustering instead of prioritizing the majority class.
- **Leakage Prevention:** Resampling is applied strictly to `X_train_transformed`, preserving the unaltered natural distribution of `X_test` for objective evaluation.