import enum


class TruckStatus(enum.Enum):
    """
    Truck Enum to list color coded "Active" and "Inactive" strings.

    Inactive will show as red.
    Active will show as green.
    """
    INACTIVE = "\u001b[31mInactive\u001b[0m"
    ACTIVE = "\u001b[32mActive\u001b[0m"