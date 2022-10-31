def mean_grade_student(students, course):
    cnt_hw = 0
    grade_hw = 0
    for student in students:
        if isinstance(student, Student) and course in student.grades:
            cnt_hw += len(student.grades[course])
            grade_hw += sum(student.grades[course])
    return 0 if not cnt_hw else grade_hw/cnt_hw


def mean_grade_lecturer(lecturers, course):
    cnt_hw = 0
    grade_hw = 0
    for lecturer in lecturers:
        if isinstance(lecturer, Lecturer) and course in lecturer.courses_attached:
            cnt_hw += len(lecturer.courses_attached[course])
            grade_hw += sum(lecturer.courses_attached[course])
    return 0 if not cnt_hw else grade_hw/cnt_hw


class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
    
    def rate_lector(self, lector, course, grade):
        if isinstance(lector, Lecturer) and course in self.courses_in_progress and course in lector.courses_attached:
            if course in lector.courses_attached:
                lector.courses_attached[course].append(grade)
            else:
                lector.courses_attached[course] = [grade]
    
    def __str__(self):
        grades = [[len(v), sum(v)] for v in self.grades.values()]
        _str_ = f'Имя: {self.name}\n'
        _str_ += f'Фамилия: {self.surname}\n'
        _str_ += f'Средняя оценка за домашние задания: {sum(map(lambda x: x[1], grades))/sum(map(lambda x: x[0], grades))}\n'
        _str_ += f'Курсы в процессе изучения: {", ".join(self.courses_in_progress)}\n'
        _str_ += f'Завершенные курсы: {", ".join(self.finished_courses)}\n'
        return _str_
    
    def __eq__(self, other): 
        if not isinstance(other, Student):
            return 'Разные классы'
        self_grades = [[len(v), sum(v)] for v in self.grades.values()]
        mean_self_grade = sum(map(lambda x: x[1], self_grades))/sum(map(lambda x: x[0], self_grades))
        other_grades = [[len(v), sum(v)] for v in other.grades.values()]
        mean_other_grade = sum(map(lambda x: x[1], other_grades))/sum(map(lambda x: x[0], other_grades))
        
        return mean_self_grade == mean_other_grade
                    
        
class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        _str_ = f'Имя: {self.name}\n'
        _str_ += f'Фамилия: {self.surname}\n'
        if isinstance(self, Lecturer):
            grades = [[len(v), sum(v)] for v in self.courses_attached.values()]
            _str_ += f'Средняя оценка за лекции: {sum(map(lambda x: x[1], grades))/sum(map(lambda x: x[0], grades))}\n'
        return _str_

class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.courses_attached = {}
    
    def __eq__(self, other): 
        if not isinstance(other, Lecturer):
            return 'Разные классы'
        self_grades = [[len(v), sum(v)] for v in self.courses_attached.values()]
        mean_self_grade = sum(map(lambda x: x[1], self_grades))/sum(map(lambda x: x[0], self_grades))
        other_grades = [[len(v), sum(v)] for v in other.courses_attached.values()]
        mean_other_grade = sum(map(lambda x: x[1], other_grades))/sum(map(lambda x: x[0], other_grades))
        
        return mean_self_grade == mean_other_grade
        
class Reviewer(Mentor):
        
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'


if __name__ == "__main__":
    first_student = Student('Ruoy', 'Eman', 'female')
    first_student.courses_in_progress += ['Python']
    first_student.courses_in_progress += ['Git']
    first_student.finished_courses += ['Введение в программирование']

    second_student = Student('Ben', 'Affleck', 'male')
    second_student.courses_in_progress += ['Python']
    second_student.courses_in_progress += ['Strange']

    third_student = Student('Nicolas', 'Cage', 'male')
    third_student.courses_in_progress += ['Python']
    third_student.courses_in_progress += ['Bad Moovie']
    third_student.finished_courses += ['Bad Moovie']

    first_lecturer = Lecturer('Some', 'Buddy')
    first_lecturer.courses_attached['Python'] = []
    first_lecturer.courses_attached['Git'] = []

    second_lecturer = Lecturer('Dwayne', 'Johnson')
    second_lecturer.courses_attached['Python'] = []
    second_lecturer.courses_attached['Strange'] = []
    second_lecturer.courses_attached['Bad Moovie'] = []

    first_reviewer = Reviewer('Some', 'Buddy')
    first_reviewer.courses_attached += ['Python', 'Git']

    second_reviewer = Reviewer('Dwayne', 'Johnson')
    second_reviewer.courses_attached += ['Python', 'Strange', 'Bad Moovie']

    [first_reviewer.rate_hw(first_student, 'Python', 10) for _ in range(7)]
    first_reviewer.rate_hw(first_student, 'Python', 9)
    first_reviewer.rate_hw(first_student, 'Git', 10)
    first_reviewer.rate_hw(first_student, 'Git', 10)
     
    second_reviewer.rate_hw(second_student, 'Python', 5)
    second_reviewer.rate_hw(second_student, 'Strange', 10)
    second_reviewer.rate_hw(second_student, 'Strange', 10)
        
    [second_reviewer.rate_hw(third_student, 'Bad Moovie', 10) for _ in range(7)]
    second_reviewer.rate_hw(third_student, 'Bad Moovie', 9)
    second_reviewer.rate_hw(third_student, 'Python', 10)
    second_reviewer.rate_hw(third_student, 'Python', 10)

    [first_student.rate_lector(first_lecturer, 'Python', 10) for _ in range(7)]
    first_student.rate_lector(first_lecturer, 'Python', 9)
    first_student.rate_lector(first_lecturer, 'Git', 10)
    first_student.rate_lector(first_lecturer, 'Git', 10)

    second_student.rate_lector(second_lecturer, 'Python', 2)
    second_student.rate_lector(second_lecturer, 'Strange', 9)
    second_student.rate_lector(second_lecturer, 'Strange', 10)

    third_student.rate_lector(first_lecturer, 'Python', 10)

    third_student.rate_lector(second_lecturer, 'Python', 2)
    third_student.rate_lector(second_lecturer, 'Strange', 10)

    print(first_student)
    print(second_student)
    print(third_student)

    print(first_lecturer)
    print(second_lecturer)  

    print(first_student == second_student)

    print(first_student == third_student)

    print(mean_grade_student([first_student, second_student, third_student], 'Python'))

    print(mean_grade_lecturer([first_lecturer, second_lecturer], 'Python'))