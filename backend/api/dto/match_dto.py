from pydantic import BaseModel

from api.dto.event_dto import event_dto
from matches.event import Event
from matches.match import Match
from api.dto.team_dto import team_dto


class match_dto(BaseModel):
    home_team: team_dto
    away_team: team_dto
    events: list[event_dto]
    minutes: int

    @classmethod
    def from_match(cls, match: Match, events: list[Event], predicted_score) -> "match_dto":
        home_team = team_dto(predicted_goals=predicted_score[0], actual_goals=match.total_goals[0], current_goals=match.goals[0])
        away_team = team_dto(predicted_goals=predicted_score[1], actual_goals=match.total_goals[1], current_goals=match.goals[1])
        event_dtos = []
        for event in events:
            event_dtos.append(event_dto(event=event.event_name, event_id=event.type))

        return cls(home_team=home_team, away_team=away_team, events=event_dtos, minutes=match.minutes)
