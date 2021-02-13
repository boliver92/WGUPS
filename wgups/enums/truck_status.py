import enum


class TruckStatus(enum.Enum):
    INACTIVE = "\u001b[31mInactive\u001b[0m"
    ACTIVE = "\u001b[32mActive\u001b[0m"