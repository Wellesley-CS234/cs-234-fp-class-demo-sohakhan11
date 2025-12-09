import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------
# Load Data
# -----------------------
@st.cache_data
def load_data():
    df = pd.read_csv("merged_econ_data.csv")
    return df

df = load_data()

st.title("Economist Popularity Explorer")
st.write("This dashboard explores 2024 Wikipedia pageviews for economists.")

# ----------------------------------------
# Sidebar Filters
# ----------------------------------------
st.sidebar.header("Filters")

# Gender filter
gender_options = df["gender_raw"].dropna().unique().tolist()
gender_filter = st.sidebar.multiselect(
    "Select gender(s):",
    options=gender_options,
    default=gender_options
)

# Apply gender filter
filtered = df[df["gender_raw"].isin(gender_filter)]

# Section 1: Overview numbers
st.header("Summary for Selected Filters")

col1, col2 = st.columns(2)

with col1:
    st.metric("Economists selected", len(filtered["name_x"].unique()))

with col2:
    st.metric("Total 2024 pageviews", int(filtered["total_views_2024"].sum()))

# Section 2: Top viewed economists
st.header("Top Viewed Economists (2024)")

if filtered.empty:
    st.warning("No data for these filters.")
else:
    top = (
        filtered.sort_values(by="total_views_2024", ascending=False)
        .head(20)
    )

    fig = px.bar(
        top,
        x="total_views_2024",
        y="name_x",
        orientation="h",
        title="Top 20 Economists in 2024",
    )
    fig.update_layout(yaxis=dict(autorange="reversed"))

    st.plotly_chart(fig, use_container_width=True)

# Section 3: Data Table
st.header("📄 Data Preview")

st.dataframe(filtered.head(50))
