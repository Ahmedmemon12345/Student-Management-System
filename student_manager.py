import json
import os
import streamlit as st
from typing import List, Dict, Optional

class Student:
    def __init__(self, student_id: str, name: str, age: int, grade: str, performance: str):
        self.student_id = student_id.strip()
        self.name = name.strip()
        self.age = age
        self.grade = grade
        self.performance = performance

    def to_dict(self) -> Dict:
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "grade": self.grade,
            "performance": self.performance
        }

    @classmethod
    def from_dict(cls, data: Dict):
        return cls(
            data["student_id"],
            data["name"],
            data["age"],
            data["grade"],
            data["performance"]
        )


class StudentManager:
    def __init__(self, file_path: str = "data/students.json"):
        self.file_path = file_path
        self.students: List[Student] = self.load_students()

    def load_students(self) -> List[Student]:
        if not os.path.exists(self.file_path):
            os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return [Student.from_dict(s) for s in data]
        except:
            return []

    def save_students(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump([s.to_dict() for s in self.students], f, indent=4)

    def add_student(self, student: Student):
        if any(s.student_id == student.student_id for s in self.students):
            raise ValueError("Student ID already exists!")
        self.students.append(student)
        self.save_students()

    def update_student(self, student_id: str, updated_data: Dict) -> bool:
        for student in self.students:
            if student.student_id == student_id:
                for key, value in updated_data.items():
                    if hasattr(student, key):
                        setattr(student, key, value)
                self.save_students()
                return True
        return False

    def delete_student(self, student_id: str) -> bool:
        initial = len(self.students)
        self.students = [s for s in self.students if s.student_id != student_id]
        if len(self.students) < initial:
            self.save_students()
            return True
        return False

    def list_students(self) -> List[Student]:
        return self.students

    def search_students(self, query: str) -> List[Student]:
        query = query.lower().strip()
        return [
            s for s in self.students
            if query in s.name.lower() or query in s.student_id.lower()
        ]

    def filter_students(
        self,
        min_age: Optional[int] = None,
        max_age: Optional[int] = None,
        grade: Optional[str] = None,
        performance: Optional[str] = None,
    ) -> List[Student]:
        filtered = self.students[:]
        if min_age is not None:
            filtered = [s for s in filtered if s.age >= min_age]
        if max_age is not None:
            filtered = [s for s in filtered if s.age <= max_age]
        if grade:
            filtered = [s for s in filtered if s.grade == grade]
        if performance:
            filtered = [s for s in filtered if s.performance == performance]
        return filtered


def display_students(students: List[Student]):
    if not students:
        st.info("No students found.")
        return

    data = [
        {
            "Student ID": s.student_id,
            "Name": s.name,
            "Age": s.age,
            "Grade": s.grade,
            "Performance": s.performance,
        }
        for s in students
    ]
    st.dataframe(data, use_container_width=True)