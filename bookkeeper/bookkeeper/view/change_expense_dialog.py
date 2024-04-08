import datetime
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QLineEdit, QPushButton, 
                       QHBoxLayout, QLabel, QComboBox)
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import show_warning_dialog, h_widget_with_label
from bookkeeper.view.category_view import get_categories, list_category_widget
from bookkeeper.models.expense import Expense

class ChangeExpenseDialog(QDialog):
    def __init__(self, expense_repo: SQLiteRepository,
                 expense_data: dict[str, str]|None = None,
                 )-> None:
        super().__init__()
        self.expense_repo = expense_repo
        
        self.setWindowTitle('Изменить расход')
        self.setFixedSize(400, 300)
        self.layout = QVBoxLayout()
        
        self.edit_expense_name = QLineEdit()
        if expense_data is not None:
            self.edit_expense_name.setText(expense_data['name'])
        self.layout.addLayout(h_widget_with_label('Название расхода ', self.edit_expense_name))

        self.edit_expense_amount = QLineEdit()
        if expense_data is not None:
            self.edit_expense_amount.setText(expense_data['amount'])
        self.layout.addLayout(h_widget_with_label('Сумма ', self.edit_expense_amount))

        self.edit_expense_date = QLineEdit()
        if expense_data is not None:
            self.edit_expense_date.setText(expense_data['date'])
        self.layout.addLayout(h_widget_with_label('Дата ', self.edit_expense_date))

        self.edit_expense_category = QComboBox()
        categories = get_categories(self.expense_repo)
        self.edit_expense_category.addItems([category.name for category in categories])
        if expense_data is not None:
            self.edit_expense_category.setCurrentText(expense_data['category'])
        self.layout.addWidget(self.edit_expense_category)

        self.apply_button = QPushButton('Apply')
        self.layout.addWidget(self.apply_button)
        self.apply_button.clicked.connect(self.apply_button_click)

        self.setLayout(self.layout)
        self.expense = None

    def apply_button_click(self)->None:
        """
        Проверяет введенные данные на корректность
        """
        if self.validate_data():
            
            self.expense = Expense(name = self.expense_dict['name'],
                                   amount = self.expense_dict['amount'],
                                   date = self.expense_dict['date'],
                                   category = self.expense_dict['category'])
            show_warning_dialog(message='Успешно!!', title='Edit')
            self.accept()
            
    def validate_data(self):
        name = self.edit_expense_name.text().strip()
        amount = self.edit_expense_amount.text().strip()
        date = self.edit_expense_date.text().strip()
        category = self.edit_expense_category.currentText()

        try :
            name = str(name)
            amount = float(amount)
            date = datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            show_warning_dialog(message= 'Неверный тип данных',
                                titlee = 'Set Expense')
            return False
        if len(name) == 0:
            show_warning_dialog(message='Название расхода не может быть пустым',
                                title = 'Set Expense')
            return False

        self.expense_dict = {'name':name, 'amount':amount, 'date':date, 'category':category}
        return True
if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from bookkeeper.repository.sqlite_repository import SQLiteRepository
    from bookkeeper.models.expense import Expense
    app = QApplication(sys.argv)
    expense_repo = SQLiteRepository(db_file = 'bookkeeper/view/new_database.db', cls = Expense)
    window = ChangeExpenseDialog(expense_repo=expense_repo)
    window.setWindowTitle('Set Expense')
    window.resize(500,500)
    window.show()
    sys.exit(app.exec())