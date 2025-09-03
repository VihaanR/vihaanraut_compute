import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ----------------------------
# Load Data
# ----------------------------
@st.cache_data
def load_data():
    # Make sure ufc-fighters-statistics_cleaned.csv is in the same repo folder as app.py
    df = pd.read_csv("ufc-fighters-statistics_cleaned.csv")
    return df

df = load_data()

# ----------------------------
# Streamlit UI
# ----------------------------
st.set_page_config(page_title="UFC Fighters Comparison", layout="wide")

st.title("🥊 UFC Fighters Comparison Dashboard")
st.markdown(
    """
    Compare UFC fighters across different features (Reach, Win %, Loss %, etc.)  
    and calculate **longest consecutive win streaks**.
    """
)

# Sidebar filters
st.sidebar.header("🔍 Compare Fighters")
fighters = df["Name"].unique()
fighter1 = st.sidebar.selectbox("Select Fighter 1", fighters)
fighter2 = st.sidebar.selectbox("Select Fighter 2", fighters)

feature = st.sidebar.selectbox(
    "Select Feature to Compare",
    ["Win Percentage", "Loss Percentage", "Reach", "Height", "Weight"]
)

# ----------------------------
# Helper Functions
# ----------------------------
def calculate_win_streak(record):
    """
    Given a fighter's fight record string like 'W, W, L, W',
    calculate longest consecutive win streak.
    """
    if pd.isna(record):
        return 0
    results = record.split(",")
    max_streak, current = 0, 0
    for r in results:
        if r.strip() == "W":
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0
    return max_streak

# Precompute win streaks if "Record" column exists
if "Record" in df.columns:
    df["Longest Win Streak"] = df["Record"].apply(calculate_win_streak)

# ----------------------------
# Fighter Comparison
# ----------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{fighter1}")
    fighter1_data = df[df["Name"] == fighter1].iloc[0]
    st.write(f"**{feature}:** {fighter1_data.get(feature, 'N/A')}")
    if "Longest Win Streak" in df.columns:
        st.write(f"**Longest Win Streak:** {fighter1_data['Longest Win Streak']}")

with col2:
    st.subheader(f"{fighter2}")
    fighter2_data = df[df["Name"] == fighter2].iloc[0]
    st.write(f"**{feature}:** {fighter2_data.get(feature, 'N/A')}")
    if "Longest Win Streak" in df.columns:
        st.write(f"**Longest Win Streak:** {fighter2_data['Longest Win Streak']}")

# ----------------------------
# Visualization
# ----------------------------
st.subheader("📊 Feature Comparison Chart")

fig, ax = plt.subplots(figsize=(6, 4))
sns.barplot(
    x=[fighter1, fighter2],
    y=[fighter1_data.get(feature, 0), fighter2_data.get(feature, 0)],
    palette="viridis",
    ax=ax
)
ax.set_ylabel(feature)
ax.set_title(f"{feature} Comparison")
st.pyplot(fig)

# ----------------------------
# Full Dataset Explorer
# ----------------------------
st.subheader("📂 Fighter Stats Data")
st.dataframe(df.head(50))
