from pydantic import BaseModel


class Match_dto(BaseModel):
    # home_team: Team
    # away_team: Team
    # events: list[Event]
    minutes: int
    goals: list[int]
    free_kicks: list[int]
    throw_ins: list[int]
    shots_on: list[int]
    shots_off: list[int]
    penalties: list[int]
