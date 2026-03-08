import streamlit as st
from student_manager import Student, display_students


def add_student_form(manager):
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            student_id = st.text_input("Student ID*", placeholder="S001")
            name = st.text_input("Full Name*", placeholder="Ahmed Khan")
            age = st.number_input("Age*", min_value=5, max_value=30, step=1, value=18)
        with col2:
            grade = st.selectbox("Grade*", ["A", "B", "C", "D", "F"])
            performance = st.selectbox(
                "Performance*", ["Excellent", "Good", "Average", "Poor"]
            )

        submitted = st.form_submit_button("Add Student", type="primary")
        if submitted:
            if not student_id or not name:
                st.error("Student ID and Name are required!")
            else:
                try:
                    student = Student(student_id, name, int(age), grade, performance)
                    manager.add_student(student)
                    st.success(f"Student {student_id} added successfully! 🎉")
                    st.rerun()
                except ValueError as e:
                    st.error(str(e))


def update_student_form(manager):
    students = manager.list_students()
    if not students:
        st.warning("No students available to update.")
        return

    student_ids = [s.student_id for s in students]
    selected_id = st.selectbox("Select Student ID to Update", student_ids)

    student = next((s for s in students if s.student_id == selected_id), None)

    if student:
        with st.form("update_form"):
            new_name = st.text_input("New Name", value=student.name)
            new_age = st.number_input("New Age", min_value=5, max_value=30, value=student.age)
            new_grade = st.selectbox("New Grade", ["A", "B", "C", "D", "F"], index=["A","B","C","D","F"].index(student.grade))
            new_perf = st.selectbox(
                "New Performance",
                ["Excellent", "Good", "Average", "Poor"],
                index=["Excellent", "Good", "Average", "Poor"].index(student.performance),
            )

            if st.form_submit_button("Update Student", type="primary"):
                if not new_name:
                    st.error("Name is required!")
                else:
                    updated = {
                        "name": new_name.strip(),
                        "age": int(new_age),
                        "grade": new_grade,
                        "performance": new_perf,
                    }
                    if manager.update_student(selected_id, updated):
                        st.success("Student updated successfully! 🎉")
                        st.rerun()
                    else:
                        st.error("Update failed.")


def delete_student_form(manager):
    students = manager.list_students()
    if not students:
        st.warning("No students to delete.")
        return

    student_ids = [s.student_id for s in students]
    selected_id = st.selectbox("Select Student ID to Delete", student_ids)

    if st.button("Delete Student", type="primary"):
        if manager.delete_student(selected_id):
            st.success(f"Student {selected_id} deleted successfully!")
            st.rerun()
        else:
            st.error("Student not found.")


def search_filter_form(manager):
    st.subheader("Search & Filter Students")
    tab1, tab2 = st.tabs(["🔍 Search by Name/ID", "📊 Advanced Filter"])

    with tab1:
        query = st.text_input("Enter Name or Student ID")
        if st.button("Search", type="primary") and query:
            results = manager.search_students(query)
            display_students(results)

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            min_age = st.number_input("Minimum Age", min_value=5, max_value=30, value=5)
            grade = st.selectbox("Grade", ["All", "A", "B", "C", "D", "F"])
        with col2:
            max_age = st.number_input("Maximum Age", min_value=5, max_value=30, value=25)
            performance = st.selectbox(
                "Performance", ["All", "Excellent", "Good", "Average", "Poor"]
            )

        if st.button("Apply Filter", type="primary"):
            g = None if grade == "All" else grade
            p = None if performance == "All" else performance
            results = manager.filter_students(
                min_age=min_age, max_age=max_age, grade=g, performance=p
            )
            display_students(results)