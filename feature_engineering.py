import pandas as pd
from sklearn.preprocessing import StandardScaler

# ----------------- 1. RAW DIRTY REAL-WORLD DATA -----------------
# Notice: City text hai, aur Age (chhoti) vs Salary (bohot badi) hai!
data = {
    "Age":        [22, 45, 30, 52, 28, 40],
    "Salary":     [25000, 120000, 65000, 180000, 45000, 95000],
    "City":       ["Delhi", "Mumbai", "Delhi", "Bangalore", "Mumbai", "Bangalore"],
    "Purchased":  [0, 1, 0, 1, 0, 1]  # Target (0 = No, 1 = Yes)
}

df = pd.DataFrame(data)
print("=== 1. ORIGINAL RAW DATA ===")
print(df)


# ----------------- STEP 1: ONE-HOT ENCODING (Text ko 0 aur 1 banana) -----------------
# pd.get_dummies automatically text columns ko 0/1 me convert kar deta hai
# drop_first=True lagate hain to avoid "Dummy Variable Trap" (Multicollinearity)
df_encoded = pd.get_dummies(df, columns=["City"], drop_first=True, dtype=int)

print("\n=== 2. AFTER ONE-HOT ENCODING (No Strings Left!) ===")
print(df_encoded)


# ----------------- STEP 2: SEPARATE X AND y -----------------
X = df_encoded.drop("Purchased", axis=1)  # Saare input features
y = df_encoded["Purchased"]               # Target output


# ----------------- STEP 3: FEATURE SCALING (StandardScaler) -----------------
# Age aur Salary ko ek hi scale par la rahe hain
scaler = StandardScaler()

# Numeric columns ko scale karo
scaled_features = scaler.fit_transform(X)

X_scaled = pd.DataFrame(scaled_features, columns=X.columns)

print("\n=== 3. FINAL ML-READY SCALED FEATURES (Mean=0, Std=1) ===")
print(X_scaled.round(2))