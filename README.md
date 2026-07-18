# E-Commerce & Credit Card Fraud Detection Pipeline

An end-to-end machine learning engineering pipeline designed to ingest, process, and analyze dual-source transactional data to detect fraud patterns. The project implements optimized range-based network lookups, scalable feature engineering, class imbalance correction, and SHAP-driven model explainability.

---

## 📌 Project Overview
Modern financial networks process billions of transactions daily, requiring highly performant data architectures to isolate fraudulent patterns without degrading consumer checkout flow. This repository establishes a modular, production-ready pipeline split across two key targets:
1. **E-Commerce Fraud Data:** Enriched dynamically via a custom high-performance range-based network mapping layer (`pd.merge_asof`) utilizing IP address integer ranges to locate origins.
2. **Credit Card Transactions:** High-dimensional, PCA-transformed anonymized feature matrices optimized for severe class imbalance remediation.

---

## 📂 Project Directory Structure

```text
Fraud-Detection/
├── .github/workflows/    # CI/CD automated test workflows
├── data/
│   ├── raw/              # Raw transaction & IP lookup CSV datasets (Git ignored)
│   └── processed/        # Transformed arrays and feature frames (Git ignored)
├── models/               # Serialized model artifacts (.pkl binaries)
├── notebooks/            # Exploratory Analysis & Model Interpretation
│   ├── eda-creditcard.ipynb
│   ├── feature-engineering.ipynb
│   └── shap-explainability.ipynb
├── src/                  # Production-ready Python core modules
│   ├── __init__.py
│   └── processing.py     # Range-based IP lookup & type-safe encoders
├── tests/                # Automated validation layers
│   └── test_processing.py
├── .gitignore            # Ignores local environments, large data frames, and .npy arrays
├── requirements.txt      # Production package dependency list
└── README.md             # Project documentation


