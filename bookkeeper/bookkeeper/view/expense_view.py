import sys
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTableWidget,QHeaderView, QSizePolicy, 
                               QLabel, QApplication, QPushButton,QTableWidgetItem, 
                               QAbstractItemView)

from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import show_warning_dialog
from bookkeeper.view.category_view import get_categories
from bookkeeper.models.expense import Expense
from bookkeeper.models.category import Category
from bookkeeper.view.change_expense_dialog import ChangeExpenseDialog

class ExpenseView(QWidget):
    def __init__(self, expense_repo: SQLiteRepository,
                 category_repo: SQLiteRepository)-> None:
        super().__init__()
        self.expense_repo = expense_repo
        self.category_repo = category_repo
        
        self.layout = QVBoxLayout()
        
        self.expense_table = QTableWidget(0, 4)
        self.expense_table.setHorizontalHeaderLabels(['ID', 'Название', 'Сумма', 'Категория'])
        self.expense_table.verticalHeader().hide()
        self.expense_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.show_expenses()
        self.layout.addWidget(self.expense_table)

        self.add_expense_button = QPushButton('Добавить расход')
        self.add_expense_button.clicked.connect(self.add_expense_dialog)
        self.layout.addWidget(self.add_expense_button)

        self.change_expense_button = QPushButton('Изменить расход')
        self.change_expense_button.clicked.connect(self.change_expense_dialog)
        self.layout.addWidget(self.change_expense_button)

        self.delete_expense_button = QPushButton('Удалить расход')
        self.delete_expense_button.clicked.connect(self.delete_expense)
        self.layout.addWidget(self.delete_expense_button)

        self.setLayout(self.layout)

    def show_expenses(self)->None:
        
        self.expense_table.setRowCount(self.expense_repo.get_all().count())
        self.expense_table.setHorizontalHeaderLabels(['ID', 'Название', 'Сумма', 'Категория'])

        expenses = self.expense_repo.get_all()
        for i, expense in enumerate(expenses):
            self.expense_table.setItem(i, 0, QTableWidgetItem(str(expense.pk)))
            self.expense_table.setItem(i, 1, QTableWidgetItem(expense.name))
            self.expense_table.setItem(i, 2, QTableWidgetItem(str(expense.amount)))
            self.expense_table.setItem(i, 3, QTableWidgetItem(expense.category.name))

    def add_expense_dialog(self)->None:
        dialog = ChangeExpenseDialog(self.expense_repo, None)
        dialog.exec()

        if dialog.expense is not None:    
            new_expense = dialog.expense

            self.expense_table.setRowCount(self.expense_table.rowCount() + 1)
            self.expense_table.setItem(self.expense_table.rowCount() - 1, 0, QTableWidgetItem(str(new_expense.pk)))
            self.expense_table.setItem(self.expense_table.rowCount() - 1, 1, QTableWidgetItem(new_expense.name))
            self.expense_table.setItem(self.expense_table.rowCount() - 1, 2, QTableWidgetItem(str(new_expense.amount)))
            self.expense_table.setItem(self.expense_table.rowCount() - 1, 3, QTableWidgetItem(new_expense.category.name))

    def change_expense_dialog(self)->None:
        pk = self.expense_table.currentRow()
        if pk == -1:
            show_warning_dialog(message='Выберите расход', title = 'Change Expense')
            return

        expense_data = {'pk':self.expense_table.item(pk, 0).text(),
                         'name':self.expense_table.item(pk, 1).text(),
                         'amount':self.expense_table.item(pk, 2).text(),
                         'category':self.expense_table.item(pk, 3).text()}
        dialog = ChangeExpenseDialog(self.expense_repo, expense_data)

        dialog.exec()

        if dialog.expense is not None:    
            new_expense = dialog.expense

            self.expense_table.setItem(pk, 1, QTableWidgetItem(new_expense.name))
            self.expense_table.setItem(pk, 2, QTableWidgetItem(str(new_expense.amount)))
            self.expense_table.setItem(pk, 3, QTableWidgetItem(new_expense.category.name))

    def delete_expense(self)->None:
        pk = self.expense_table.currentRow()
        if pk == -1:
            show_warning_dialog(message='Выберите расход', title = 'Delete Expense')
            return

        self.expense_repo.delete(pk)
        self.expense_table.removeRow(pk)

if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from bookkeeper.repository.sqlite_repository import SQLiteRepository
    from bookkeeper.models.expense import Expense
    from bookkeeper.models.category import Category
    app = QApplication(sys.argv)
    expense_repo = SQLiteRepository(db_file = 'bookkeeper/view/new_database.db', cls = Expense)
    category_repo = SQLiteRepository(db_file = 'bookkeeper/view/new_database.db', cls = Category)
    window = ExpenseView(expense_repo=expense_repo, category_repo=category_repo)
    window.setWindowTitle('Expense View')
    window.resize(500,500)
    window.show()
    sys.exit(app.exec())