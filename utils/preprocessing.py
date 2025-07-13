# Functions for preprocessing soil images
from PIL import Image
import numpy as np
import cv2

IMG_SIZE = (224, 224)

def extract_color_features(image_path):
    image = Image.open(image_path).convert('RGB').resize(IMG_SIZE)
    img_np = np.array(image)

    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)
    lab = cv2.cvtColor(img_np, cv2.COLOR_RGB2Lab)

    features = []
    for i in range(3):
        features.append(img_np[:, :, i].mean())
        features.append(img_np[:, :, i].std())
    for i in range(3):
        features.append(hsv[:, :, i].mean())
        features.append(hsv[:, :, i].std())
    for i in range(3):
        features.append(lab[:, :, i].mean())
        features.append(lab[:, :, i].std())

    return np.array(features).reshape(1, -1)

