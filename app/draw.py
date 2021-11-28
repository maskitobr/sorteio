import json
from datetime import date
from random import choice, shuffle
from app import app
from app.models import Units, Slots, Results


def get_locked_index(slot, index):
    dif = 1 if slot.num not in range(48, 96) else (-1)
    if slot.num % 2 == 0:
        return index - dif
    else:
        return index + dif


def load_last_result():
    try:
        slots_q = app.session.query(Slots)
        res_q = app.session.query(Results).order_by(Results.id.desc()).first().result
        last = json.loads(str(res_q).replace("'", '"'))
        for unidade in last:
            for slot in unidade["slots"]:
                slots_q.filter(Slots.num == slot["vaga"]).update(
                    {Slots.owner_id: unidade["num"]}
                )
        return "Last result loaded successfully."
    except AttributeError as _e:
        raise _e


def save_new_result():
    query = app.session.query(Units).all()
    this_year = Results(year=date.today().year + 1, result=[i.serialize for i in query])
    app.session.add(this_year)
    try:
        app.session.commit()
        return "Draw result saved sucessfully."
    except Exception as _e:
        raise _e


def draw():

    load_last_result()

    sorteio_from = []

    # definindo query
    slots_q = app.session.query(Slots).filter_by(reserved=False).all()
    units_q = app.session.query(Units).all()
    shuffle(units_q)

    # sorteando duplas
    for unidade in filter(lambda x: x.dual, units_q):
        unc_slots = list(filter(lambda s: s.double and not s.covered, slots_q))
        cov_slots = list(filter(lambda s: s.double and s.covered, slots_q))

        # checando tipo de vaga
        if unidade.slots[-1].covered:
            sorteio_from = unc_slots if len(unc_slots) > 0 else cov_slots
        else:
            sorteio_from = cov_slots if len(cov_slots) > 0 else unc_slots

        # sorteando vaga e vaga vizinha
        sorteada = choice(sorteio_from)
        vizinha = sorteio_from[get_locked_index(sorteada, sorteio_from.index(sorteada))]

        # atribuindo novos usuarios
        sorteada.owner_id = unidade.num
        vizinha.owner_id = unidade.num

        # removendo sorteadas da lista
        del slots_q[slots_q.index(vizinha)]
        del slots_q[slots_q.index(sorteada)]

    # sorteando restante
    for unidade in filter(lambda x: not x.dual, units_q):
        unc_slots = list(filter(lambda s: not s.double and not s.covered, slots_q))
        cov_slots = list(filter(lambda s: not s.double and s.covered, slots_q))

        if unidade.slots[-1].covered:
            sorteio_from = (
                unc_slots
                if len(unc_slots) > 0
                else cov_slots
                if len(cov_slots) > 0
                else slots_q
            )
        else:
            sorteio_from = (
                cov_slots
                if len(cov_slots) > 0
                else unc_slots
                if len(unc_slots) > 0
                else slots_q
            )

        sorteada = choice(sorteio_from)
        sorteada.owner_id = unidade.num
        del slots_q[slots_q.index(sorteada)]

    app.session.commit()

    return app.session.query(Units)
