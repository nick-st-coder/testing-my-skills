
#include <iostream>
#include <vector>
#include <string>
#include <memory>
using namespace std;

class Student {
private:
    string name;
    int age;
    float grade;

public:
    Student(string name, int age, float grade)
        : name(name), age(age), grade(grade) {}

    void display() const {
        cout << "Name: " << name << endl;
        cout << "Age: " << age << endl;
        cout << "Grade: " << grade << endl;
    }

    bool isEligibleForScholarship() const {
        return grade >= 4.5;
    }

    void updateGrade(float newGrade) {
        grade = newGrade;
    }

    string getName() const {
        return name;
    }
};

class StudentList {
private:
    vector<shared_ptr<Student>> students;

public:
    void addStudent(shared_ptr<Student> student) {
        students.push_back(student);
    }

    void removeStudent(const string& studentName) {
        for (auto it = students.begin(); it != students.end(); ++it) {
            if ((*it)->getName() == studentName) {
                students.erase(it);
                return;
            }
        }
    }

    void getScholarshipCandidates() const {
        cout << "\nStudents with scholarship:" << endl;
        for (const auto& student : students) {
            if (student->isEligibleForScholarship()) {
                student->display();
            }
        }
    }

    void displayAllStudents() const {
        cout << "\nAll students:" << endl;
        for (const auto& student : students) {
            student->display();
        }
    }
};

int main() {
    StudentList list;

    auto student1 = make_shared<Student>("Nikita Babukh", 16, 4.37);
    auto student2 = make_shared<Student>("Yahe Lape", 15, 4.22);
    auto student3 = make_shared<Student>("Cumil Cumalcz", 15, 6.0);

    list.addStudent(student1);
    list.addStudent(student2);
    list.addStudent(student3);

    list.displayAllStudents();

    student1->updateGrade(5.6);

    cout << "\nAfter changes:";
    list.displayAllStudents();

    list.getScholarshipCandidates();

    list.removeStudent("Cumil Cumalcz");

    cout << "\nAfter remove:";
    list.displayAllStudents();

    return 0;
}
