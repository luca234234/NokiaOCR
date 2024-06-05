import re
import logging
import unicodedata

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


def normalize_string(s):
    s = s.strip().lower()
    s = ''.join(
        c for c in unicodedata.normalize('NFD', s)
        if unicodedata.category(c) != 'Mn'
    )
    return s


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
        'personal_numerical_code': None,
        'date': None
    }

    patterns = {
        'series': ('seria', r"\b[A-Z]{2}\b"),
        'number': ('nr', r"\b\d{6}\b"),
        'first_name': ('prenume', r"\b[A-Z\s]+\b"),
        'last_name': ('nume', r"\b[A-Z]+\b"),
        'gender': ('sex', r"\b[M|F]\b"),
        'place_of_birth': ('loc nastere', r".*\b(Jud\.|Mun\.)\b.*"),
        'address': ('domiciliu', r".*\b(Str\.|nr\.)\b.*"),
        'issued_by': ('emisa de', r".*\bSPCLEP\b.*"),
        'nationality': ('cetatenie', r"\bROU\b"),
        'personal_numerical_code': ('cnp', r"\b\d{13}\b"),
        'date': ('valabilitate', r"\b\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{4}\b"),
    }

    label_positions = {}
    for pattern_name, (label_str, _) in patterns.items():
        closest_match = None
        closest_distance = float('inf')
        closest_length_difference = float('inf')

        for result in ocr_results[0]['results']:
            text = normalize_string(result['text'])
            label_str_normalized = normalize_string(label_str)
            if len(text) < len(label_str_normalized):
                continue
            for i in range(len(text) - len(label_str_normalized) + 1):
                substring = text[i:i + len(label_str_normalized)]
                distance = sum(1 for a, b in zip(substring, label_str_normalized) if a != b)
                length_difference = abs(len(substring) - len(label_str_normalized))

                if (distance < closest_distance) or (
                        distance == closest_distance and length_difference < closest_length_difference):
                    closest_distance = distance
                    closest_length_difference = length_difference
                    closest_match = result

        if closest_match:
            label_positions[pattern_name] = closest_match['bound_box']

    for pattern_name, (label_str, value_pattern) in patterns.items():
        if pattern_name in label_positions:
            label_bbox = label_positions[pattern_name]
            closest_value = None
            closest_distance = float('inf')

            for result in ocr_results[0]['results']:
                text = result['text']
                bbox = result['bound_box']
                if re.match(value_pattern, text):
                    if pattern_name in ['personal_numerical_code', 'series', 'number']:
                        if bbox[0][0] > label_bbox[1][0]:  # To the right
                            label_right = label_bbox[1][0]
                            label_top = label_bbox[0][1]
                            value_left = bbox[0][0]
                            value_top = bbox[0][1]
                            distance = abs(label_right - value_left) + abs(label_top - value_top)
                            if distance < closest_distance:
                                closest_distance = distance
                                closest_value = text
                    else:
                        if bbox[0][1] > label_bbox[1][1]:  # Below
                            label_left = label_bbox[0][0]
                            label_bottom = label_bbox[1][1]
                            value_left = bbox[0][0]
                            value_top = bbox[0][1]
                            distance = abs(label_left - value_left) + abs(label_bottom - value_top)
                            if distance < closest_distance:
                                closest_distance = distance
                                closest_value = text

            if not closest_value:  # If no value found in the expected area, search the whole list
                for result in ocr_results[0]['results']:
                    text = result['text']
                    bbox = result['bound_box']
                    if re.match(value_pattern, text):
                        label_left = label_bbox[0][0]
                        label_top = label_bbox[0][1]
                        value_left = bbox[0][0]
                        value_top = bbox[0][1]
                        distance = abs(label_left - value_left) + abs(label_top - value_top)
                        if distance < closest_distance:
                            closest_distance = distance
                            closest_value = text

            if closest_value:
                if pattern_name == 'date':
                    issue_date, expiry_date = closest_value.split('-')
                    id_card_data['issue_date'] = issue_date.strip()
                    id_card_data['expiry_date'] = expiry_date.strip()
                else:
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