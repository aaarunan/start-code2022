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
    def from_match(
        cls, match: Match, events: list[Event], predicted_score
    ) -> "match_dto":
        home_team = team_dto(
            predicted_goals=predicted_score[0],
            actual_goals=match.total_goals[0],
            current_goals=match.goals[0],
            name=match.home_team.name,
            abbr=match.home_team.abbreviation,
        )
        away_team = team_dto(
            predicted_goals=predicted_score[1],
            actual_goals=match.total_goals[1],
            current_goals=match.goals[1],
            name=match.away_team.name,
            abbr=match.away_team.abbreviation,
        )
        event_dtos = []
        for event in events:
            event_dtos.append(
                event_dto(
                    event=event.event_name,
                    event_id=event.type,
                    minutes=event.minutes,
                    seconds=event.seconds,
                    perpetrator=event.side
                )
            )

        return cls(
            home_team=home_team,
            away_team=away_team,
            events=event_dtos,
            minutes=match.minutes,
        )
