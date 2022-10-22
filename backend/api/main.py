from fastapi import FastAPI

from matches.event import Event
from matches.xml_parser import parse_file
from api.dto.match_dto import Match_dto

app = FastAPI()
match = parse_file('matches/300matches/27647274.xml')

match_gen = match.event_per_minute()


@app.get("/next-minute")
async def get_next_match():
    events: list[Event] = next(match_gen)
    return Match_dto(**vars(match)).dict()


@app.get("/reset")
async def reset_match():
    global match_gen
    match_gen = match.event_per_minute()
    return "Success!"
