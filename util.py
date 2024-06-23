import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)

# Mapping dictionaries for character conversion
fuel_dict = {'D': '-', 'P': '-', '-': '-'}
first_letter_province_dict = {'H': 'W', 'C': 'C', 'E': 'E', 'N': 'N', 'S': 'S', '5': 'S', 'W': 'W', 'U': 'U'}
second_letter_province_dict = {'H': 'W', 'C': 'C', 'W': 'W', 'P': 'P', 'G': 'G', '6': 'G'}
dict_char_to_int = {'O': '0', 'I': '1', 'J': '3', 'A': '4', 'G': '6', 'S': '5', 'T': '7'}
dict_int_to_char = {'0': 'O', '1': 'I', '3': 'J', '4': 'A', '6': 'G', '5': 'S', '7': 'T'}

def license_complies_format(text):
    """
    Check if the license plate text complies with the required format.
    """
    if len(text) > 10:
        return False
    if len(text) == 9:
        return (text[0] in string.ascii_uppercase or text[0] in first_letter_province_dict.keys()) and \
               (text[1] in string.ascii_uppercase or text[1] in second_letter_province_dict.keys()) and \
               all(char in string.ascii_uppercase or char in string.digits for char in text[2:])
    elif len(text) == 8:
        return (text[0] in string.ascii_uppercase or text[0] in first_letter_province_dict.keys()) and \
               (text[1] in string.ascii_uppercase or text[1] in second_letter_province_dict.keys()) and \
               all(char in string.ascii_uppercase or char in string.digits for char in text[2:])
    return False

def format_license(text):
    """
    Format the license plate text by converting characters using the mapping dictionaries.
    """
    if len(text) == 9:
        mapping = {0: first_letter_province_dict, 1: second_letter_province_dict, 
                   2: dict_int_to_char, 3: dict_int_to_char, 4: fuel_dict, 
                   5: dict_char_to_int, 6: dict_char_to_int, 7: dict_char_to_int, 8: dict_char_to_int}
        return ''.join(mapping[j].get(text[j], text[j]) for j in range(9))
    return text

def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.
    """
    detections = reader.readtext(license_plate_crop)
    result_text = ''.join(text.upper().replace(' ', '') for _, text, _ in detections)
    
    # print(f'recognized_plate -> {result_text}, {len(result_text)}')
    
    if license_complies_format(result_text):
        formatted_text = format_license(result_text)
        # print(f'formatted_plate -> {formatted_text}')
        # return formatted_text, None  # Adjust confidence score calculation as needed
    return result_text, None


def get_car(license_plate, vehicle_track_ids):
    """
    Retrieve the vehicle coordinates and ID based on the license plate coordinates.

    Args:
        license_plate (tuple): Tuple containing the coordinates of the license plate (x1, y1, x2, y2, score, class_id).
        vehicle_track_ids (list): List of vehicle track IDs and their corresponding coordinates.

    Returns:
        tuple: Tuple containing the vehicle coordinates (x1, y1, x2, y2) and ID.
    """
    x1, y1, x2, y2, score, class_id = license_plate

    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]

        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break

    if foundIt:
        return vehicle_track_ids[car_indx]

    return -1, -1, -1, -1, -1
