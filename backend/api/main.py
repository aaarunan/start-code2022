import pandas
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from matches.event import Event
from matches.xml_parser import parse_file
from api.dto.match_dto import match_dto
from sportradar_ml.forest_reg import load_model_from_joblib, get_new_prediction
from sportradar_ml.forest_reg import get_new_prediction

app = FastAPI()
match = parse_file('matches/300matches/27647274.xml')
rf = load_model_from_joblib('rf')

match_gen = match.event_per_minute()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.get("/next-minute")
async def get_next_match():
    events: list[Event] = next(match_gen)
    home_data = pandas.DataFrame(data=match.last_event_data(0))
    away_data = pandas.DataFrame(data=match.last_event_data(1))
    predictions = (get_new_prediction(home_data, rf), get_new_prediction(away_data, rf))
    return match_dto.from_match(match, events, predictions).dict()


@app.get("/reset")
async def reset_match():
    global match_gen
    match_gen = match.event_per_minute()
    return "Success!"
