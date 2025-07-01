class GPAError(Exception):
    def __init__(self,message):
        super().__init__(message)

class GPA:
    def __init__(self):
        self.semesterPoints = 0
        self.semesterHours = 0
        self.prevGPA = 0
        self.prevHours = 0
        self.gradePoint = {"A+": 4, "A": 3.75, "B+": 3.5, "B": 3, "C+": 2.5, "C": 2, "D+": 1.5, "D": 1, "F": 0}

    def calculate_semester_gpa(self, grades_credits):
        try:
         for grade, credit in grades_credits:
            if credit < 0:
                raise GPAError("credit hours value can't be negative")
            if grade in self.gradePoint:
                self.semesterPoints += self.gradePoint[grade] * credit
                self.semesterHours += credit
         if self.semesterHours == 0:
            raise GPAError("please enter valid values")
         return round(self.semesterPoints / self.semesterHours, 3)
        except (ValueError, TypeError):
            raise GPAError("please enter valid value")



    def calculate_cumulative_gpa(self, prev_gpa, prev_credits):
        try:
            if (prev_credits + self.semesterHours) == 0:
                return 0.0
            if  prev_gpa < 0 or prev_credits < 0 or self.semesterPoints<0 or self.semesterHours < 0:
                raise GPAError("you can't enter a negative value")

            cumulativeGPA =  round(((prev_gpa * prev_credits) + self.semesterPoints) / (prev_credits + self.semesterHours), 3)
            if cumulativeGPA < 0:
                raise GPAError("please enter valid values")
            return cumulativeGPA

        except (ValueError, TypeError):
            raise GPAError("please enter valid values")
