from pprint import pprint
from app import app
from app.models import Units, Spaces


def set_dual(num):
    dual = [111, 113, 114, 116, 121, 123, 124, 126,
            131, 133, 134, 136, 141, 143, 144, 146, 151, 153,
            154, 156, 161, 163, 164, 166, 171, 173, 174, 176,
            181, 183, 184, 186, 191, 193, 194, 196, 201, 203,
            204, 206, 211, 213, 214, 216, 221, 223, 224, 226,
            231, 233, 234, 236, 241, 243, 244, 246, 251, 253,
            254, 256, 261, 263, 264, 266, 271, 273, 274, 276]
    return True if num in dual else False


def set_locked(num):
    singles = [x for x in range(43, 259) if x not in range(48, 96) if x not in range(
        111, 181) if x not in range(183, 195) if x not in range(199, 225)]
    if num in range(48, 96) or num in range(217, 225):
        return num % 2 != 0
    elif num in singles:
        return False
    else:
        return num % 2 == 0


def set_uncovered(num):
    uncovered = [x for x in range(44, 229) if x not in range(101, 217)]
    return True if num not in uncovered else False


def set_reserved(num):
    reserved = [43, 101, 102, 103, 104, 105, 106, 107, 108, 181,
                230, 232, 234, 236, 238, 240, 242, 244, 245, 246,
                247, 248, 249, 250, 251, 252, 253, 254, 256, 258]
    return True if num in reserved else False


def get_neighbor(space):
    return (
        app.session.query(Spaces).filter_by(
            reserved=False, id=space.id-1).first(), space
    ) if space.locked else (space, app.session.query(Spaces).filter_by(reserved=False, id=space.id+1).first()
                            ) if space.num not in range(48, 96) or space.num not in range(217, 225) else (space, app.session.query(Spaces).filter_by(reserved=False, id=space.id+1).first()
                                                                                                          ) if space.locked else (app.session.query(Spaces).filter_by(reserved=False, id=space.id-1).first()
                                                                                                                                  )


def get_last_type(unit):
    i = len(unit.spaces) - 1
    if i == - 1:
        return None
    else:
        return 'Covered' if unit.spaces[i].covered else 'Uncovered'


def db_init():

    for i in range(11, 277):
        if str(i).endswith(('1', '2', '3', '4', '5', '6')):
            new_unity = Units(id=i, num=i, dual=set_dual(i))
            app.session.add(new_unity)
        else:
            i += 4

    for i in range(1, 261):
        new_space = Spaces(
            id=i,
            num=i,
            floor='Underground' if i < 216 else 'Ground Floor',
            covered=set_uncovered(i),
            reserved=set_reserved(i),
            locked=set_locked(i),
        )
        app.session.add(new_space)

    app.session.commit()
    print('Crude database initialized successfully.')
