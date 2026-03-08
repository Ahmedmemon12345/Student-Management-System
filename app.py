import streamlit as st
import student_manager # type: ignore
from forms import add_student_form, update_student_form, delete_student_form, search_filter_form # type: ignore

def main():
    manager = student_manager.StudentManager("data/students.json")

    st.title("Student Management System")

    menu = ["List Students", "Add Student", "Update Student", "Delete Student", "Search/Filter Students"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "List Students":
        st.subheader("All Students")
        students = manager.list_students()
        student_manager.display_students(students)

    elif choice == "Add Student":
        st.subheader("Add New Student")
        add_student_form(manager)

    elif choice == "Update Student":
        st.subheader("Update Student")
        update_student_form(manager)

    elif choice == "Delete Student":
        st.subheader("Delete Student")
        delete_student_form(manager)

    elif choice == "Search/Filter Students":
        st.subheader("Search and Filter Students")
        search_filter_form(manager)

if __name__ == "__main__":
    main()