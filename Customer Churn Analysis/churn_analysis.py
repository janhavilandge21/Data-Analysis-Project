
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (classification_report, confusion_matrix,
                              roc_auc_score, roc_curve, ConfusionMatrixDisplay)
from sklearn.inspection import permutation_importance
import warnings
warnings.filterwarnings("ignore")

print("=" * 55)
print("   CUSTOMER CHURN PREDICTION — JANHAVI LANDGE")
print("=" * 55)

# ─── 1. DATA GENERATION ───────────────────────────────────────────────────────
np.random.seed(42)
n = 7043  # Same size as real Telco churn dataset

tenure       = np.random.randint(1, 73, n)
monthly_charges = np.random.uniform(18, 118, n).round(2)
total_charges   = (tenure * monthly_charges * np.random.uniform(0.85, 1.0, n)).round(2)

contract    = np.random.choice(["Month-to-month","One year","Two year"], n,
                                p=[0.55, 0.24, 0.21])
internet    = np.random.choice(["DSL","Fiber optic","No"], n, p=[0.34,0.44,0.22])
payment     = np.random.choice(["Electronic check","Mailed check",
                                 "Bank transfer","Credit card"], n,
                                p=[0.34,0.23,0.22,0.21])
senior      = np.random.choice([0, 1], n, p=[0.84, 0.16])
partner     = np.random.choice(["Yes","No"], n, p=[0.48,0.52])
dependents  = np.random.choice(["Yes","No"], n, p=[0.30,0.70])
tech_support= np.random.choice(["Yes","No","No internet service"], n, p=[0.29,0.49,0.22])
paperless   = np.random.choice(["Yes","No"], n, p=[0.59,0.41])
gender      = np.random.choice(["Male","Female"], n)

# Churn probability based on real-world drivers
churn_prob = (
    0.05 +
    (contract == "Month-to-month").astype(float) * 0.25 +
    (internet == "Fiber optic").astype(float) * 0.10 +
    (payment == "Electronic check").astype(float) * 0.08 +
    senior.astype(float) * 0.05 +
    (monthly_charges > 70).astype(float) * 0.08 +
    (tenure < 12).astype(float) * 0.12 -
    (partner == "Yes").astype(float) * 0.04 -
    (tech_support == "Yes").astype(float) * 0.06
)
churn_prob = np.clip(churn_prob, 0, 1)
churn = (np.random.uniform(0, 1, n) < churn_prob).astype(int)

df = pd.DataFrame({
    "tenure": tenure, "monthly_charges": monthly_charges,
    "total_charges": total_charges, "contract": contract,
    "internet_service": internet, "payment_method": payment,
    "senior_citizen": senior, "partner": partner,
    "dependents": dependents, "tech_support": tech_support,
    "paperless_billing": paperless, "gender": gender, "churn": churn
})

print(f"\n[1] Dataset Shape       : {df.shape}")
print(f"    Churn Rate          : {df['churn'].mean()*100:.2f}%")
print(f"    Non-Churn           : {(df['churn']==0).sum():,}")
print(f"    Churn               : {(df['churn']==1).sum():,}")

# ─── 2. EDA ───────────────────────────────────────────────────────────────────
print(f"\n[2] EDA — Churn Rate by Key Segments:")

for col in ["contract","internet_service","payment_method"]:
    rate = df.groupby(col)["churn"].mean().sort_values(ascending=False)
    print(f"\n  By {col.replace('_',' ').title()}:")
    for k, v in rate.items():
        bar = "█" * int(v * 40)
        print(f"    {k:<22}: {v*100:5.1f}%  {bar}")

# ─── 3. PREPROCESSING ─────────────────────────────────────────────────────────
le = LabelEncoder()
cat_cols = ["contract","internet_service","payment_method",
            "partner","dependents","tech_support","paperless_billing","gender"]
for col in cat_cols:
    df[col+"_enc"] = le.fit_transform(df[col])

feature_cols = (["tenure","monthly_charges","total_charges","senior_citizen"] +
                [c+"_enc" for c in cat_cols])

X = df[feature_cols]
y = df["churn"]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.20, random_state=42, stratify=y)

print(f"\n[3] Train size: {len(X_train):,} | Test size: {len(X_test):,}")

# ─── 4. MODEL TRAINING ────────────────────────────────────────────────────────
models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
}

results = {}
print(f"\n[4] MODEL PERFORMANCE:\n{'─'*55}")
for name, model in models.items():
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:,1]
    auc    = roc_auc_score(y_test, y_prob)
    cv     = cross_val_score(model, X_scaled, y, cv=5, scoring="roc_auc").mean()
    results[name] = {"model":model,"pred":y_pred,"prob":y_prob,"auc":auc,"cv_auc":cv}
    print(f"\n  {name}:")
    print(f"    ROC-AUC Score   : {auc:.4f}")
    print(f"    CV ROC-AUC (5x) : {cv:.4f}")
    print(f"\n{classification_report(y_test, y_pred, target_names=['No Churn','Churn'])}")

# Best model
best_name = max(results, key=lambda k: results[k]["auc"])
best      = results[best_name]
print(f"  ✅ Best Model: {best_name} (AUC = {best['auc']:.4f})")

# ─── 5. FEATURE IMPORTANCE ────────────────────────────────────────────────────
rf_model   = results["Random Forest"]["model"]
importances = pd.Series(rf_model.feature_importances_, index=feature_cols)\
                .sort_values(ascending=False)

print(f"\n[5] TOP CHURN DRIVERS (Feature Importance):")
for feat, imp in importances.head(8).items():
    bar = "█" * int(imp * 200)
    print(f"  {feat:<30}: {imp:.4f}  {bar}")

# ─── 6. VISUALIZATIONS ────────────────────────────────────────────────────────
fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle("Customer Churn Analysis — Janhavi Landge", fontsize=15, fontweight="bold")

# Plot 1: Churn distribution
axes[0,0].pie([y.value_counts()[0], y.value_counts()[1]],
              labels=["No Churn","Churn"], autopct="%1.1f%%",
              colors=["#2563EB","#EF4444"], startangle=90)
axes[0,0].set_title("Overall Churn Distribution")

# Plot 2: Churn by Contract
ct = df.groupby("contract")["churn"].mean().sort_values(ascending=False).reset_index()
sns.barplot(data=ct, x="contract", y="churn", palette="Reds_r", ax=axes[0,1])
axes[0,1].set_title("Churn Rate by Contract Type")
axes[0,1].set_ylabel("Churn Rate")
axes[0,1].tick_params(axis='x', rotation=10)

# Plot 3: Monthly Charges vs Churn
sns.boxplot(data=df, x="churn", y="monthly_charges",
            palette=["#2563EB","#EF4444"], ax=axes[0,2])
axes[0,2].set_title("Monthly Charges vs Churn")
axes[0,2].set_xticklabels(["No Churn","Churn"])

# Plot 4: ROC Curve
for name, r in results.items():
    fpr, tpr, _ = roc_curve(y_test, r["prob"])
    axes[1,0].plot(fpr, tpr, linewidth=2, label=f"{name} (AUC={r['auc']:.3f})")
axes[1,0].plot([0,1],[0,1],"k--")
axes[1,0].set_title("ROC Curve Comparison")
axes[1,0].set_xlabel("False Positive Rate")
axes[1,0].set_ylabel("True Positive Rate")
axes[1,0].legend()

# Plot 5: Feature Importance
top_features = importances.head(8)
sns.barplot(x=top_features.values, y=top_features.index,
            palette="Blues_r", ax=axes[1,1])
axes[1,1].set_title("Top Churn Drivers (Feature Importance)")
axes[1,1].set_xlabel("Importance")

# Plot 6: Confusion Matrix (best model)
cm = confusion_matrix(y_test, best["pred"])
disp = ConfusionMatrixDisplay(cm, display_labels=["No Churn","Churn"])
disp.plot(ax=axes[1,2], colorbar=False, cmap="Blues")
axes[1,2].set_title(f"Confusion Matrix — {best_name}")

plt.tight_layout()
plt.savefig("churn_analysis.png", dpi=150, bbox_inches="tight")
print(f"\n[✓] Charts saved → churn_analysis.png")

# ─── 7. BUSINESS RECOMMENDATIONS ─────────────────────────────────────────────
print(f"\n{'─'*55}")
print("  BUSINESS RECOMMENDATIONS")
print(f"{'─'*55}")
print("  1. Customers on Month-to-month contracts churn most —")
print("     offer discounts to upgrade them to annual plans.")
print("  2. High monthly charges + Fiber optic = high churn risk —")
print("     introduce loyalty pricing for long-tenure users.")
print("  3. Customers without Tech Support churn more —")
print("     proactively offer free tech support trials.")
print("  4. Electronic check payers have highest churn —")
print("     incentivize auto-pay (bank transfer) with discounts.")
print(f"{'─'*55}")
print(f"\n  Model AUC = {best['auc']:.4f} — means the model correctly ranks")
print(f"  a churner above a non-churner {best['auc']*100:.1f}% of the time.")
