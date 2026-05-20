#  python -m streamlit run web-page.py
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter

# -------------------------------
# Step 1: Load the dataset
# -------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("swiggy.csv")

df = load_data()

# -------------------------------
# Step 2: Dashboard Title
# -------------------------------
st.title("🍴 Swiggy Restaurant Data Dashboard")
st.markdown("An interactive dashboard to explore restaurant delivery times, ratings, prices, and cuisines.")

# -------------------------------
# Step 3: Sidebar Filters
# -------------------------------
st.sidebar.header("Filters")

# City filter
cities = df['City'].unique()
selected_city = st.sidebar.selectbox("Select City", cities)

# Area filter
areas = df[df['City'] == selected_city]['Area'].unique()
selected_area = st.sidebar.selectbox("Select Area", areas)

# Filtered Data
filtered_df = df[(df['City'] == selected_city) & (df['Area'] == selected_area)]

st.subheader(f"📍 Data for {selected_area}, {selected_city}")
st.write(filtered_df.head())

# -------------------------------
# Step 4: Key Metrics
# -------------------------------
avg_delivery = filtered_df['Delivery time'].mean()
avg_rating = filtered_df['Avg ratings'].mean()
avg_price = filtered_df['Price'].mean()

col1, col2, col3 = st.columns(3)
col1.metric("Average Delivery Time", f"{avg_delivery:.1f} mins")
col2.metric("Average Rating", f"{avg_rating:.2f}")
col3.metric("Average Price", f"₹{avg_price:.2f}")
# -------------------------------
# Step 5: Visualizations
# -------------------------------

sns.set_style("whitegrid")

# =========================================
# ROW 1
# =========================================

col1, col2 = st.columns(2)

# 1. Delivery Time Distribution
with col1:
    st.subheader("⏱ Delivery Time Distribution")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(
        filtered_df['Delivery time'],
        bins=30,
        kde=True,
        color="steelblue",
        ax=ax
    )

    ax.set_title("Delivery Time")
    st.pyplot(fig)

# 2. Ratings Distribution
with col2:
    st.subheader("⭐ Ratings Distribution")

    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(
        filtered_df['Avg ratings'],
        bins=20,
        kde=True,
        color="purple",
        ax=ax
    )

    ax.set_title("Ratings Distribution")
    st.pyplot(fig)

# =========================================
# ROW 2
# =========================================

col3, col4 = st.columns(2)

# 3. Top Cuisines
with col3:
    st.subheader("🍲 Top Cuisines")

    food_counts = Counter(
        ','.join(filtered_df['Food type']).split(',')
    )

    cuisine_df = pd.DataFrame(
        food_counts.most_common(10),
        columns=['Cuisine', 'Count']
    )

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        x='Cuisine',
        y='Count',
        data=cuisine_df,
        palette="magma",
        ax=ax
    )

    plt.xticks(rotation=45)
    ax.set_title("Top 10 Cuisines")

    st.pyplot(fig)

# 4. Fastest Restaurants
with col4:
    st.subheader("🏃 Fastest Restaurants")

    delivery_rest = (
        filtered_df.groupby('Restaurant')['Delivery time']
        .mean()
        .sort_values()
        .head(10)
    )

    fig, ax = plt.subplots(figsize=(6,4))

    sns.barplot(
        x=delivery_rest.values,
        y=delivery_rest.index,
        palette="viridis",
        ax=ax
    )

    ax.set_title("Top 10 Fastest Delivery")

    st.pyplot(fig)

# -------------------------------
# Step 6: Insights
# -------------------------------
st.subheader("📊 Insights")
st.markdown(f"""
- **Fastest delivery area overall:** {df.groupby('Area')['Delivery time'].mean().idxmin()}
- **Slowest delivery area overall:** {df.groupby('Area')['Delivery time'].mean().idxmax()}
- **Most popular cuisine in {selected_area}:** {cuisine_df.iloc[0]['Cuisine']}
- **Top restaurant by rating in {selected_area}:** {filtered_df.sort_values(by='Avg ratings', ascending=False).iloc[0]['Restaurant']}
""")