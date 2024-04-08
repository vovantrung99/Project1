from dataclasses import dataclass, field
from typing import Optional

from bookkeeper.repository.sqlite_repository import SqliteRepository
from bookkeeper.models.category import Category

@dataclass
class Budget:
    amount: float
    category: Category
    day: int = field(default=1)
    month: int = field(default=1)
    year: int = field(default=2023)

    def add(self, repository: SqliteRepository):
        repository.add(self)

    def update(self, repository: SqliteRepository):
        repository.update(self)

    def delete(self, repository: SqliteRepository):
        repository.delete(self.pk)

    @staticmethod
    def get_by_id(repository: SqliteRepository, budget_id: int):
        return repository.get_by_id(budget_id)