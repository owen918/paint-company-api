from sqlalchemy import Enum
from db import db
import enum

class ColorModel(enum.Enum):
    blue = 1
    grey = 2
    black = 3
    white = 4
    purple = 5