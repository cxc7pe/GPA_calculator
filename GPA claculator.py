
from PyQt5.QtWidgets import(
    QApplication,QWidget,QVBoxLayout,QHBoxLayout,QPushButton,QTableWidget,QTableWidgetItem,
    QComboBox,QLabel,QCheckBox,QLineEdit,QGroupBox,QFormLayout,QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon

class GPACalculator(QWidget):
    class GPA:
        def __init__(self):
            self.semesterPoints = 0
            self.semesterHours = 0
            self.prevGPA = 0
            self.prevHours = 0
            self.gradePoint = {"A+": 4, "A": 3.75, "B+": 3.5, "B": 3, "C+": 2.5, "C": 2, "D+": 1.5, "D": 1, "F": 0}

        def calculate_semester_gpa(self, grades_credits):
            self.semesterPoints = 0
            self.semesterHours = 0
            for grade, credit in grades_credits:
                if grade in self.gradePoint:
                    self.semesterPoints += self.gradePoint[grade] * credit
                    self.semesterHours += credit
            if self.semesterHours == 0:
                return 0.0
            return round(self.semesterPoints / self.semesterHours, 3)

        def calculate_cumulative_gpa(self, prev_gpa, prev_credits):
            if (prev_credits + self.semesterHours) == 0:
                return 0.0
            return round(((prev_gpa * prev_credits) + self.semesterPoints) / (prev_credits + self.semesterHours), 3)


    def __init__(self):
        super().__init__()
        self.setWindowTitle(" GPA Calculator")
        self.setGeometry(100, 100, 700, 400)
        self.course_number = 1
        self.setWindowIcon(QIcon("ICON2-.png"))

        self.setStyleSheet("background-color: #f3efff;")

        self.layout=QVBoxLayout()
        self.setLayout(self.layout)

        #The title
        title_label = QLabel("GPA Calculator")
        title_font = QFont("Arial", 20, QFont.Bold)
        title_label.setStyleSheet("""
            font-size: 28px;
            font-weight: bold;
            color: #3d2c8d; 
            margin-bottom: 12px;
        """)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)

        self.layout.addWidget(title_label)


        #The table
        self.table=QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Course","Credits","Grade"])
        self.table.setMinimumHeight(250)
        self.table.setMinimumWidth(700)
        self.layout.addWidget(self.table)
        self.table.setStyleSheet("""
                    QTableWidget {
                        background-color: #ffffff;
                        font-size: 14px;
                        color: #4a148c;
                        border: 1px solid #d1c4e9;
                    }
                    QHeaderView::section {
                        background-color: #7e57c2;
                        color: white;
                        padding: 5px;
                        font-weight: bold;
                        font-size: 13px;
                    }
                """)

        #تنسيق الجدول
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)  # توسع الأعمدة تلقائيًا
        self.table.verticalHeader().setDefaultSectionSize(40)  # ارتفاع الصفوف
        self.table.verticalHeader().setVisible(False)


        #توسيط الجدول
        table_container = QHBoxLayout()
        table_container.addStretch()
        table_container.addWidget(self.table)
        table_container.addStretch()


        self.layout.addLayout(table_container)
        # Buttoms
        buttons_layout = QHBoxLayout()

        self.add_button=QPushButton("Add Course")
        self.add_button.clicked.connect(self.add_course_row)
        self.style_button(self.add_button)
        buttons_layout.addWidget(self.add_button)


        self.calc_button=QPushButton("Calculate GPA")
        self.calc_button.clicked.connect(self.calculate_gpa)
        self.style_button(self.calc_button)
        buttons_layout.addWidget(self.calc_button)

        self.gpa_label=QLabel("GPA:")
        self.gpa_label.setStyleSheet("font-weight: bold; color: #4a148c;")
        buttons_layout.addWidget(self.gpa_label)

        self.cumulative_checkbox = QCheckBox("Cumulative GPA Option")
        self.cumulative_checkbox.stateChanged.connect(self.toggle_cumulative_section)
        buttons_layout.addWidget(self.cumulative_checkbox)

        self.layout.addLayout(buttons_layout)

        # Cumulative
        self.cumulative_layout_widget = QWidget()
        self.cumulative_layout = QFormLayout(self.cumulative_layout_widget)

        self.previous_gpa_input = QLineEdit()
        self.style_input(self.previous_gpa_input)
        self.previous_credits_input = QLineEdit()
        self.style_input(self.previous_credits_input)
        self.cumulative_results = QLabel("")
        self.cumulative_results.setStyleSheet("color: #4a148c; font-weight: bold;")

        self.calc_cumulative_button = QPushButton("Calculate Cumulative")
        self.calc_cumulative_button.clicked.connect(self.calculate_cumulative)
        self.style_button(self.calc_cumulative_button)

        self.cumulative_layout.addRow("Previous GPA:", self.previous_gpa_input)
        self.cumulative_layout.addRow("Previous Attempted credit:", self.previous_credits_input)
        self.cumulative_layout.addRow(self.calc_cumulative_button)
        self.cumulative_layout.addRow("Results:", self.cumulative_results)

        self.layout.addWidget(self.cumulative_layout_widget)
        self.cumulative_layout_widget.setVisible(False)

        self.setStyleSheet("background-color: #eaf6ff;")

    def style_button(self, button):
        button.setStyleSheet("""
                QPushButton {
                    background-color: #9575cd;
                    color: white;
                    border: none;
                    border-radius: 6px;
                    padding: 6px 12px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #7e57c2;
                }
            """)

    def style_input(self, line_edit):
        line_edit.setStyleSheet("""
                QLineEdit {
                    background-color: #f3e5f5;
                    color: #4a148c;
                    border: 1px solid #b39ddb;
                    padding: 4px;
                    border-radius: 4px;
                }
            """)

    def add_course_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        course_item = QTableWidgetItem(str(self.course_number))
        course_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row_position, 0, course_item)
        #
        credit_input = QLineEdit()
        self.style_input(credit_input)
        self.table.setCellWidget(row_position, 1, credit_input)

        grade_box = QComboBox()
        grade_box.addItems([" ", "A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"])
        self.table.setCellWidget(row_position, 2, grade_box)

        self.course_number += 1

    def calculate_gpa(self):
        data = []
        for row in range(self.table.rowCount()):
            credit_widget = self.table.cellWidget(row, 1)
            grade_widget = self.table.cellWidget(row, 2)
            if credit_widget and grade_widget:
                try:
                    credit = float(credit_widget.text())
                    grade = grade_widget.currentText()
                    data.append((grade, credit))
                except ValueError:
                    continue
        self.gpa_engine = self.GPA()
        semester_gpa = self.gpa_engine.calculate_semester_gpa(data)
        self.gpa_label.setText(f"GPA: {semester_gpa}")

    def calculate_cumulative(self):
        try:
            prev_gpa = float(self.previous_gpa_input.text())
            prev_credits = float(self.previous_credits_input.text())
            cumulative_gpa = self.gpa_engine.calculate_cumulative_gpa(prev_gpa, prev_credits)
            self.cumulative_results.setText(f"{cumulative_gpa}")
        except ValueError:
            self.cumulative_results.setText("Invalid input")

    def toggle_cumulative_section(self, state):
        self.cumulative_layout_widget.setVisible(state == Qt.Checked)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPACalculator()
    window.show()
    sys.exit(app.exec_())





