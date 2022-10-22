from pydantic import BaseModel

from matches.match import Match


class team_dto(BaseModel):
    current_goals: int
    expected_goals: int
    actual_goals: int

