import enum


class DeliveryStatus(enum.Enum):
    """Package Enum to list color coded "Delayed", "Arrived at Hub", "Out for delivery", and "Delivered" strings.


    """
    DELAYED = "\u001b[31mDelayed\u001b[0m"
    LOADING = "\u001b[33mArrived at HUB\u001b[0m"
    LOADED = "\u001b[34mOut for delivery\u001b[0m"
    DELIVERED = "\u001b[32mDelivered\u001b[0m"
