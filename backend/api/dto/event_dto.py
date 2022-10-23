from pydantic import BaseModel


class event_dto(BaseModel):
    event: str
    event_id: int
    minutes: int
    seconds: int
    perpetrator: str
