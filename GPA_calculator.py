import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QLabel, QCheckBox, QLineEdit, QFormLayout, QHeaderView)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from gpa_backend import GPA, GPAError


class GPACalculator(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(" GPA Calculator")
        self.setGeometry(100, 100, 700, 400)
        self.courseNumber = 1
        self.setStyleSheet("background-color: #f3efff;")
        self.setWindowIcon(QIcon("ICON2-.png"))

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # العنوان
        titleLabel = QLabel("GPA Calculator")
        title_font = QFont("Arial", 20, QFont.Bold)
        titleLabel.setStyleSheet("""
                        font-size: 28px;
                        font-weight: bold;
                        color: #3d2c8d; 
                        margin-bottom: 12px;
                    """)
        titleLabel.setFont(title_font)
        titleLabel.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(titleLabel)

        # الجدول
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Course", "Credits", "Grade"])
        self.table.setMinimumWidth(700)
        self.table.setMinimumHeight(250)
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

        # تنسيق الجدول
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setDefaultSectionSize(40)
        self.table.verticalHeader().setVisible(False)

        # لوضع الجدول في المنتصف
        table_in_Center = QHBoxLayout()
        table_in_Center.addStretch()
        table_in_Center.addWidget(self.table)
        table_in_Center.addStretch()
        self.layout.addLayout(table_in_Center)

        # الازرار
        buttons_layout = QHBoxLayout()

        self.addButton = QPushButton("Add Course")
        self.addButton.clicked.connect(self.add_row)
        self.style_button(self.addButton)
        buttons_layout.addWidget(self.addButton)

        self.resetButton = QPushButton("Reset")
        self.resetButton.clicked.connect(self.reset)
        self.style_button(self.resetButton)
        buttons_layout.addWidget(self.resetButton)

        self.calcButton = QPushButton("Calculate GPA")
        self.calcButton.clicked.connect(self.calculate_gpa)
        self.style_button(self.calcButton)
        buttons_layout.addWidget(self.calcButton)

        self.gpaLabel = QLabel("GPA:")
        self.gpaLabel.setStyleSheet("font-weight: bold; color: #4a148c;")
        buttons_layout.addWidget(self.gpaLabel)

        self.cumulativeCheckbox = QCheckBox("Cumulative GPA Option")
        self.cumulativeCheckbox.stateChanged.connect(self.toggle_cumulative_section)
        buttons_layout.addWidget(self.cumulativeCheckbox)

        self.layout.addLayout(buttons_layout)

        # المعدل التراكمي
        self.cumulative_layout_widget = QWidget()
        self.cumulative_layout = QFormLayout(self.cumulative_layout_widget)

        self.previous_gpa = QLineEdit()
        self.style_input(self.previous_gpa)
        self.previous_credits = QLineEdit()
        self.style_input(self.previous_credits)
        self.cumulative_results = QLabel("")
        self.cumulative_results.setStyleSheet("color: #4a148c; font-weight: bold;")

        self.calc_cumulative_button = QPushButton("Calculate Cumulative")
        self.calc_cumulative_button.clicked.connect(self.calculate_cumulative)
        self.style_button(self.calc_cumulative_button)

        self.cumulative_layout.addRow("Previous GPA:", self.previous_gpa)
        self.cumulative_layout.addRow("Previous Attempted credit:", self.previous_credits)
        self.cumulative_layout.addRow(self.calc_cumulative_button)
        self.cumulative_layout.addRow("Results:", self.cumulative_results)

        self.layout.addWidget(self.cumulative_layout_widget)
        self.cumulative_layout_widget.setVisible(False)

        self.setStyleSheet("background-color: #eaf6ff;")
        # دوال التنسيق والالوان CSS

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
        # دالة لإضافة صف

    def add_row(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        course_item = QTableWidgetItem(str(self.courseNumber))
        course_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
        self.table.setItem(row_position, 0, course_item)

        credit_input = QLineEdit()
        self.style_input(credit_input)
        self.table.setCellWidget(row_position, 1, credit_input)

        grade_box = QComboBox()
        grade_box.addItems([" ", "A+", "A", "B+", "B", "C+", "C", "D+", "D", "F"])
        self.table.setCellWidget(row_position, 2, grade_box)

        self.courseNumber += 1
        # دالة إعادة الضبط

    def reset(self):
        self.gpaLabel.setText("GPA:")

        self.previous_credits.clear()
        self.previous_gpa.clear()
        self.cumulative_results.setText("")
        # دوال الربط و التعامل مع الاخطاء

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

                except (ValueError, GPAError) as e:
                    continue
        self.gpa_engine = GPA()
        try:
            semester_gpa = self.gpa_engine.calculate_semester_gpa(data)
            self.gpaLabel.setText(f"GPA: {semester_gpa}")
        except GPAError as e:
            self.gpaLabel.setText(str(e))

    def calculate_cumulative(self):
        try:
            prev_gpa = float(self.previous_gpa.text())
            prev_credits = float(self.previous_credits.text())

            cumulative_gpa = self.gpa_engine.calculate_cumulative_gpa(prev_gpa, prev_credits)

            self.cumulative_results.setText(f"{cumulative_gpa}")
        except (ValueError, GPAError) as e:
            self.cumulative_results.setText(str(e))
        # دالة تفقد ال Check box

    def toggle_cumulative_section(self, state):
        self.cumulative_layout_widget.setVisible(state == Qt.Checked)


    # لتشغيل البرنامج

if __name__ == "__main__":
        app = QApplication(sys.argv)
        window = GPACalculator()
        window.show()
        sys.exit(app.exec_())





