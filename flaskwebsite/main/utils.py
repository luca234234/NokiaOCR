import re

field_mapping = {
        'series': 'series',
        'number': 'number',
        'first_name': 'first_name',
        'last_name': 'last_name',
        'gender': 'gender',
        'place_of_birth': 'place_of_birth',
        'address': 'address',
        'issued_by': 'issued_by',
        'issue_date': 'issue_date',
        'expiry_date': 'expiry_date',
        'nationality': 'nationality',
        'personal_numerical_code': 'personal_numerical_code'
    }


def extract_data(ocr_results):
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
        'series': (r"S(erie|eria|ERIA)[\s:]*", r"\b[A-Z]{1,2}\b"),
        'number': (r"N(umar|o|UMAR|o)[\s:]*", r"\b\d{6}\b"),
        'first_name': (r"Prenume[\s:]*", r"\b[A-Za-z\-]{2,50}\b"),
        'last_name': (r"Nume[\s:]*", r"\b[A-Za-z\-]{2,50}\b"),
        'gender': (r"Sex[\s:]*", r"\b[MF]\b"),
        'place_of_birth': (r"Locul nasterii[\s:]*", r"[A-Za-z\s]+"),
        'address': (r"Adresa[\s:]*", r"[A-Za-z0-9\s,.]+"),
        'issued_by': (r"Eliberat de[\s:]*", r"[A-Za-z\s]+"),
        'issue_date': (r"Data eliberarii[\s:]*", r"\b\d{2}/\d{2}/\d{4}\b"),
        'expiry_date': (r"Data expirarii[\s:]*", r"\b\d{2}/\d{2}/\d{4}\b"),
        'nationality': (r"Nationalitate[\s:]*", r"\b[A-Za-z]+\b"),
        'personal_numerical_code': (r"CNP[\s:]*", r"\b\d{13}\b")
    }

    label_positions = {}
    for pattern_name, (label_pattern, _) in patterns.items():
        for bbox, text, _ in ocr_results:
            if re.search(label_pattern, text, re.IGNORECASE):
                label_positions[pattern_name] = bbox
                break

    for pattern_name, (label_pattern, value_pattern) in patterns.items():
        if pattern_name in label_positions:
            label_bbox = label_positions[pattern_name]
            closest_value = None
            closest_distance = float('inf')
            for bbox, text, _ in ocr_results:
                if re.match(value_pattern, text):
                    label_right = label_bbox[1][0]
                    label_top = label_bbox[0][1]
                    value_left = bbox[0][0]
                    value_top = bbox[0][1]
                    distance = abs(label_right - value_left) + abs(label_top - value_top)
                    if distance < closest_distance:
                        closest_distance = distance
                        closest_value = text
            if closest_value:
                id_card_data[pattern_name] = closest_value

    return id_card_data


def format_data(data):
    id_card_data = {
        'data_id': data.id,
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