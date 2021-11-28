from app import app
from app.models import Units, Slots


def set_dual(num):
    if str(num).endswith(("2", "5")):
        return False
    else:
        return True if num > 110 else False


def set_double(num):
    singles = [
        x
        for x in range(43, 259)
        if x not in range(48, 96)
        if x not in range(111, 181)
        if x not in range(183, 195)
        if x not in range(199, 225)
    ]
    return False if num in singles else True


def set_uncovered(num):
    uncovered = [x for x in range(44, 229) if x not in range(101, 217)]
    return True if num not in uncovered else False


def set_reserved(num):
    reserved = [
        43,
        101,
        102,
        103,
        104,
        105,
        106,
        107,
        108,
        181,
        230,
        232,
        234,
        236,
        238,
        240,
        242,
        244,
        245,
        246,
        247,
        248,
        249,
        250,
        251,
        252,
        253,
        254,
        256,
        258,
    ]
    return True if num in reserved else False


def db_init():

    for i in range(11, 277):
        if str(i).endswith(("1", "2", "3", "4", "5", "6")):
            new_unity = Units(id=i, num=i, dual=set_dual(i))
            app.session.add(new_unity)

        else:
            i += 4

    for i in range(1, 261):
        new_slot = Slots(
            id=i,
            num=i,
            floor="Subsolo" if i < 216 else "Terreo",
            covered=set_uncovered(i),
            reserved=set_reserved(i),
            double=set_double(i),
        )
        app.session.add(new_slot)

    app.session.commit()
