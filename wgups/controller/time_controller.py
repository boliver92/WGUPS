from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import ClassVar

@dataclass()
class TimeController:

    current_time: datetime = datetime.now()

    def __post_init__(self):
        self.current_time.replace(hour=9, minute=0, second=0)