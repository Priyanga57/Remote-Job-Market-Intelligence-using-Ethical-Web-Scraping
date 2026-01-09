import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Loading cleaned dataset...")
df = pd.read_csv("remoteok_jobs_cleaned.csv")
print("Total jobs:", len(df))


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
# plt.savefig("top_skills.png", dpi=300)
plt.close()

# Posting freshness
def classify_posting(x):
    if isinstance(x, str):
        if "d" in x:
            return "Recent"
        elif "mo" in x:
            return "Old"
    return "Unknown"
    
# Remove fake job titles
df = df[~df["job_title"].str.contains("current openings", case=False, na=False)]

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
# plt.savefig("skill_frequency_comparison.png", dpi=300)
plt.close()

print("Analysis complete.")


# Visualization Part

df_copy=df.copy()

# 1. top skills

# Prepare skills
df_copy['skills']=df_copy['skills'].str.split(', ')
df_copy = df_copy.explode("skills")
df_copy = df_copy[df_copy["skills"] != ""]
skills_not_required = ["software", "engineer", "senior", "developer", "web", "code", "system", "manager",",","job or 100% money back"]
df_copy = df_copy[~df_copy["skills"].isin(skills_not_required)]

# Get top 10
top_skills=df_copy['skills'].value_counts().head(10)

# creating graph
plt.figure(figsize=(12, 6))
ax=sns.barplot(
    x=top_skills.index, 
    y=top_skills.values, 
    palette='Blues', 
    hue=top_skills.index )
for i, value in enumerate(top_skills.values):
    ax.text(i,value,str(value),ha='center',va='bottom',fontsize=10)
plt.title('Top 10 Most Demanded Skills in RemoteOk Jobs', fontsize=14, fontweight='bold')
plt.xlabel('Skill', fontsize=12)
plt.ylabel('Number of Job Postings', fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("top_skills.png", dpi=300)
plt.close()
print('Skills graph saved')

# 2.Job Type Distribution 

# Prepare Job type
def categorize_job_type(x):
    if 'h' in x:
        return '<15d'
    elif 'd' in x:
        days=int(x.replace('d',''))
        if days < 15:
            return '<15d'
        else:
            return '<1mo'
    elif x=='1mo':
        return '1mo'
    elif x=='2mo':
        return '2mo'
    elif x=='3mo':
        return '3mo'
    else:
        return 'other'

df_copy['job_type_group']=df_copy['job_type'].apply(categorize_job_type)

# Count job types
job_type_counts = df_copy['job_type_group'].value_counts()

# Create pie chart
plt.figure(figsize=(12, 6))
plt.pie(job_type_counts, labels=job_type_counts.index, autopct='%1.1f%%', startangle=90)
plt.title('Job Type Distribution', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('job_type_distribution.png', dpi=300)
plt.close()
print('Job Type Distribution Saved')


# 3. top job titles

# Remove fake job titles
df_copy = df_copy[~df_copy["job_title"].str.contains("current openings", case=False, na=False)]
# Create horizontal bar chart
job_title_count=df_copy['job_title'].value_counts().head(10)
job_title_count.plot(kind='barh', color='skyblue')
# plotting graph
plt.title('Top 10 Job Title')
plt.xlabel('Number Of Posting')
plt.ylabel('Top Job Title')
plt.tight_layout()
plt.savefig('top_job_titles.png', dpi=300)
plt.close()
print('Top Job Title Saved')

# 4. skill frequency comparison

# Skill frequency
skill_frequency=df_copy["skills"].value_counts().head(15)
# plotting graph
skill_frequency.plot(kind='barh', color='green')
plt.title('Skill Frequency Comparison')
plt.xlabel('Frequency (Count)')
plt.ylabel('Top Skills')
plt.tight_layout()
plt.savefig('skill_frequency_comparison.png', dpi=300)
plt.close()
print('Skill frequency Comparison Saved')

# 5. Top Most Frequent Job Location

# prepare data
import re
def clean_location(location_str):
    if isinstance(location_str, str):
        cleaned = location_str.encode('ascii', 'ignore').decode('ascii')
        cleaned = re.sub(r'[\W_]+', ' ', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned.lower()
    return location_str    
# Apply the enhanced cleaning function
df_copy['location_normalized'] = df_copy['location'].apply(clean_location)
generic_locations_cleaned = [clean_location(loc) for loc in ['upgrade to premium to see salary', 'probably worldwide', 'worldwide']]
filtered_locations_normalized = df_copy[~df_copy['location_normalized'].isin(generic_locations_cleaned)]['location_normalized']
top_locations= filtered_locations_normalized.value_counts().head(10)
# Plotting graph
plt.figure(figsize=(12, 6))
ax=sns.barplot(
    x=top_locations.index, 
    y=top_locations.values, 
    hue=top_locations.index, 
    palette='magma', 
    legend=False)
# Add numeric labels above bars
for i, value in enumerate(top_locations.values):
    ax.text(i,value,str(value),ha='center',va='bottom',fontsize=10)
plt.title('Top 10 Most Frequent Job Locations')
plt.xlabel('Location')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_job_location.png', dpi=300)
plt.close()
print('Top Location Saved')


# 6. Top Hiring Companies

top_companies= df_copy['company'].value_counts().head(10)
# Plotting the graph
plt.figure(figsize=(12, 6))
ax=sns.barplot(
    x=top_companies.index, 
    y=top_companies.values, 
    hue=top_companies.index, 
    palette='magma', 
    legend=False)
# Add numeric labels above bars
for i, value in enumerate(top_companies.values):
    ax.text(i,value,str(value),ha='center',va='bottom',fontsize=10)
plt.title('Top Hiring Companies')
plt.xlabel('Companies')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('top_hiring_company.png', dpi=300)
plt.close()
print('Top hiring Companies saved')

# 7. Job trend over time

df_copy['date_posted'] = pd.to_datetime(df_copy['date_posted'])
job_posted=df_copy['date_posted'].dt.date.value_counts().sort_index()
# Plotting the graph
job_posted.plot(figsize=(12,6))
plt.title('Job Posting Trend Over Time')
plt.ylabel('Number of Jobs')
plt.tight_layout()
plt.savefig('job_trend.png', dpi=300)
plt.close()
print('Job Trend saved')







