import enum
from sqlalchemy import Enum

class StatusModel(enum.Enum):
    available = 1
    running_low = 2
    out_of_stock = 3