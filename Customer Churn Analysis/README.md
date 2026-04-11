# 📉 Customer Churn Prediction — Telecom



---


A telecom company loses revenue every time a customer cancels their subscription. The goal is to predict which customers are at risk of churning **before they leave**, so the retention team can take proactive action.

## 🎯 What Was Done
1. **EDA** — Analyzed churn patterns across contract type, payment method, internet service, tenure
2. **Feature Engineering** — Encoded categorical variables, scaled numerical features
3. **Modelling** — Trained Logistic Regression & Random Forest, compared with ROC-AUC
4. **Feature Importance** — Identified top churn drivers using Random Forest
5. **Business Recommendations** — Actionable retention strategies for each risk segment

## 📊 Key Results
| Model | ROC-AUC | CV AUC (5-fold) |
|---|---|---|
| Logistic Regression | ~0.82 | ~0.81 |
| **Random Forest** | **~0.84** | **~0.83** |

## 💡 Key Churn Drivers Found
1. **Month-to-month contracts** — highest churn rate (~42%)
2. **High monthly charges** (>₹70) — significantly increases churn risk
3. **Fiber optic + no tech support** — vulnerable segment
4. **Electronic check payment** — associated with higher churn
5. **Low tenure (<12 months)** — new customers need early engagement

## 💼 Business Impact
- Model correctly identifies churners 84% of the time (AUC)
- Targeting the **top 20% high-risk customers** with retention offers can reduce churn by an estimated **15–20%**

## 🗂️ Project Structure
```
customer_churn_analysis/
├── churn_analysis.py    # Full EDA + ML pipeline + recommendations
├── churn_analysis.png   # Visualizations (ROC, confusion matrix, feature importance)
└── README.md
```

## 🚀 How to Run
```bash
pip install pandas numpy scikit-learn matplotlib seaborn
python churn_analysis.py
```

## 🛠️ Skills Demonstrated
- Exploratory Data Analysis (EDA)
- Feature Engineering & Preprocessing
- Binary Classification (Logistic Regression, Random Forest)
- Model Evaluation (ROC-AUC, Cross-Validation, Confusion Matrix)
- Business Insight Generation & Recommendations

**Dataset:** 7,043 telecom customer records  
**Best Model AUC:** 0.84+

