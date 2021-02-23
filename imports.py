import re
import pdfplumber
from app import app
from app.models import Units, Spaces, Results
from secrets import files_path


def get_space_id(num):
    return app.session.query(Spaces).get(num)


def get_unit_id(num):
    return app.session.query(Units).get(num)


def import_2021():

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
                    space = get_space_id(match_single.group(2))
                    space.owner = get_unit_id(match_single.group(1))

                if match_dual:
                    space_1 = get_space_id(match_dual.group(2))
                    space_2 = get_space_id(match_dual.group(3))
                    space_1.owner = get_unit_id(match_dual.group(1))
                    space_2.owner = get_unit_id(match_dual.group(1))

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2021,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()


def import_2020():

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
                    space = get_space_id(match_single.group(2))
                    space.owner = get_unit_id(match_single.group(1))

                if match_dual:
                    space_1 = get_space_id(match_dual.group(2))
                    space_2 = get_space_id(match_dual.group(3))
                    space_1.owner = get_unit_id(match_dual.group(1))
                    space_2.owner = get_unit_id(match_dual.group(1))

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2020,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()


def import_2019():

    with open(files_path+'resultado-sorteio-2019.txt', 'r') as f:
        for line in f:
            res = line.replace('\n', '').split(',')
            if res[2] in '-':
                space = get_space_id(res[1])
                space.owner = get_unit_id(res[0])
            else:
                space_1 = get_space_id(res[1])
                space_2 = get_space_id(res[2])
                space_1.owner = get_unit_id(res[0])
                space_2.owner = get_unit_id(res[0])

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2019,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()


def import_2018():

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
                    space_1 = get_space_id(match.group(2))
                    space_2 = get_space_id(match.group(3))
                    space_1.owner = get_unit_id(match.group(1))
                    space_2.owner = get_unit_id(match.group(1))

    with pdfplumber.open(file_singles) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            for line in text.split('\n'):
                match = re.search(match_singles, line)

                if match:
                    space = get_space_id(match.group(2))
                    space.owner = get_unit_id(match.group(1))

    query = app.session.query(Units).order_by(Units.dual).all()
    this_year = Results(year=2018,
                        result=[i.serialize for i in query])
    app.session.add(this_year)

    app.session.commit()
