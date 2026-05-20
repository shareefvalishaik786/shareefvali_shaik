# ============================================
# Swiggy Restaurant Dataset Analysis Project
# Author: Muninagaraju
# Tools: Python (Pandas, Seaborn, Matplotlib)
# ============================================

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# -------------------------------
# Step 1: Load the dataset
# -------------------------------
df = pd.read_csv("swiggy.csv")   # Use read_excel if your file is .xlsx

# -------------------------------
# Step 2: Basic Data Checks
# -------------------------------
print("=== Dataset Info ===")
print(df.info())
print("\n=== Missing Values ===")
print(df.isnull().sum())
print("\n=== Summary Statistics ===")
print(df.describe())

# -------------------------------
# Step 3: Data Cleaning & Feature Engineering
# -------------------------------
# Create a new feature: Price per Rating
df['Price_per_rating'] = df['Price'] / df['Avg ratings']

# Categorize delivery speed
def categorize_delivery(x):
    if x < 50:
        return "Fast"
    elif 50 <= x <= 60:
        return "Medium"
    else:
        return "Slow"

df['Delivery_category'] = df['Delivery time'].apply(categorize_delivery)

# -------------------------------
# Step 4: Exploratory Data Analysis (EDA)
# -------------------------------

# 4.1 Average delivery time per area
delivery_by_area = df.groupby('Area')['Delivery time'].mean().sort_values()
print("\n=== Average Delivery Time by Area (Top 10) ===")
print(delivery_by_area.head(10))

# 4.2 Top cuisines
food_counts = Counter(','.join(df['Food type']).split(','))
print("\n=== Top 10 Cuisines ===")
print(food_counts.most_common(10))

# 4.3 Top restaurants by rating
top_rated = df.sort_values(by='Avg ratings', ascending=False).head(10)
print("\n=== Top 10 Restaurants by Rating ===")
print(top_rated[['Restaurant', 'Avg ratings', 'Total ratings']])

# -------------------------------
# Step 5: Visualizations
# -------------------------------

sns.set_style("whitegrid")  # Professional style

# Distribution of delivery times
plt.figure(figsize=(8,5))
sns.histplot(df['Delivery time'], bins=30, kde=True, color="steelblue")
plt.title("Distribution of Delivery Times", fontsize=14)
plt.xlabel("Delivery Time (minutes)")
plt.ylabel("Frequency")
plt.show()

# Average delivery time by area (Top 10)
plt.figure(figsize=(10,6))
sns.barplot(x=delivery_by_area.index[:10], y=delivery_by_area.values[:10], palette="viridis")
plt.xticks(rotation=45)
plt.title("Average Delivery Time by Area (Top 10)", fontsize=14)
plt.xlabel("Area")
plt.ylabel("Average Delivery Time (minutes)")
plt.show()

# Cuisine frequency bar chart
cuisine_df = pd.DataFrame(food_counts.most_common(10), columns=['Cuisine','Count'])
plt.figure(figsize=(8,5))
sns.barplot(x='Cuisine', y='Count', data=cuisine_df, palette="magma")
plt.xticks(rotation=45)
plt.title("Top 10 Cuisines", fontsize=14)
plt.xlabel("Cuisine")
plt.ylabel("Number of Restaurants")
plt.show()



# -------------------------------
# Step 6: Export Results
# -------------------------------
# Export cleaned dataset with new features
df.to_excel("swiggy_analysis_results.xlsx", index=False)

print("\n=== Analysis complete. Visualizations displayed and results exported to Excel. ===")