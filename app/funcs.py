def res_by_num(unity):
    return unity['num']


def res_by_covered(unity):
    return unity['slots'][-1]['tipo']


def res_by_floor(unity):
    return unity['slots'][-1]['piso']


def new_by_owner_id(slot):
    return slot.serialize['owner']


def new_by_slot_num(slot):
    return slot.serialize['num']


def new_by_slot_type(slot):
    return slot.serialize['covered']


def new_by_slot_floor(slot):
    return slot.serialize['floor']
