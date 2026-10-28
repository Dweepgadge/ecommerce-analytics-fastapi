import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# ----------------- 1. SAMPLE DATASET (Customer Churn) -----------------
# Age, Balance, aur Support Calls ke hisab se Churn predict karna
# Churn: 1 = Bank Chhod diya (Left), 0 = Bank me ruka hua hai (Stayed)
data = {
    "Age":               [22, 25, 47, 52, 46, 56, 48, 29, 31, 35, 40, 58, 23, 50, 38],
    "Account_Balance":   [15000, 22000, 85000, 120000, 95000, 110000, 78000, 30000, 35000, 42000, 50000, 130000, 18000, 98000, 60000],
    "Support_Calls":     [1, 0, 5, 4, 3, 6, 4, 1, 0, 2, 1, 5, 0, 4, 2],
    "Churn":             [0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0]
}

df = pd.DataFrame(data)
print("=== 1. CUSTOMER DATA (First 5 Rows) ===")
print(df.head())


# ----------------- STEP 1: X (Features) aur y (Target) -----------------
X = df[["Age", "Account_Balance", "Support_Calls"]]
y = df["Churn"]  # Target is 0 or 1


# ----------------- STEP 2: TRAIN / TEST SPLIT -----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


# ----------------- STEP 3: LOGISTIC REGRESSION MODEL TRAIN KARO -----------------
model = LogisticRegression()
model.fit(X_train, y_train)
print("\n=== Model Training Complete! ===")


# ----------------- STEP 4: PREDICTION -----------------
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)[:, 1]  # Churn hone ki % probability

results = pd.DataFrame({
    "Actual_Churn": y_test.values,
    "Predicted_Churn": predictions,
    "Churn_Probability": probabilities.round(2)
})
print("\n=== 2. PREDICTIONS ON TEST CUSTOMERS ===")
print(results)


# ----------------- STEP 5: EVALUATION (Accuracy & Confusion Matrix) -----------------
acc = accuracy_score(y_test, predictions)
cm = confusion_matrix(y_test, predictions)

print(f"\nModel Accuracy: {acc * 100:.1f}%")
print("\nConfusion Matrix (Matrix Format):")
print(cm)


# ----------------- REAL-WORLD BUSINESS PREDICTION -----------------
# Naya Customer aaya: Age = 55, Balance = 90000, Support Calls = 5
new_customer = [[55, 90000, 5]]
pred = model.predict(new_customer)
prob = model.predict_proba(new_customer)[0][1]

print("\n" + "="*50)
print(f"👉 New Customer Alert:")
if pred[0] == 1:
    print(f"⚠️ HIGH RISK! Customer will CHURN (Leave Bank)! Probability: {prob*100:.1f}%")
else:
    print(f"✅ Customer will STAY! Probability: {prob*100:.1f}%")
print("="*50)