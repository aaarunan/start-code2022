from typing import Iterator

import pandas

from matches.event import *
from matches.team import Team


class Match:
    home_team: Team
    away_team: Team
    events: list[Event]

    minutes: int
    goals: list[int]
    free_kicks: list[int]
    throw_ins: list[int]
    shots_on: list[int]
    shots_off: list[int]
    penalties: list[int]

    total_goals: list[int] = [0, 0]

    def __init__(self, **kwargs):
        try:
            self.home_team = Team(
                int(kwargs["t1id"]), kwargs["t1name"], kwargs.get("t1abbr", "")
            )
            self.away_team = Team(
                int(kwargs["t2id"]), kwargs["t2name"], kwargs.get("t2abbr", "")
            )
        except KeyError as e:
            print(e, kwargs)
        self.events = list()
        self.reset_stats()

    def set_total_goals(self):
        self.reset_stats()
        for _ in self.events_generator():
            pass
        self.total_goals = self.goals[:]

    def reset_stats(self):
        self.minutes = 0
        self.goals = [0, 0]
        self.free_kicks = [0, 0]
        self.throw_ins = [0, 0]
        self.shots_on = [0, 0]
        self.shots_off = [0, 0]
        self.penalties = [0, 0]

    def event_per_minute(self):
        events = self.events_generator(False)
        last_event = next(events, None)
        while last_event is not None:
            if last_event.minutes > self.minutes:
                yield list()
            else:
                out: list[Event] = [last_event]
                while (
                    last_event := next(events, None)
                ) is not None and last_event.minutes <= self.minutes:
                    out.append(last_event)
                yield out
            self.minutes += 1

    def events_generator(self, add_before=True) -> Iterator[Event]:
        self.reset_stats()
        for event in self.events:
            side = 0 if event.side == "home" else 1

            match event.type:
                case 30:

                    def add_function():
                        self.goals[side] += 1

                case 150:

                    def add_function():
                        self.free_kicks[side] += 1

                case 152:

                    def add_function():
                        self.throw_ins[side] += 1

                case 155:

                    def add_function():
                        self.shots_on[side] += 1

                case 156:

                    def add_function():
                        self.shots_off[side] += 1

                case 161:

                    def add_function():
                        self.penalties[side] += 1

                case _:
                    raise NotImplementedError(
                        f"Event type {{id={event.type}}} not implemented"
                    )

            if add_before:
                add_function()
            yield event
            if not add_before:
                add_function()

    def dataframe(self) -> pandas.DataFrame:
        data: dict[str, list[float]] = {
            event.event_name: list() for event in event_types.values()
        }
        del data[GoalEvent.event_name]
        data["GAME TIME"] = list()
        data["FINAL GOALS"] = list()
        for event in self.events_generator():
            if isinstance(event, GoalEvent):
                continue
            side = 0 if event.side == "home" else 1
            data[FreeKickEvent.event_name].append(self.free_kicks[side])
            data[FreeThrowEvent.event_name].append(self.throw_ins[side])
            data[ShotOnTargetEvent.event_name].append(self.shots_on[side])
            data[ShotOffTargetEvent.event_name].append(self.shots_off[side])
            data[PenaltyAwardedEvent.event_name].append(self.penalties[side])
            data["GAME TIME"].append(event.fractional_minutes())
            data["FINAL GOALS"].append(self.total_goals[side])
        return pandas.DataFrame(data=data)

    def __str__(self):
        return_str = "Match:"
        for attribute, value in vars(self).items():
            if attribute == "events":
                continue
            return_str += f" {attribute}={value},"
        return_str = return_str[:-1]
        for event in self.events:
            return_str += f"\n{event}"
        return return_str


if __name__ == "__main__":
    from matches.xml_parser import parse_file

    match = parse_file("300matches/27647274.xml")
    pandas.set_option('display.max_columns', 100)
    print(match.dataframe().head(10))
