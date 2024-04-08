
from inspect import get_annotations
import sqlite3
from typing import Any, Optional

from bookkeeper.repository.sqlite_repository import T, SqliteRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense


class SqliteRepository(SqliteRepository[T]):
    def __init__(self, db_file: str, cls: type) -> None:
        self.db_file = db_file
        self.table_name = cls.__name__.lower()
        self.fields = get_annotations(cls, eval_str = True)
        self.fields.pop('pk')
    def add(self, obj: T) -> int:
        names = ', '.join(self.fields.keys())
        p = ', '.join("?" * len(self.fields))
        values = [getattr(obj, x) for x in self.fields]
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute('PRAGMA foreign_keys = ON')
            cur.execute(f"INSERT INTO {self.table_name} ({names}) VALUES ({p})", values)
        conn.close()
        return obj.pk
    def get(self, pk: int) -> T | None:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            names = ', '.join(self.fields.keys())
            query = f"SELECT {names} FROM {self.table_name} WHERE pk = {pk}"
            cur.execute(query)
            row = cur.fetchone()
            if row is None:
                return None
        conn.close()
        obj_dict = dict(zip(self.fields.keys(), row))
        for field, value in obj_dict.items():
            if not isinstance(value, self.fields[field]):
                # Nếu kiểu không phù hợp, trả về None
                return None
        obj_dict['pk'] = pk
        obj = class_name(self.table_name.capitalize(),obj_dict)
        return obj

    def get_all(self, where: dict[str, Any]|None = None,
                value_range = False)->list[T]:
        
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute(f"PRAGMA table_info({self.table_name})")
            columns_info = cur.fetchall()
            column_names = [column[1] for column in columns_info]
            if where is None:
                
                query = f"SELECT * FROM {self.table_name}"
                cur.execute(query)
                rows = cur.fetchall()
            elif value_range is True: # Tìm giá trị trong phạm vi
                key = next(iter(where.keys()))
                query = f"""
                SELECT * FROM {self.table_name}
                WHERE {key} >=? AND {key} <=?
                """
                cur.execute(query, tuple(where[key]))
                rows = cur.fetchall()
            else:
                
                query = f"SELECT * FROM {self.table_name} WHERE " + " AND ".join([f"{k} =?" for k in where.keys()])
                cur.execute(query, tuple(where.values()))
                rows = cur.fetchall()
        conn.close()
        list_obj_dict = []
        for row in rows:
            obj_dict = dict(zip(column_names, row))
            
            obj_dict['pk'] = row[0]
            obj = class_name(self.table_name.capitalize(),obj_dict)
            list_obj_dict.append(obj)
        return list_obj_dict
    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            values = [getattr(obj, x) for x in self.fields]
            set_clause = ', '.join(f'{field} =?' for field in self.fields.keys())
            query =f"UPDATE {self.table_name} SET {set_clause} WHERE pk = {obj.pk}"
            cur.execute(query, values)
        conn.close()
    def delete(self,pk: int)-> None:
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute(f"DELETE FROM {self.table_name} WHERE pk = {pk}")
        cur.close()
    
    def table_exists(self):
        """
        Kiểm tra xem bảng có tồn tại hay không
        """
        with sqlite3.connect(self.db_file) as conn:
            cur = conn.cursor()
            cur.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{self.table_name}'")
            row = cur.fetchone()
            if row is None:
                return False
        return True
        
     
    def create_table_db(self):
        """
        Tạo bảng nếu chưa tồn tại
        """
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        if self.table_name == 'Budget':
            query = ''' 
            CREATE TABLE IF NOT EXISTS Budget (
                        pk INTEGER PRIMARY KEY,
                        day FLOAT,
                        week FLOAT,
                        month FLOAT)
            '''
        elif self.table_name == 'Category':
            query = ''' 
            CREATE TABLE IF NOT EXISTS Category (
                        pk INTEGER PRIMARY KEY,
                        name TEXT,
                        parent INTEGER,
                        FOREIGN KEY(parent) REFERENCES Category(pk)
                        )'''
        elif self.table_name == 'Expense':
            query = ''' 
            CREATE TABLE IF NOT EXISTS Expense (
                        pk INTEGER PRIMARY KEY,
                        comment TEXT,
                        amount FLOAT,
                        category INTEGER,
                        added_date TEXT,
                        expense_date TEXT,
                        FOREIGN KEY(category) REFERENCES Category(pk)
                        )'''
        cursor.execute(query)
        conn.commit()
        conn.close()
def class_name(name:str, values:dict)-> T: 
    """
    Chuyển đổi dict thành đối tượng lớp
    """
    if name == 'Budget':
        return Budget(pk = values['pk'],
                      day = values['day'], 
                      week = values['week'],
                      month = values['month'] )
    elif name == 'Category':
        return Category(pk = values['pk'],
                        name = values['name'],
                        parent = values['parent'])
    elif name == 'Expense':
        return Expense(pk = values['pk'],
                       expense_date= values['expense_date'],
                       comment= values['comment'],
                       amount = values['amount'],
                       category= values['category'])
    else:
        raise ValueError(f'Unknown class name: {name}')