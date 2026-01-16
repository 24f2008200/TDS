from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS for GET requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# Load CSV data at startup
students_data = []

with open("students.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        students_data.append({
            "studentId": int(row["studentId"]),
            "class": row["class"]
        })


@app.get("/api")
def get_students(class_: list[str] = Query(default=None, alias="class")):
    """
    Returns all students, or filters by one or more class query parameters.
    Order is preserved from the CSV file.
    """
    if class_ is None:
        return {"students": students_data}

    filtered = [
        student
        for student in students_data
        if student["class"] in class_
    ]

    return {"students": filtered}
