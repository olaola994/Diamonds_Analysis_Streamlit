import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

original_df = sns.load_dataset("diamonds")
df = original_df

st.title('Diamond analysis')

st.header('30 sample rows')

st.sidebar.header("Choose your filters")

with st.sidebar:
    colors = st.multiselect(
        "Choose color",
        sorted(df["color"].dropna().unique())
    )
    cuts = st.multiselect(
        "Choose cut",
        sorted(df["cut"].dropna().unique())
    )
    min_price, max_price = st.slider(
        "Choose pice range",
        min_value = int(df["price"].min()),
        max_value=int(df["price"].max()), 
        value=(int(df["price"].min()), int(df["price"].max()))
    )

if colors:
    df = df[df["color"].isin(colors)]

if cuts:
    df = df[df["cut"].isin(cuts)]
df = df[(df["price"] >= min_price) & (df["price"] <= max_price)]

c0,c1 = st.columns(2)
with c0:
    st.dataframe(
    df.sample(min(30, len(df))),
    use_container_width=True,
    hide_index=True
    )
with c1:
    st.image(
        f"diamond.webp"
    )


st.header('How does the price depend on the mass (carat)?')

fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(data=df, x="carat", y="price", alpha=0.3, ax=ax)
ax.set_xlabel("Mass (carat)")
ax.set_ylabel("Price ($)")
ax.set_title("Dependence of diamond price on weight (carat)")
st.pyplot(fig)
st.markdown("""
### 📊 Conclusions:
- Diamonds with a higher carat are more expensive.
- Price increases in proportion to weight - larger diamonds are **significantly more expensive**.
""")


st.header("Does the quality of the grind (cut) affect the price?")

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=original_df, x="cut", y="price", ax=ax, palette="viridis", order=["Fair", "Good", "Very Good", "Premium", "Ideal"])
ax.set_xlabel("Quality of Cut")
ax.set_ylabel("Average Price ($)")
ax.set_title("Average Price of Diamonds by Cut Quality")
st.pyplot(fig)
st.markdown("""
### 📊 Conclusions:
- The quality of the grind affects the price, while the price does not increase with the quality.
- The most expensive grind is premium and fair.
""")

st.header('What combinations of colour and purity are the most expensive?')

pivot_table = original_df.pivot_table(values="price", index="color", columns="clarity", aggfunc="mean")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(pivot_table, annot=True, fmt=".0f", cmap="coolwarm", linewidths=0.5, ax=ax)
ax.set_xlabel("Clarity")
ax.set_ylabel("Colour")
ax.set_title("Average Price of Diamonds by Colour and Clarity")

st.pyplot(fig)

df["depth_range"] = pd.cut(df["depth"], bins=[50, 55, 60, 65, 70], labels=["50-55%", "55-60%", "60-65%", "65-70%"])
st.markdown("""
### 📊 Conclusions:
- The most expensive combinations of colour and purity are D IF, I SI2 and J SI2 respectively.
""")

st.header("Does colour influence carat weight?")

fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=original_df, x="color", y="carat", ax=ax, palette="muted")
ax.set_xlabel("Colour")
ax.set_ylabel("Carat")
ax.set_title("Carat Distribution Across Diamond Colours")

st.pyplot(fig)
st.markdown("""
### 📊 Conclusions:
- Colours influcene carat weight, the further away the colour, the heavier the carat.
""")

st.header("The most common diamond characteristics")
common_combinantions = original_df.groupby(["cut", "color","clarity"]).size().reset_index(name="count")
common_combinantions = common_combinantions.sort_values(by="count", ascending=False).head(10)
st.dataframe(
    common_combinantions,
    use_container_width=True,
    hide_index=True
)

st.header("How does clarity and cut affect price?")

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=original_df, x="clarity", y="price", hue="cut", palette="coolwarm", ax=ax)
ax.set_xlabel("Clarity")
ax.set_ylabel("Average Price ($)")
ax.set_title("Average Price of Diamonds by Clarity and Cut")

st.pyplot(fig)
st.markdown("""
### 📊 Conclusions:
- The average price does not increase linearly - for example, VVS1 and VVS2 diamonds are not significantly cheaper than IF.
- The greater the purity, the greater the price range: high-purity diamonds (IF, VVS1) have greater price differences depending on the cut. Diamonds of lower purity (SI1, SI2) have more even prices between the different cuts.
""")

st.header("What are the most common diamond carats?")
fig, ax = plt.subplots(figsize=(14, 7))
sns.histplot(data=original_df["carat"], bins=50, kde=True, ax=ax, color="blue")
ax.set_xlabel("Carat")
ax.set_ylabel("Count")
ax.set_xticks(np.arange(0, original_df["carat"].max() + 0.2, 0.2))
st.pyplot(fig)
st.markdown("""
### 📊 Conclusions:
- The most common carats of diamonds are those in the range 0.3-0.4.
""")

# st.header("How do different features affect the price at the same time?")
# fig = sns.pairplot(df, vars=["carat", "depth", "table", "price"], hue="cut", palette="coolwarm")
# st.pyplot(fig)

st.header("Are there extreme outliers in diamond sizes?")
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(data=original_df, y="carat", ax=ax, color="red")
ax.set_title("Carat Outliers")
st.pyplot(fig)

median_carat = original_df["carat"].median()
mean_carat = original_df["carat"].mean()

st.write(f"**Carat median**: {median_carat:.2f}")
st.write(f"**Carat mean**: {mean_carat:.2f}")

st.markdown("""
### 📊 Conclusions:
- Most of the diamonds in the base are less than 2 carats in weight, suggesting that larger diamonds are much rarer.
- Diamonds over 2 carats are outliers.
""")

st.header("How do multiple dimensions influence diamond price?")

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

sns.scatterplot(data=original_df, x='x', y='price', alpha=0.3, ax=axes[0])
axes[0].set_title('Length (x) vs Price')
axes[0].set_xlabel('x (Length)')
axes[0].set_ylabel('Price ($)')

sns.scatterplot(data=original_df, x='y', y='price', alpha=0.3, ax=axes[1])
axes[1].set_title('Width (y) vs Price')
axes[1].set_xlabel('y (Width)')
axes[1].set_ylabel('Price ($)')

sns.scatterplot(data=original_df, x='z', y='price', alpha=0.3, ax=axes[2])
axes[2].set_title('Depth (z) vs Price')
axes[2].set_xlabel('z (Depth)')
axes[2].set_ylabel('Price ($)')

plt.tight_layout()
st.pyplot(fig)

st.markdown("""
### 📊 Conclusions:
- Each dimension increases the price of a diamond as its value increases.
""")