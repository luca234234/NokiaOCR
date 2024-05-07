import re

def extract_data(ocr_result):
    id_card_data = {
        'series': None,
        'number': None,
        'first_name': None,
        'last_name': None,
        'gender': None,
        'place_of_birth': None,
        'address': None,
        'issued_by': None,
        'issue_date': None,
        'expiry_date': None,
        'nationality': None,
        'personal_numerical_code': None
    }
    patterns = {
        'series': r"Serie: (\w+)",
        'number': r"Numar: (\d+)",
        'first_name': r"Prenume: ([a-zA-Z]+)",
        'last_name': r"Nume: ([a-zA-Z]+)",
        'gender': r"Sex: ([MF])",
        'place_of_birth': r"Locul nasterii: ([a-zA-Z]+)",
        'address': r"Adresa: ([\w, ]+)",
        'issued_by': r"Eliberat de: ([\w ]+)",
        'issue_date': r"Data eliberarii: (\d{2}/\d{2}/\d{4})",
        'expiry_date': r"Data expirarii: (\d{2}/\d{2}/\d{4})",
        'nationality': r"Nationalitate: ([a-zA-Z]+)",
        'personal_numerical_code': r"CNP: (\d{13})"
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, ocr_result)
        if match:
            id_card_data[key] = match.group(1)

    return id_card_data

def format_data(data):
    id_card_data = {
        'series': data.series,
        'number': data.number,
        'first_name': data.first_name,
        'last_name': data.last_name,
        'gender': data.gender,
        'place_of_birth': data.place_of_birth,
        'address': data.address,
        'issued_by': data.issued_by,
        'issue_date': data.issue_date,
        'expiry_date': data.expiry_date,
        'nationality': data.nationality,
        'personal_numerical_code': data.personal_numerical_code
    }
    return id_card_data