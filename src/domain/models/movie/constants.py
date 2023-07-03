from enum import IntEnum


class MovieStatusEnum(IntEnum):

    RELEASED = 0
    CANCELED = 1
    PLANNED = 2


class MPAAEnum(IntEnum):

    G = 0
    PG = 1
    PG13 = 2
    R = 3
    NC17 = 4


class MovieGenreEnum(IntEnum):

    ACTION = 0
    THRILLER = 1
    COMEDY = 2
    WAR = 3
    DOCUMENTARY = 4
    CRIME = 5
    DRAMA = 6
    ROMANCE = 7
    FANTASY = 8
    ADVENTURE = 9
    HORROR = 10
    MUSICAL = 11
    MYSTERY = 12
    SCIENCE_FICTION = 13
    WESTERN = 14
    HISTORY = 15
    BIOGRAPHY = 16
    ANIMATION = 17

