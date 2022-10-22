class Event:
    type: id
    event_name: str
    minutes: int
    seconds: int
    side: str

    def __init__(self, event_name, type, mtime, side, **kwargs):
        self.type = int(type)
        self.event_name = event_name
        self.minutes, self.seconds = self.mtime_to_minutes_and_seconds(mtime)
        self.side = side

    def fractional_minutes(self):
        return self.minutes + self.seconds / 60

    def __str__(self):
        return_str = "Event:"
        for attribute, value in vars(self).items():
            if isinstance(value, str):
                return_str += f" {attribute}='{value}',"
            else:
                return_str += f" {attribute}={value},"
        return return_str[:-1]

    @staticmethod
    def mtime_to_minutes_and_seconds(mtime: str) -> tuple[int, int]:
        total_minutes = total_seconds = 0
        for partial_time in mtime.split(" +"):
            minutes, seconds = partial_time.split(":")
            total_seconds += int(seconds)
            total_minutes += int(minutes)
        return total_minutes, total_seconds


class FreeKickEvent(Event):
    event_name: str = "FREE KICK"

    def __init__(self, **kwargs):
        super().__init__(event_name=self.event_name, **kwargs)


class FreeThrowEvent(Event):
    event_name: str = "FREE-THROW EVENT"

    def __init__(self, **kwargs):
        super().__init__(event_name=self.event_name, **kwargs)


class ShotOnTargetEvent(Event):
    event_name: str = "SHOT ON TARGET"

    def __init__(self, **kwargs):
        super().__init__(event_name=self.event_name, **kwargs)


class ShotOffTargetEvent(Event):
    event_name: str = "SHOT OF TARGET"

    def __init__(self, **kwargs):
        super().__init__(event_name=self.event_name, **kwargs)


class PenaltyAwardedEvent(Event):
    event_name: str = "PENALTY AWARDED"

    def __init__(self, **kwargs):
        super().__init__(event_name=self.event_name, **kwargs)


class GoalEvent(Event):
    event_name: str = "GOAL"

    def __init__(self, **kwargs):
        super().__init__(event_name=self.event_name, **kwargs)


event_types = {
    30: GoalEvent,
    150: FreeKickEvent,
    152: FreeThrowEvent,
    155: ShotOnTargetEvent,
    156: ShotOffTargetEvent,
    161: PenaltyAwardedEvent,
}


def create_event(type: int, **kwargs) -> Event | None:
    int_type = int(type)
    if int_type not in event_types:
        return None
    return event_types[int_type](type=type, **kwargs)
