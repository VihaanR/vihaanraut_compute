import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# -----------------------------
# Load Data
# -----------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("https://raw.githubusercontent.com/VihaanR/vihaanraut_compute/refs/heads/main/ML_Tasks/ufc-fighters-statistics.csv")
    return df

df = load_data()

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(
    page_title="UFC Fighter Comparison",
    page_icon="🥊",
    layout="wide"
)

st.title("🥊 UFC Fighter Comparison Dashboard")
st.markdown("""
Compare UFC fighters across different features (**Wins, Losses, Height, Reach, Striking, etc.**)  
Also check each fighter's **Longest Consecutive Win Streak** (if fight history available).
""")

# -----------------------------
# Helper Function – Longest Win Streak
# -----------------------------
def longest_win_streak(record_str):
    """
    Calculate the longest consecutive win streak from a fight history string.
    Example: "W W L W W W L" -> 3
    """
    if pd.isna(record_str):
        return 0
    results = record_str.split()
    max_streak, current = 0, 0
    for r in results:
        if r == "W":
            current += 1
            max_streak = max(max_streak, current)
        else:
            current = 0
    return max_streak

if "Fight_History" in df.columns:
    df["LongestWinStreak"] = df["Fight_History"].apply(longest_win_streak)

# -----------------------------
# Fighter Selection
# -----------------------------
fighters = sorted(df["name"].unique())

col1, col2 = st.columns(2)
with col1:
    fighter1 = st.selectbox("Select Fighter 1", fighters)
with col2:
    fighter2 = st.selectbox("Select Fighter 2", fighters)

# -----------------------------
# Feature Selection
# -----------------------------
feature_map = {
    "Wins": "wins",
    "Losses": "losses",
    "Draws": "draws",
    "Height (cm)": "height_cm",
    "Weight (kg)": "weight_in_kg",
    "Reach (cm)": "reach_in_cm",
    "Strikes Landed per Min": "significant_strikes_landed_per_minute",
    "Striking Accuracy %": "significant_striking_accuracy",
    "Strikes Absorbed per Min": "significant_strikes_absorbed_per_minute",
    "Strike Defense %": "significant_strike_defence",
    "Takedowns per 15 min": "average_takedowns_landed_per_15_minutes",
    "Takedown Accuracy %": "takedown_accuracy",
    "Takedown Defense %": "takedown_defense",
    "Submissions per 15 min": "average_submissions_attempted_per_15_minutes"
}

feature_label = st.selectbox("Select Feature to Compare", list(feature_map.keys()))
feature = feature_map[feature_label]

# -----------------------------
# Display Fighter Stats
# -----------------------------
def display_fighter_stats(fighter):
    stats = df[df["name"] == fighter].iloc[0]
    st.subheader(f"**{fighter}** 🥋")
    st.metric("Wins", int(stats["wins"]))
    st.metric("Losses", int(stats["losses"]))
    st.metric("Draws", int(stats["draws"]))
    st.metric("Height", f"{stats['height_cm']} cm")
    st.metric("Weight", f"{stats['weight_in_kg']} kg")
    st.metric("Reach", f"{stats['reach_in_cm']} cm")
    if "LongestWinStreak" in stats:
        st.metric("Longest Win Streak", int(stats["LongestWinStreak"]))

col1, col2 = st.columns(2)
with col1:
    display_fighter_stats(fighter1)
with col2:
    display_fighter_stats(fighter2)

# -----------------------------
# Visualization
# -----------------------------
st.markdown("### 📊 Feature Comparison")

f1_val = df.loc[df["name"]==fighter1, feature].values[0]
f2_val = df.loc[df["name"]==fighter2, feature].values[0]

fig, ax = plt.subplots(figsize=(6,4))
ax.bar([fighter1, fighter2], [f1_val, f2_val], color=["#1f77b4","#ff7f0e"])
ax.set_ylabel(feature_label)
ax.set_title(f"{feature_label} Comparison")
st.pyplot(fig)

# -----------------------------
# Extra: Fighter Table
# -----------------------------
st.markdown("### 📋 Fighter Stats Table")
st.dataframe(df[df["name"].isin([fighter1, fighter2])].set_index("name"))
