import pandas as pd
import matplotlib.pyplot as plt
import textwrap


df = pd.read_csv('/workspaces/oaksurvey/data.csv')
print(df.columns)

#standardize the column names to lowercase
df.columns = df.columns.str.lower().str.replace(" ", "_")
# Check and convert the data types
# --- check the data type of all columns
# --- cleaned_gdf.info()
df.info()

# change the column name from "on_a_scale_of_1_to_5,_how_important_of_an_issue_to_you_is_sea_level_rise_and_flooding?" to "flooding_impscale"
df = df.rename(columns={
    "how_frequently_are_you_impacted_by_flooding?":"flooding_frequency",
    "how_have_you_been_impacted_by_flooding?":"flooding_impact",
    "on_a_scale_of_1_to_5,_how_important_of_an_issue_to_you_is_sea_level_rise_and_flooding?": "flooding_impscale",
    "what_matters_most_to_you_when_planning_for_future_flooding?":"plan_goal",
    "how_do_you_usually_get_around_oakland?":"transport",
    "if_there_was_a_flood_or_emergency_in_your_neighborhood,_how_would_you_get_to_safety?":"emergency_transport",
    "do_you_live_or_work_in_oakland?":"live_work",
    "what_race_or_ethnicity_do_you_identify_with?_please_check_all_that_apply":"race",
    "what_is_your_gender_identity?":"gender",
    "what_neighborhood_do_you_live_in?":"neighborhood"
})
# Rename columns
df_clean = df.rename(columns={
    "how_frequently_are_you_impacted_by_flooding?": "flooding_frequency",
    "how_have_you_been_impacted_by_flooding?": "flooding_impact",
    "on_a_scale_of_1_to_5,_how_important_of_an_issue_to_you_is_sea_level_rise_and_flooding?": "flooding_impscale",
    "what_matters_most_to_you_when_planning_for_future_flooding?": "plan_goal",
    "how_do_you_usually_get_around_oakland?": "transport",
    "if_there_was_a_flood_or_emergency_in_your_neighborhood,_how_would_you_get_to_safety?": "emergency_transport",
    "do_you_live_or_work_in_oakland?": "live_work",
    "what_race_or_ethnicity_do_you_identify_with?_please_check_all_that_apply": "race",
    "what_is_your_gender_identity?": "gender",
    "what_neighborhood_do_you_live_in?": "neighborhood"
})

# Keep only the selected columns
columns_to_keep = [
    "flooding_frequency",
    "flooding_impact",
    "flooding_impscale",
    "plan_goal",
    "transport",
    "emergency_transport",
    "live_work",
    "race",
    "gender",
    "neighborhood"
]

df_clean = df_clean[columns_to_keep]

# Preview the new dataset
# df_clean.info()

# flooding_frequency analysis
# View unique responses
# print(df_clean["flooding_frequency"].unique())

# "Al menos una vez al mes durante la temporada de lluvias" = 'At least once a month during the rainy season',
# "至少每年一次" = "At least once a year"
# "At least once a year (Rain)" = "At least once a year"

df_clean["flooding_frequency"] = df_clean["flooding_frequency"].replace({
    "Al menos una vez al mes durante la temporada de lluvias":
        "At least once a month during the rainy season",
    "至少每年一次":
        "At least once a year",
    "At least once a year (Rain)":
        "At least once a year",
    "At least once a month during the rainy season - daily":
        "At least once a month during the rainy season"
})
df_clean["flooding_frequency"] = (
    df_clean["flooding_frequency"]
    .str.split(", ")
)

# "At least once a month during the rainy season, At least once a year" split to two answers - "At least once a month during the rainy season" & "At least once a year"
df_clean = df_clean.explode("flooding_frequency")

print(df_clean["flooding_frequency"].value_counts(dropna=False))
frequency_counts = df_clean["flooding_frequency"].value_counts()

# Calculate percentages
frequency_percentages = frequency_counts / frequency_counts.sum() * 100

# Count responses
frequency_counts = df_clean["flooding_frequency"].value_counts()

# Calculate percentages
frequency_counts = df_clean["flooding_frequency"].value_counts()
#-----------------------------------------------------------
# Matte color palette
colors = ["#A3B18A", "#8DA9B6", "#D4A373", "#C08475"]
# bar chart
fig, ax = plt.subplots(figsize=(10, 6))

bars = ax.bar(
    frequency_counts.index,
    frequency_counts.values,
    color="#8DA9B6",
    width=0.65
)

# Title and labels
ax.set_title(
    "How Frequently Are You Impacted by Flooding?",
    fontsize=15,
    fontweight="medium",
    pad=20
)
ax.set_ylabel("Number of Respondents", fontsize=11)
ax.set_xlabel("")

# Add value labels
ax.bar_label(bars, padding=5, fontsize=11)

# Clean up graph appearance
ax.set_facecolor("#FAF9F6")
fig.patch.set_facecolor("#FAF9F6")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)

ax.grid(axis="y", linestyle="--", alpha=0.25)
ax.set_axisbelow(True)

# Wrap long x-axis labels into two lines
wrapped_labels = [
    textwrap.fill(label, width=25)
    for label in frequency_counts.index
]

ax.set_xticks(range(len(frequency_counts)))
ax.set_xticklabels(
    wrapped_labels,
    rotation=0,
    ha="center",
    fontsize=10
)

ax.set_ylabel("Number of Respondents", fontsize=10, labelpad=10)

plt.tight_layout()
plt.savefig("flooding_frequency_counts.png", dpi=300,
            bbox_inches="tight", facecolor="#FAF9F6")

#-----------------------------------------------------------
# Donut chart
fig, ax = plt.subplots(figsize=(7, 6))

# Pie chart
wedges, texts, autotexts = ax.pie(
    frequency_counts.values,
    labels=None,
    colors=colors,
    autopct="%1.1f%%",
    startangle=90,
    counterclock=False,
    pctdistance=0.65,
    radius=1.15,
    wedgeprops={
        "edgecolor": "#FAF9F6",
        "linewidth": 2
    },
    textprops={
        "fontsize": 11,
        "color": "#444444"
    }
)

# Style percentage labels
for autotext in autotexts:
    autotext.set_fontsize(11)
    autotext.set_fontweight("medium")
    autotext.set_color("#444444")

# Background
fig.patch.set_facecolor("#FAF9F6")
ax.set_facecolor("#FAF9F6")

# Legend
ax.legend(
    wedges,
    frequency_counts.index,
    title="How Frequently Are You Impacted by Flooding?",
    loc="center left",
    bbox_to_anchor=(0.95, 0.5),
    frameon=False,
    fontsize=10,
    title_fontsize=11,
)

ax.axis("equal")

plt.tight_layout()

plt.savefig(
    "flooding_frequency_percentage.png",
    dpi=300,
    bbox_inches="tight",
    facecolor="#FAF9F6"
)

