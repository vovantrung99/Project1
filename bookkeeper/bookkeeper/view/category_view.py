from typing import Optional, List
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit, QTableWidget, QDialog, QTableWidgetItem
from bookkeeper.repository.sqlite_repository import SQLiteRepository
from bookkeeper.utils import show_warning_dialog, h_widget_with_label

class AddCategoryDialog(QDialog):
    def __init__(self, category_repo: SQLiteRepository,
                 category_data: dict[str, str]|None = None,
                 )-> None:
        super().__init__()
        self.category_repo = category_repo
        
        self.setWindowTitle('Добавить категорию')
        self.setFixedSize(300, 150)
        self.layout = QVBoxLayout()
        
        self.edit_category_name = QLineEdit()
        if category_data is not None:
            self.edit_category_name.setText(category_data['name'])
        self.layout.addLayout(h_widget_with_label('Название категории ', self.edit_category_name))

        self.apply_button = QPushButton('Apply')
        self.layout.addWidget(self.apply_button)
        self.apply_button.clicked.connect(self.apply_button_click)

        self.setLayout(self.layout)
        self.category = None

    def apply_button_click(self)->None:
        """
        Проверяет введенные данные на корректность
        """
        if self.validate_data():
            
            self.category = Category(name = self.category_dict['name'])
            show_warning_dialog(message='Успешно!!', title='Edit')
            self.accept()
            
    def validate_data(self):
        name = self.edit_category_name.text().strip()
        try :
            name = str(name)
        except ValueError:
            show_warning_dialog(message= 'Неверный тип данных',
                                titlee = 'Set Category')
            return False
        if len(name) == 0:
            show_warning_dialog(message='Название категории не может быть пустым',
                                title = 'Set Category')
            return False

        self.category_dict = {'name':name}
        return True
class EditCategoryDialog(QDialog):
    def __init__(self, category_repo: SQLiteRepository,
                 category_data: dict[str, str]|None = None,
                 )-> None:
        super().__init__()
        self.category_repo = category_repo
        
        self.setWindowTitle('Редактировать категорию')
        self.setFixedSize(300, 150)
        self.layout = QVBoxLayout()
        
        self.edit_category_name = QLineEdit()
        if category_data is not None:
            self.edit_category_name.setText(category_data['name'])
        self.layout.addLayout(h_widget_with_label('Название категории ', self.edit_category_name))

        self.apply_button = QPushButton('Apply')
        self.layout.addWidget(self.apply_button)
        self.apply_button.clicked.connect(self.apply_button_click)

        self.setLayout(self.layout)
        self.category = None

    def apply_button_click(self)->None:
        """
        Проверяет введенные данные на корректность
        """
        if self.validate_data():
            
            self.category = Category(pk = self.category_dict['pk'],
                                     name = self.category_dict['name'])
            show_warning_dialog(message='Успешно!!', title='Edit')
            self.accept()
            
    def validate_data(self):
        pk = self.category_dict['pk']
        name = self.edit_category_name.text().strip()
        try :
            name = str(name)
        except ValueError:
            show_warning_dialog(message= 'Неверный тип данных',
                                titlee = 'Set Category')
            return False
        if len(name) == 0:
            show_warning_dialog(message='Название категории не может быть пустым',
                                title = 'Set Category')
            return False

        self.category_dict = {'pk':pk, 'name':name}
        return True
class CategoryView(QWidget):
    """
    Виджет отображает категории в главном окне
    """
    def __init__(self, category_repo: SQLiteRepository|None = None)-> None:
        super().__init__()
        self.category_repo = category_repo
        
        self.layout = QVBoxLayout()
        
        self.category_table = QTableWidget(0, 2)
        self.show_categories()
        self.layout.addWidget(self.category_table)

        self.add_category_button = QPushButton('Добавить категорию')
        self.add_category_button.clicked.connect(self.add_category_dialog)
        self.layout.addWidget(self.add_category_button)

        self.edit_category_button = QPushButton('Редактировать категорию')
        self.edit_category_button.clicked.connect(self.edit_category_dialog)
        self.layout.addWidget(self.edit_category_button)

        self.delete_category_button = QPushButton('Удалить категорию')
        self.delete_category_button.clicked.connect(self.delete_category)
        self.layout.addWidget(self.delete_category_button)

        self.save_button = QPushButton('Save')
        self.save_button.clicked.connect(self.save_button_click)
        self.layout.addWidget(self.save_button)

        self.change_category= None

        self.setLayout(self.layout)

    def show_categories(self)->None:
        
        self.category_table.setColumnCount(2)
        self.category_table.setRowCount(self.category_repo.get_all().count())
        self.category_table.setHorizontalHeaderLabels(['ID', 'Название категории'])
        self.category_table.setVerticalHeaderLabels(['ID'])
        self.category_table.setEditTriggers(QTableWidget.NoEditTriggers)

        categories = self.category_repo.get_all()
        for i, category in enumerate(categories):
            self.category_table.setItem(i, 0, QTableWidgetItem(str(category.pk)))
            self.category_table.setItem(i, 1, QTableWidgetItem(category.name))

    def add_category_dialog(self)->None:
        category_data = {'name':''}
        dialog = AddCategoryDialog(category_repo = self.category_repo, 
                                 budget_data = category_data)

        dialog.exec()

        if dialog.category is not None:    
            new_category = dialog.category

            self.category_table.setRowCount(self.category_table.rowCount() + 1)
            self.category_table.setItem(self.category_table.rowCount() - 1, 0, QTableWidgetItem(str(new_category.pk)))
            self.category_table.setItem(self.category_table.rowCount() - 1, 1, QTableWidgetItem(new_category.name))
            self.change_category= ('add-category',dialog.category)

    def edit_category_dialog(self)->None:
        pk = self.category_table.currentRow()
        if pk == -1:
            show_warning_dialog(message='Выберите категорию', title = 'Edit Category')
            return

        category_data = {'pk':self.category_table.item(pk, 0).text(),
                         'name':self.category_table.item(pk, 1).text()}
        dialog = EditCategoryDialog(category_repo = self.category_repo, 
                                 budget_data = category_data)

        dialog.exec()

        if dialog.category is not None:    
            new_category = dialog.category

            self.category_table.setItem(pk, 1, QTableWidgetItem(new_category.name))
            self.change_category= ('update-category',dialog.category)

    def delete_category(self)->None:
        pk = self.category_table.currentRow()
        if pk == -1:
            show_warning_dialog(message='Выберите категорию', title = 'Delete Category')
            return

        self.category_repo.delete(pk)
        self.category_table.removeRow(pk)
        self.change_category= ('delete-category',pk)

    def save_button_click(self):
        """
        Сохранить категории
        """
        if self.change_category is None:
            show_warning_dialog(message='Нет изменения', title = 'Сохранение')
        else:
             
            if self.category_repo.table_exists() is False:
                self.category_repo.create_table_db()

            if self.change_category[0] == 'add-category':
                self.category_repo.add(self.change_category[1])
            elif self.change_category[0] == 'update-category':
                self.category_repo.update(self.change_category[1])
            elif self.change_category[0] == 'delete-category':
                self.category_repo.delete(self.change_category[1])
            show_warning_dialog(message='Успешно сохранить категории', title= 'Сохранение')

            self.change_category = None
if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from bookkeeper.repository.sqlite_repository import SQLiteRepository
    from bookkeeper.models.category import Category
    app = QApplication(sys.argv)
    category_repo = SQLiteRepository(db_file = 'bookkeeper/view/new_database.db', cls = Category)
    window = CategoryView(category_repo=category_repo)
    window.setWindowTitle('Set Category')
    window.resize(500,500)
    window.show()
    sys.exit(app.exec())