from enum import Enum

GENRE_MAPPING = {
    "0. POP": 0,
    "1. Anime": 1,
    "2. Kids": 2,
    "3. VOCALOID™ Music": 3,
    "4. Game Music": 4,
    "5. NAMCO Original": 5,
    "6. Variety": 6,
    "7. Classic": 7,
}

GENRE_COLOURS = {
    0: '#49d5eb',
    1: '#fe9e01',
    2: '#fe90d2',
    3: '#cbcfde',
    4: '#cc8aeb',
    5: '#ff7028',
    6: '#0acc2a',
    7: '#ded523'
}

class Language(Enum):
    JPN = 0
    ENG = 1
    zh_TW = 2
    KOR = 3
