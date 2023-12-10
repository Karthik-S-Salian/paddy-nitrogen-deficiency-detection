import numpy as np 
import cv2 
import matplotlib.pyplot as plt
from normalizer import hsv_normalization
from io import BytesIO
from utils import rgb_to_hsv

COLOR_UPPER = (102,255,255)
COLOR_LOWER = (25,52,72)

TARGET_COLORS = [
    (174,249,101),
    (133,204,64),
    (104,168,42),
    (64,115,15),
    (33,62,5)
]

TARGET_COLORS_HSV = [rgb_to_hsv(color) for color in TARGET_COLORS]

MESSAGE = ['No2 Deficiency observed - Class 1:  \n Apply N-Fertilizer immediately', 
            'N02 Deficiency observed - Class 2: \n Apply N-Fertilizer soon', 
            'Ideal range - Class 3: \n Do not apply N-Fertilizer and continue to monitor closely', 
            'Ideal range - Class 4: \n Do not apply N-Fertilizer and continue to monitor'
        ]

def get_message(index:int):
    return MESSAGE[index]

def get_class_index(input_color):
    # Convert colors to HSV
    color_hsv = rgb_to_hsv(input_color)
    # Find the closest target color in HSV space
    closest_color_index = np.argmin(np.linalg.norm(np.array(TARGET_COLORS_HSV) - color_hsv, axis=1))
    return closest_color_index

def draw_contours(image, mask):
    image = image.copy()
    img_width,img_height = image.shape[:2]
    MIN_AREA = .2*img_width*img_height
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (hierarchy[0, i, 3] == -1) and area>MIN_AREA:
            contour_mask = np.zeros(image.shape[:2],dtype=np.uint8)
            cv2.drawContours(contour_mask, [contour], -1, 255, thickness=cv2.FILLED)
            image = cv2.bitwise_and(image, image, mask=contour_mask)

    return image

def mode_of_image(image):
    # Reshape the image to a 2D array of RGB values
    reshaped_image = image.reshape((-1, 3))

    # Filter out black pixels (assuming black is [0, 0, 0] in RGB)
    non_black_pixels = reshaped_image[np.any(reshaped_image != [0, 0, 0], axis=1)]

    # Find unique values and their counts for non-black pixels
    unique_values, counts = np.unique(non_black_pixels, axis=0, return_counts=True)

    # Find the index/indices of the maximum count(s)
    max_count_indices = np.where(counts == counts.max())[0]

    # The mode(s) is/are the corresponding unique value(s)
    modes = unique_values[max_count_indices]

    return np.mean(modes,axis=0).astype(np.uint8)


def predict_class(image_data:bytes):
    image_np = np.asarray(bytearray(BytesIO(image_data).read()), dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    #applying normalization change whichever nprmalization you want here
    normalized_image = hsv_normalization(image)

    hsv_image = cv2.cvtColor(normalized_image, cv2.COLOR_BGR2HSV)

    green_lower = np.array(COLOR_LOWER, np.uint8) 
    green_upper = np.array(COLOR_UPPER, np.uint8) 
    green_mask = cv2.inRange(hsv_image, green_lower, green_upper) 

    masked_image = draw_contours(hsv_image,green_mask) 

    mode_color = mode_of_image(masked_image)

    class_index = get_class_index(mode_color)

    return get_message(class_index)    
