class Clock:

    def __init__(self, total_minutes: int = 480):
        self.total_minutes = total_minutes
        self.minute = total_minutes % 60
        self.hour = (total_minutes // 60) % 24
        if self.hour >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"

    def add_minutes(self, minutes_to_add):
        self.total_minutes += minutes_to_add
        self.minute = self.total_minutes % 60
        self.hour = (self.total_minutes // 60) % 24
        if self.hour >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"

    def add_hour(self, hours_to_add):
        self.total_minutes += hours_to_add
        self.minute = self.total_minutes % 60
        self.hour = (self.total_minutes // 60) % 24
        if self.hour >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"

    def __str__(self):
        if self.hour >= 13:
            strHr = self.hour % 12
        else:
            strHr = self.hour

        if self.minute < 10:
            return f"{strHr}:0{self.minute} {self.meridian}"
        else:
            return f"{strHr}:{self.minute} {self.meridian}"

    def __repr__(self):
        if self.hour >= 13:
            strHr = self.hour % 12
        else:
            strHr = self.hour

        if self.minute < 10:
            return f"{strHr}:0{self.minute} {self.meridian}"
        else:
            return f"{strHr}:{self.minute} {self.meridian}"