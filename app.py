import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
-  The greater the purity, the greater the price range: high-purity diamonds (IF, VVS1) have greater price differences depending on the cut. Diamonds of lower purity (SI1, SI2) have more even prices between the different cuts.
""")

st.header("How do different features affect the price at the same time?")
fig = sns.pairplot(df, vars=["carat", "depth", "table", "price"], hue="cut", palette="coolwarm")
st.pyplot(fig)
