import enum


class DeliveryStatus(enum.Enum):
    LOADING = "\u001b[31mArrived at HUB\u001b[0m"
    LOADED = "\u001b[34mOut for delivery"
    DELIVERED = "\u001b[32mDelivered\u001b[0m"
