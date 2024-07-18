import string
import easyocr

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=True)


def read_license_plate(license_plate_crop):
    """
    Read the license plate text from the given cropped image.
    """
    detections = reader.readtext(license_plate_crop)
    
    result_text = ''.join(text.upper().replace(' ', '') for _, text, _ in detections)
    scores = [score for _, _, score in detections]
    
    return result_text, scores


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
