from pydantic import BaseModel

from matches.match import Match


class team_dto(BaseModel):
    current_goals: int
    predicted_goals: int
    actual_goals: int

