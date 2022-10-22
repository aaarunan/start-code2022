from matches.event import create_event, Event
from matches.match import Match
import shlex

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
    return match

# def parse_folder(path: str) -> list[Match]:



if __name__ == "__main__":
    match = parse_file("300matches/27647274.xml")
    print(match)
