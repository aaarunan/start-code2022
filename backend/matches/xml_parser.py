import os
import shlex
from typing import Iterator

import pandas
import tqdm

from matches.event import create_event, Event
from matches.match import Match

line_types = {"match": Match, "event": create_event}


def parse_line(xml_line: str) -> None | Event | Match:
    line = xml_line.strip().strip("<>")
    words = shlex.split(line)
    line_type = words[0]

    if line_type not in line_types:
        return None
    kwargs = {key: value for key, value in (word.split("=") for word in words[1:])}

    return line_types[line_type](**kwargs)


def parse_file(path: str) -> Match:
    with open(path, "r") as f:
        line = f.readline()
        match: Match = parse_line(line)
        while line := f.readline():
            event: Event | None = parse_line(line)
            if event is not None:
                match.events.append(event)
    match.set_total_goals()
    return match


def parse_folder(path: str) -> Iterator[Match]:
    print(os.getcwd())
    return (parse_file(os.path.join(path, file)) for file in os.listdir(path))


def create_and_save_csv(xml_folder_path: str, csv_path: str, loading_bar=True) -> pandas.DataFrame:
    matches = parse_folder(xml_folder_path)
    df = next(matches).dataframe()
    if loading_bar:
        matches = tqdm.tqdm(matches)
    for match in matches:
        df = pandas.concat((df, match.dataframe()), ignore_index=True)

    df.to_csv(csv_path, index=False)

    return df


if __name__ == "__main__":
    create_and_save_csv("300matches", "300matches.csv")
    create_and_save_csv("1000matches", "1000matches.csv")
