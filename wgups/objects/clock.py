class Clock:
    """Class used to represent and simulate time.

    The class takes the total minutes elapsed and determines the
    current time. For the purpose of this program, the class is
    initialized with 480 total minutes so that it is 8:00 AM.

    ...

    Attributes
        total_minutes: int Default: 480
            The total number of minuted elapsed.
        hour: int
            The current hour in 24-hr format
        minute: int
            The current minute
        meridian: str
            The current "meridian" (AM or PM)
    """

    max_min: int = 0

    def __init__(self, total_minutes: float = 480.0):
        self.total_minutes = total_minutes
        self.minute = int(total_minutes % 60)
        self.hour = int((total_minutes // 60) % 24)
        if self.hour >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"

    def add_minutes(self, minutes_to_add: float):
        """Adds to the specified number of minutes to the Clock instance's
        total_minutes and updates the instance's hour, minute, and
        meridian properties.

        :param minutes_to_add: int The number of minutes to increment
        the clock instance's total_minutes by.

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        self.total_minutes += minutes_to_add
        self.minute = int(self.total_minutes % 60)
        self.hour = int((self.total_minutes // 60) % 24)
        if self.hour == 0:
            self.hour += 1
        if self.hour >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"

    def add_hour(self, hours_to_add):
        """
        Adds to the specified number of hours to the Clock instance's
        total_minutes and updates the instance's hour and
        meridian properties.

        :param hours_to_add:
            The number of hours to increment
        the clock instance's hour by.

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        self.total_minutes += (hours_to_add * 60)
        self.minute = int(self.total_minutes % 60)
        self.hour = int((self.total_minutes // 60) % 24)
        if self.hour >= 12:
            self.meridian = "PM"
        else:
            self.meridian = "AM"

    def refresh(self):
        """Resets the clock to match the static Clock.max_min variable and resets the Clock.max_min to 0

        This method is primarily used to synchronize multiple clocks to
        reflect the latest time

        """
        if Clock.max_min > self.total_minutes:
            self.total_minutes = Clock.max_min
            self.minute = int(self.total_minutes % 60)
            self.hour = int((self.total_minutes // 60) % 24)
            if self.hour >= 12:
                self.meridian = "PM"
            else:
                self.meridian = "AM"
        Clock.max_min = 0

    def __repr__(self):
        """
        Displays the Clock instance as a "HH:MM AM/PM" string

        :return: "HH:MM AM/PM"

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        if self.hour >= 13:
            strHr = self.hour % 12
        else:
            strHr = self.hour

        if self.minute < 10:
            return f"{strHr}:0{self.minute} {self.meridian}"
        else:
            return f"{strHr}:{self.minute} {self.meridian}"

    def simulate_travel_time(self, miles_to_simulate, average_mph=18):
        """Increases the clock time based on the amount of miles traveled

        The method takes in the number of miles driven and it is used
        to determine the time elapsed during travel based on the
        average_mph.

        :param miles_to_simulate:

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        minutes_to_simulate = int((60 // average_mph) * miles_to_simulate)
        self.add_minutes(minutes_to_simulate)

    def __str__(self):
        """
        Displays the Clock instance as a "HH:MM AM/PM" string

        :return: "HH:MM AM/PM"

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        if self.hour >= 13:
            str_hr = self.hour % 12
        else:
            str_hr = self.hour

        if self.minute < 10:
            return f"{str_hr}:0{self.minute} {self.meridian}"
        else:
            return f"{str_hr}:{self.minute} {self.meridian}"