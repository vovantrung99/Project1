import pytest
from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.budget import Budget
from bookkeeper.models.category import Category
from bookkeeper.models.expense import Expense

def test_add():
    db_file = ':memory:'
    budget_repo = SqliteRepository(db_file, Budget)
    budget_repo.create_table_db()

    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budgets = budget_repo.get_all()
    assert len(budgets) == 1

def test_get():
    db_file = ':memory:'
    budget_repo = SqliteRepository(db_file, Budget)
    budget_repo.create_table_db()

    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budget = budget_repo.get(1)
    assert budget is not None
    assert budget.day == 100.0

def test_get_all():
    db_file = ':memory:'
    budget_repo = SqliteRepository(db_file, Budget)
    budget_repo.create_table_db()

    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budgets = budget_repo.get_all()
    assert len(budgets) == 1

def test_update():
    db_file = ':memory:'
    budget_repo = SqliteRepository(db_file, Budget)
    budget_repo.create_table_db()

    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budget = budget_repo.get(1)
    budget.day = 300.0
    budget_repo.update(budget)

    updated_budget = budget_repo.get(1)
    assert updated_budget is not None
    assert updated_budget.day == 300.0

def test_delete():
    db_file = ':memory:'
    budget_repo = SqliteRepository(db_file, Budget)
    budget_repo.create_table_db()

    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budget_repo.delete(1)

    budgets = budget_repo.get_all()
    assert len(budgets) == 0

@pytest.fixture
def db_file():
    return ':memory:'

@pytest.fixture
def budget_repo(db_file):
    budget_repo = SqliteRepository(db_file, Budget)
    budget_repo.create_table_db()
    return budget_repo

@pytest.fixture
def category_repo(db_file):
    category_repo = SqliteRepository(db_file, Category)
    category_repo.create_table_db()
    return category_repo

@pytest.fixture
def expense_repo(db_file):
    expense_repo = SqliteRepository(db_file, Expense)
    expense_repo.create_table_db()
    return expense_repo

def test_add_budget(budget_repo):
    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budgets = budget_repo.get_all()
    assert len(budgets) == 1

def test_get_budget(budget_repo):
    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budget = budget_repo.get(1)
    assert budget is not None
    assert budget.day == 100.0

def test_get_all_budgets(budget_repo):
    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budgets = budget_repo.get_all()
    assert len(budgets) == 1

def test_update_budget(budget_repo):
    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budget = budget_repo.get(1)
    budget.day = 300.0
    budget_repo.update(budget)

    updated_budget = budget_repo.get(1)
    assert updated_budget is not None
    assert updated_budget.day == 300.0

def test_delete_budget(budget_repo):
    budget = Budget(day=100.0, week=500.0, month=2000.0)
    budget_repo.add(budget)

    budget_repo.delete(1)

    budgets = budget_repo.get_all()
    assert len(budgets) == 0

def test_add_category(category_repo):
    category = Category(name='Category1')
    category_repo.add(category)

    categories = category_repo.get_all()
    assert len