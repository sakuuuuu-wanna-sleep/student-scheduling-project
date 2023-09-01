import csv


class Student:
    all_students = []

    def __init__(self, name, grade, advisor, list_of_requests):
        self.name = name
        self.grade = grade
        self.advisor = advisor
        self.list_of_requests = list_of_requests
        self.list_of_requests = [x for x in self.list_of_requests if x not in ["Anatomy and Physiology", "Life Skills", "Study Skills", "Independent Study", "", "Independent Study - The New Space Race"]]

        self.total_number_of_classes = 0
        self.schedule = {
            "Q1/3 P1": None,
            "Q1/3 P2": None,
            "Q1/3 P3": None,
            "Q1/3 P4": None,
            "Q2/4 P1": None,
            "Q2/4 P2": None,
            "Q2/4 P3": None,
            "Q2/4 P4": None,
        }
        self.class_not_meet = 0
        Student.all_students.append(self)

    def __repr__(self):
        return f"{self.name} in grade {self.grade} in {self.advisor}'s advisory request for {self.list_of_requests}"

    @classmethod
    def instantiate_from_csv(cls, filename: str):
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            items = list(reader)
            #print(items)
        for item in items:
            Student(
                name=item.get("name"),
                grade=item.get("grade"),
                advisor=item.get("advisor"),
                list_of_requests=[item.get("req1"), item.get("req2"), item.get("req3"), item.get("req4"), item.get("req5"), item.get("req6"), item.get("req7"), item.get("req8")]
            )
    @classmethod
    def scheduling(cls):
        count = 0
        for student in Student.all_students:
            for request in student.list_of_requests:
                options = ClassSection.all_classes[request]
                for option in options:
                    if len(option.roster) < option.class_size:
                        if request in ["Humanities 10", "American Studies: English"]:
                            if student.schedule[option.period] is None:
                                student.schedule[option.period] = option
                                student.schedule["Q2/4" + option.period[option.period.index(" "):]] = option
                                option.roster.append(student)
                                break
                        else:
                            if student.schedule[option.period] is None:
                                student.schedule[option.period] = option
                                option.roster.append(student)
                                break
            enrolled_courses = [x for x in student.schedule.values() if x is not None]
            if len(student.list_of_requests) > len(enrolled_courses):
                count += 1
        return count

    @classmethod
    def print_report(cls):
        for student in Student.all_students:
            print(student.name)
            for a in student.schedule:
                print(f"\t{a}: {student.schedule[a]}")
            print()
        for x in ClassSection.all_classes:
            for i in range(len(ClassSection.all_classes[x])):
                print(
                    f"Class {ClassSection.all_classes[x][i].class_name} teach by {ClassSection.all_classes[x][i].teacher}, period {ClassSection.all_classes[x][i].period}")
                print(
                    f"{len(ClassSection.all_classes[x][i].roster)} students in the class with maximum {ClassSection.all_classes[x][i].class_size} students.")




class ClassSection:

    all_classes = {}

    def __init__(self, class_name, teacher, period, class_size):
        self.class_name = class_name
        self.teacher = teacher
        self.period = period
        self.class_size = class_size
        self.roster = []

        try:
            ClassSection.all_classes[self.class_name].append(self)
        except:
            ClassSection.all_classes[self.class_name] = []
            ClassSection.all_classes[self.class_name].append(self)

    def __repr__(self):
        return f"{self.class_name} teach by {self.teacher} in {self.period}"

    @classmethod
    def instantiate_from_csv(cls, filename: str):
        with open(filename, "r") as f:
            reader = csv.DictReader(f)
            items = list(reader)
            # print(items)
        for item in items:
            ClassSection(
                class_name=item.get("name"),
                teacher=item.get("teacher"),
                period=item.get("period"),
                class_size=int(item.get("class size"))
            )


if __name__ == '__main__':
    Student.instantiate_from_csv("sample student data no names.csv")
    ClassSection.instantiate_from_csv("sample class data.csv")
    num_imperfect = Student.scheduling()
    print(str(num_imperfect) + " students were not perfect")
    print(str((num_imperfect/len(Student.all_students))*100) + " percent of student were imperfect")
    Student.print_report()





