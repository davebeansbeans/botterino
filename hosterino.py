from geopy.distance import distance
from geopy.point import Point
from config import donotreply, incorrect, pg, coords_not_found
from random import choice
import re

# google maps decimal or dms
decimal_or_DMS = re.compile(
    """(?:((?:[-+]?\d{1,2}[.]\d+),\s*(?:[-+]?\d{1,3}[.]\d+))|(\d{1,3}°\d{1,3}'\d{1,3}\.\d\"[N|S]\s\d{1,3}°\d{1,3}'\d{1,3}\.\d\"[E|W]))"""
)

# google earth formats, other formats
everything_else = re.compile(
     """(^| )(-?\d{1,2}(\.\d+)?(?=\s*,?\s*)[\s,]+-?\d{1,3}(\.\d+)?|\d{1,2}(\.\d+°|°(\d{1,2}(\.\d+'|'(\d{1,2}(\.\d+)?\")?))?)[NS](?=\s*,?\s*)[\s,]+\d{1,3}(\.\d+°|°(\d{1,2}(\.\d+'|'(\d{1,2}(\.\d+)?\")?))?)[EW])"""
)

def get_distance(guess, answer):
    match = re.search(decimal_or_DMS, guess)
    if not match:
        match = re.search(everything_else, guess)
        if not match:
            return
    coord = Point(match[0])
    try:
        return distance(coord, answer).m
    except Exception as e:
        print('There was a problem in getting distance', e)


def check(submission, answer, tolerance):
    answer = Point(answer)
    for c in pg.stream.comments(skip_existing=True):
        wrong = choice(incorrect)
        if (c.author.name.lower() not in donotreply
                and c.submission == submission):
            error = get_distance(c.body, answer)
            result = '+correct' if error is not None and error <= tolerance else wrong
            c.reply(result if error is not None else coords_not_found)
            print(f'{c.author}\'s guess {c.body} was {error} meters off')
            if '+correct' == result:
                return
