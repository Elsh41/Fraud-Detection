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




### SHAP Interpretation & Comparison

#### 1. MDI Importance vs. SHAP Importance
- **Built-in MDI Feature Importance** highlights `device_velocity` and `ip_velocity` as dominant contributors. However, MDI feature importance is structurally biased toward continuous, high-cardinality features. It only shows *how much* a feature is used to split trees, not the *direction* of its impact.
- **SHAP Summary Plot** corrects this cardinality bias. It reveals that short values of `time_since_signup` (low values shown in blue) have a massive positive force (pushing the model output to the right), heavily driving fraud risk. It also contextualizes direction: low values of user `age` moderately increase risk, whereas high values of `device_velocity` (red dots) strongly drive predictions toward class 1.

#### 2. Top 5 Drivers of Fraud
1. **time_since_signup:** Instantly buying a high-value item within seconds of registration is the absolute strongest behavioral sign of script-based or automated fraud.
2. **device_velocity:** High numbers of user IDs sharing a single device ID indicate device-spoofing or botnet activity.
3. **ip_velocity:** Multiple sessions emerging from the exact same IP address indicates proxy-pooling or structured coordinate attacks.
4. **purchase_value:** Abnormally high transaction amounts skew the model heavily toward fraud, as fraudsters seek to extract maximum economic value before accounts are blocked.
5. **hour_of_day:** Late-night transactions (between 12:00 AM and 4:00 AM) demonstrate a minor yet statistically significant positive push toward fraud predictions.

#### 3. Counterintuitive Findings
- **High Age Risk:** The model identified that very young profiles, but also exceptionally elderly profiles with high purchase values, exhibited higher risk scores. This indicates fraudsters might target or spoof specific vulnerable demographics.
- **The "Safe" Source:** One-hot encoded traffic channels (e.g., SEO/Direct) have surprisingly little predictive power when compared to pure behavioral telemetry (time delta & velocities), indicating that fraud vectors bypass traditional acquisition channel rules.


### Actionable Business Recommendations

Based on the SHAP interpretations and global feature drivers, HBGB Events and Marketing recommends implementing the following risk-mitigation protocols for the event campaign:

#### 1. Instant Purchase Velocity Lock (Derived from `time_since_signup` SHAP impact)
- **Insight:** SHAP identifies that a low `time_since_signup` value (registration-to-purchase window $< 10$ minutes) is the single highest driver of positive fraud predictions.
- **Action:** Introduce an automated **"cooling-off" velocity gate**. Any newly created user profile attempting a high-ticket transaction within 10 minutes of account signup must complete mandatory Out-of-Band Multi-Factor Verification (such as SMS or WhatsApp OTP verified through Ethio Telecom's network) before transaction clearance.

#### 2. Device Fingerprint Multi-Account Cap (Derived from `device_velocity` SHAP impact)
- **Insight:** High device velocity (multiple accounts sharing a single hardware identifier) drastically elevates risk. 
- **Action:** Limit device association at the client level. If more than 2 distinct user accounts transact using the same unique device fingerprint within a 24-hour window, flag all associated accounts for manual review and restrict subsequent purchases on that device to verified mobile wallet channels only.

#### 3. Dynamic Late-Night Escalation (Derived from `hour_of_day` SHAP impact)
- **Insight:** Transactions executed between 11:00 PM and 4:00 AM EAT push predictions toward fraud.
- **Action:** Implement a dynamic late-night friction protocol. High-value purchases occurring during these hours should trigger automated security checks (such as verifying Billing Zip Codes match the geolocation mapped via IP) to mitigate the risk of account takeovers while legitimate users are asleep.
