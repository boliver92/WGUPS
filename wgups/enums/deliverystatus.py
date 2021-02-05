import enum


class DeliveryStatus(enum.Enum):
    Loading = "Loading"
    Delivery = "Out for delivery"
    Delivered = "Delivered"
