import re
import pdfplumber
from app import app
from app.models import Units, Slots, Results
from secrets import files_path


def get_slot_id(num):
    return app.session.query(Slots).filter(Slots.num == num).first()


def get_unit_id(num):
    return app.session.query(Units).filter(Units.num == num).first()


def bulk_data():
    return app.session.query(Slots).update({Slots.owner_id: None})


def import_2021():

    bulk_data()

    file_2021 = files_path+'resultado-sorteio-2021.pdf'
    single_re = r"^(\d{2,3})\s(\d{1,3})\s(\D+?)\s(\D+$)"
    dual_re = r"^(\d{2,3})\s(\d{1,3})\s(\d{1,3})\s(\D+?)\s(\D+$)"

    with pdfplumber.open(file_2021) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                match_single = re.search(single_re, line)
                match_dual = re.search(dual_re, line)

                if match_single:
                    slot = get_slot_id(match_single.group(2))
                    slot.owner = get_unit_id(match_single.group(1))

                if match_dual:
                    slot_1 = get_slot_id(match_dual.group(2))
                    slot_2 = get_slot_id(match_dual.group(3))
                    slot_1.owner = get_unit_id(match_dual.group(1))
                    slot_2.owner = get_unit_id(match_dual.group(1))

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2021,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()


def import_2020():

    bulk_data()

    file_2020 = files_path+'resultado-sorteio-2020.pdf'
    single_re = r"^(\d{2,3})\s(\d{1,3})\s(\D+?)\s(\D+$)"
    dual_re = r"^(\d{2,3})\s(\d{1,3})\s(\d{1,3})\s(\D+?)\s(\D+$)"

    with pdfplumber.open(file_2020) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                match_single = re.search(single_re, line)
                match_dual = re.search(dual_re, line)

                if match_single:
                    slot = get_slot_id(match_single.group(2))
                    slot.owner = get_unit_id(match_single.group(1))

                if match_dual:
                    slot_1 = get_slot_id(match_dual.group(2))
                    slot_2 = get_slot_id(match_dual.group(3))
                    slot_1.owner = get_unit_id(match_dual.group(1))
                    slot_2.owner = get_unit_id(match_dual.group(1))

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2020,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()


def import_2019():

    bulk_data()

    with open(files_path+'resultado-sorteio-2019.txt', 'r') as f:
        for line in f:
            res = line.replace('\n', '').split(',')
            if res[2] in '-':
                slot = get_slot_id(res[1])
                slot.owner = get_unit_id(res[0])
            else:
                slot_1 = get_slot_id(res[1])
                slot_2 = get_slot_id(res[2])
                slot_1.owner = get_unit_id(res[0])
                slot_2.owner = get_unit_id(res[0])

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2019,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()


def import_2018():

    bulk_data()

    file_singles = files_path+'resultado-sorteio-2018-singles.pdf'
    file_duals = files_path+'resultado-sorteio-2018-duals.pdf'
    match_singles = r"(\d{2,3})\s.+Vaga:\s(\d{1,3})"
    match_duals = r"(\d{3})\s.+Vagas:\s(\d{1,3}) e (\d{1,3})"

    with pdfplumber.open(file_duals) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                match = re.search(match_duals, line)

                if match:
                    slot_1 = get_slot_id(match.group(2))
                    slot_2 = get_slot_id(match.group(3))
                    slot_1.owner = get_unit_id(match.group(1))
                    slot_2.owner = get_unit_id(match.group(1))

    with pdfplumber.open(file_singles) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                match = re.search(match_singles, line)

                if match:
                    slot = get_slot_id(match.group(2))
                    slot.owner = get_unit_id(match.group(1))

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2018,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()
