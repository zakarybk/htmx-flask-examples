from dataclasses import dataclass
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, name: str) -> None:
        self.name = name

    def get_id(self):
        return self.name
