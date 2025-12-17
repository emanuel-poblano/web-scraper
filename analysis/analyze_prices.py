import pandas as pd
import matplotlib.pyplot as plt
import re

# ─── Load the CSV ─────────────────────
df = pd.read_csv("data/listings.csv")

# ─── Clean the “price” column ─────────
def clean_price(x):
    if pd.isna(x):
        return None
    # Strip $ and commas
    return float(re.sub(r"[^\d.]", "", x))

df["price_clean"] = df["price"].apply(clean_price)

# ─── Clean the “sqft” column ──────────
def clean_sqft(x):
    if pd.isna(x):
        return None
    # Strip non-digits
    return float(re.sub(r"[^\d.]", "", x))

df["sqft_clean"] = df["sqft"].apply(clean_sqft)

# ─── Calculate price per sqft ────────
df = df.dropna(subset=["price_clean", "sqft_clean"])
df["price_per_sqft"] = df["price_clean"] / df["sqft_clean"]

# ─── Summary statistics ──────────────
print("\n=== Price Summary ===")
print(df["price_clean"].describe())

print("\n=== Sqft Summary ===")
print(df["sqft_clean"].describe())

print("\n=== Price per Sqft Summary ===")
print(df["price_per_sqft"].describe())

# ─── Averages by beds ────────────────
if "beds" in df.columns:
    # Extract numeric part of bed string, e.g. "2 beds" → 2
    df["beds_num"] = df["beds"].str.extract(r"(\d+)").astype(float)
    avg_by_beds = df.groupby("beds_num")["price_per_sqft"].mean().sort_index()
    print("\n=== Avg Price per Sqft by Beds ===")
    print(avg_by_beds)

# ─── Plots ───────────────────────────
plt.figure(figsize=(8, 4))
plt.hist(df["price_clean"], bins=30, color="steelblue")
plt.title("Home Price Distribution")
plt.xlabel("Price ($)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("output_price_distribution.png")
plt.show()

plt.figure(figsize=(8, 4))
plt.hist(df["price_per_sqft"], bins=30, color="darkorange")
plt.title("Price per Sqft Distribution")
plt.xlabel("Price per Sqft ($)")
plt.ylabel("Count")
plt.tight_layout()
plt.savefig("output_price_per_sqft.png")
plt.show()

print("\nAnalysis complete — charts saved to disk!")
