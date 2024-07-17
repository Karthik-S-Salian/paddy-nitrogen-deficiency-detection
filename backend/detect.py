from fastapi import HTTPException
import numpy as np 
import cv2 
from normalizer import hsv_normalization
from io import BytesIO
from utils import rgb_to_hsv

class LeafNotFoundException(Exception):
    def __init__(self, message="Could not find any leaf in the image"):
        self.message = message
        super().__init__(self.message)

COLOR_UPPER = np.array((102,255,255), np.uint8)
COLOR_LOWER = np.array((25,52,72), np.uint8) 

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

def get_class_index(color_hsv):
    # Find the closest target color in HSV space
    closest_color_index = np.argmin(np.linalg.norm(np.array(TARGET_COLORS_HSV) - color_hsv, axis=1))
    return closest_color_index

def draw_contours(image, mask):
    image = image.copy()
    contour_mask = np.zeros(image.shape[:2],dtype=np.uint8)
    img_width,img_height = image.shape[:2]
    MIN_AREA = .01*img_width*img_height
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if (hierarchy[0, i, 3] == -1) and area>MIN_AREA: 
            cv2.drawContours(contour_mask, [contour], -1, 255, thickness=cv2.FILLED)

    return cv2.bitwise_and(image, image, mask=contour_mask)

def image_mean(hsv_image):
    # Reshape the image to a 2D array of RGB values
    reshaped_image = hsv_image.reshape((-1, 3))

    # Filter out black pixels (assuming black is [0, 0, 0] in RGB)
    non_black_pixels = reshaped_image[reshaped_image[:,2] != 0]
    if non_black_pixels.shape[0]==0:
        raise LeafNotFoundException()
    return np.mean(non_black_pixels, axis=0)


def predict_class(image_data:bytes):
    image_np = np.asarray(bytearray(BytesIO(image_data).read()), dtype=np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)
    
    hsv_image =cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    #applying normalization change whichever nprmalization you want here
    hsv_image = hsv_normalization(hsv_image)
    mask = cv2.inRange(hsv_image, COLOR_LOWER, COLOR_UPPER) 
    masked_image = draw_contours(hsv_image,mask) 

    try:
        mean = image_mean(masked_image)
    except LeafNotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

    class_index = get_class_index(mean)

    return get_message(class_index)    
