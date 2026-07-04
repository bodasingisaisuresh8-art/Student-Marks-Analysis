"""
analysis.py
Student Marks Analysis Project using Pandas + Matplotlib

Steps:
1. Load data
2. Compute Total, Average, Grade, Pass/Fail
3. Subject-wise & student-wise statistics
4. Visualizations:
   - Bar chart: average marks per subject
   - Histogram: distribution of total marks
   - Pie chart: grade distribution
   - Bar chart: top 10 students
   - Heatmap: correlation between subjects
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# ---------------------------------------------------------
# 1. LOAD DATA
# ---------------------------------------------------------
df = pd.read_csv("student_marks.csv")
subjects = ["Maths", "Science", "English", "Computer", "History"]

# ---------------------------------------------------------
# 2. DERIVED COLUMNS
# ---------------------------------------------------------
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1).round(2)


def get_grade(avg):
    if avg >= 90:
        return "A+"
    elif avg >= 80:
        return "A"
    elif avg >= 70:
        return "B"
    elif avg >= 60:
        return "C"
    elif avg >= 40:
        return "D"
    else:
        return "F"


df["Grade"] = df["Average"].apply(get_grade)
df["Result"] = df["Grade"].apply(lambda g: "Fail" if g == "F" else "Pass")

# ---------------------------------------------------------
# 3. SUMMARY STATISTICS
# ---------------------------------------------------------
print("=" * 55)
print("STUDENT MARKS ANALYSIS - SUMMARY")
print("=" * 55)

print(f"\nTotal Students        : {len(df)}")
print(f"Class Average (%)     : {df['Average'].mean():.2f}")
print(f"Highest Average       : {df['Average'].max():.2f} "
      f"({df.loc[df['Average'].idxmax(), 'Student_Name']})")
print(f"Lowest Average        : {df['Average'].min():.2f} "
      f"({df.loc[df['Average'].idxmin(), 'Student_Name']})")
print(f"Pass Percentage       : {(df['Result'] == 'Pass').mean() * 100:.1f}%")

print("\nSubject-wise Average Marks:")
subject_avg = df[subjects].mean().round(2).sort_values(ascending=False)
print(subject_avg)

print("\nGrade Distribution:")
print(df["Grade"].value_counts().sort_index())

print("\nTop 5 Students:")
print(df.sort_values("Average", ascending=False)[["Student_Name", "Average", "Grade"]].head(5)
      .to_string(index=False))

# Save the enriched dataset
df.to_csv("student_marks_analyzed.csv", index=False)

# ---------------------------------------------------------
# 4. VISUALIZATIONS
# ---------------------------------------------------------
plt.style.use("seaborn-v0_8-whitegrid")
import os

OUT = "output"
os.makedirs(OUT, exist_ok=True)

# --- Chart 1: Average marks per subject (bar chart) ---
plt.figure(figsize=(8, 5))
subject_avg.plot(kind="bar", color="#4C72B0")
plt.title("Average Marks per Subject")
plt.ylabel("Average Marks")
plt.xlabel("Subject")
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(f"{OUT}/1_subject_avg_bar.png", dpi=150)
plt.close()

# --- Chart 2: Distribution of total marks (histogram) ---
plt.figure(figsize=(8, 5))
plt.hist(df["Total"], bins=10, color="#55A868", edgecolor="black")
plt.title("Distribution of Total Marks")
plt.xlabel("Total Marks (out of 500)")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(f"{OUT}/2_total_marks_histogram.png", dpi=150)
plt.close()

# --- Chart 3: Grade distribution (pie chart) ---
grade_counts = df["Grade"].value_counts().sort_index()
plt.figure(figsize=(6, 6))
plt.pie(grade_counts, labels=grade_counts.index, autopct="%1.1f%%",
        startangle=90, colors=plt.cm.Set3.colors)
plt.title("Grade Distribution")
plt.tight_layout()
plt.savefig(f"{OUT}/3_grade_pie_chart.png", dpi=150)
plt.close()

# --- Chart 4: Top 10 students (bar chart) ---
top10 = df.sort_values("Average", ascending=False).head(10)
plt.figure(figsize=(9, 5))
plt.bar(top10["Student_Name"], top10["Average"], color="#C44E52")
plt.title("Top 10 Students by Average Marks")
plt.ylabel("Average Marks")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig(f"{OUT}/4_top10_students.png", dpi=150)
plt.close()

# --- Chart 5: Correlation heatmap between subjects ---
corr = df[subjects].corr()
plt.figure(figsize=(7, 6))
im = plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(im, label="Correlation")
plt.xticks(range(len(subjects)), subjects, rotation=45, ha="right")
plt.yticks(range(len(subjects)), subjects)
for i in range(len(subjects)):
    for j in range(len(subjects)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", color="black")
plt.title("Correlation Between Subjects")
plt.tight_layout()
plt.savefig(f"{OUT}/5_correlation_heatmap.png", dpi=150)
plt.close()

print("\nAll charts saved to:", OUT)