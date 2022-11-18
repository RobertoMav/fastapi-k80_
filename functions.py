import cv2 as cv
import os
import numpy as np
from datetime import datetime
import tflite_runtime.interpreter as tflite
from pathlib import Path
import json

def return_pic():
    cam = cv.VideoCapture(0)

    if not cam.isOpened():
        print("cant open camera")
        exit()
    path = r"C:\Users\Roberto\Documents\Codes\Pot-Filler\Pics"

    os.chdir(path)

    global image_name
    global image

    while True:
        ret, frame = cam.read()
        if not ret:
            print("cant receive frame")
            break
        
        mirror = cv.flip(frame, 1)
        now = datetime.now()
        name = now.strftime("%Y_%m_%d__%H_%M_%S")
        img_name = "img_{}.png".format(name)
        image_name = img_name

        cv.imwrite(img_name, mirror)
        image = cv.imread(path + "\\" +image_name)
        print(f"written img: {img_name}")
        break

    cam.release()
    cv.destroyAllWindows()

    return image_name, image


def adj_img(image):
    width = int(224)
    dim = (width, width)
    img_resize = cv.resize(image, dim)
    adjusted_image = np.expand_dims(img_resize, axis=0)
    return adjusted_image

BASE_DIR = Path(__file__).resolve(strict=True).parent

MODEL = tflite.Interpreter('model.tflite')

def predict_pipeline():
    MODEL.allocate_tensors()
    input_details = MODEL.get_input_details()
    output_details = MODEL.get_output_details()

    img_name, img = return_pic()
    image = adj_img(img)

    MODEL.set_tensor(input_details[0]['index'], image.astype(np.float32))

    MODEL.invoke()

    output_data = MODEL.get_tensor(output_details[0]['index'])

    pred = float(output_data[0][0])
    return img_name, pred

def to_json():
    img_name, pred = predict_pipeline()
    dict = {"image": img_name, "output": pred}
    return json.dumps(dict, indent=4)
