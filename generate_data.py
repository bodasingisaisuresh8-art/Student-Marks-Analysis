"""
generate_data.py
Creates a sample student marks dataset (CSV) for the analysis project.
Replace this with your own real dataset (e.g., from your school/college)
by just pointing analysis.py to your CSV file instead.
"""

import pandas as pd
import numpy as np

np.random.seed(42)

num_students = 60
subjects = ["Maths", "Science", "English", "Computer", "History"]

names = [f"Student_{i+1}" for i in range(num_students)]

data = {"Student_Name": names}

# Generate correlated-ish marks (students who are good tend to be
# decently good across subjects, with some randomness per subject)
base_ability = np.random.normal(65, 15, num_students)

for subject in subjects:
    noise = np.random.normal(0, 10, num_students)
    marks = base_ability + noise
    marks = np.clip(marks, 0, 100).round().astype(int)
    data[subject] = marks

df = pd.DataFrame(data)

df.to_csv("/home/claude/student_marks_project/data/student_marks.csv", index=False)
print("Dataset created with shape:", df.shape)
print(df.head())
