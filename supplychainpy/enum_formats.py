from enum import Enum


class FileFormats(Enum):
    text = 1
    csv = 2


class PeriodFormats(Enum):
    days = 1
    weeks = 2
    months = 3
    quarters = 4
    years = 5
