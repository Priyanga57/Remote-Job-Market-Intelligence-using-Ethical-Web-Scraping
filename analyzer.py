import pandas as pd
import matplotlib.pyplot as plt

print("Loading cleaned dataset...")
df = pd.read_csv("remoteok_jobs_cleaned.csv")
print("Total jobs:", len(df))

# Remove fake job titles
df = df[~df["job_title"].str.contains("current openings", case=False, na=False)]

# Prepare skills
df_skills = df.copy()
df_skills["skills"] = df_skills["skills"].str.split(",")
df_skills = df_skills.explode("skills")
df_skills["skills"] = df_skills["skills"].str.strip().str.lower()
df_skills = df_skills[df_skills["skills"] != ""]

bad_skills = ["software", "engineer", "senior", "developer", "web", "code", "system", "manager"]
df_skills = df_skills[~df_skills["skills"].isin(bad_skills)]

# Top skills
top_skills = df_skills["skills"].value_counts().head(10)
plt.figure(figsize=(10,6))
top_skills.plot(kind="bar")
plt.title("Top 10 Skills")
plt.tight_layout()
plt.savefig("top_skills.png", dpi=300)
plt.close()

# Posting freshness
def classify_posting(x):
    if isinstance(x, str):
        if "d" in x:
            return "Recent"
        elif "mo" in x:
            return "Old"
    return "Unknown"

df["posting_age_group"] = df["job_type"].apply(classify_posting)
df["posting_age_group"].value_counts().plot(kind="bar")
plt.tight_layout()
plt.savefig("job_posting_freshness.png", dpi=300)
plt.close()

# Top job titles
df["job_title"].value_counts().head(10).plot(kind="barh")
plt.tight_layout()
plt.savefig("top_job_titles.png", dpi=300)
plt.close()

# Skill frequency
df_skills["skills"].value_counts().head(15).plot(kind="barh")
plt.tight_layout()
plt.savefig("skill_frequency_comparison.png", dpi=300)
plt.close()

print("Analysis complete.")
