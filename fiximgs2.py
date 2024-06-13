import argparse
import os
import sys
import cv2
import numpy as np

# Add the Real-ESRGAN directory to the Python path
sys.path.append(os.path.abspath("/home/plindsay/prjs/photo/Real-ESRGAN"))

from Real_ESRGAN.models import get_model_list, load_model

def enhance_image(input_image_path, output_image_path):
    image = cv2.imread(input_image_path, cv2.IMREAD_UNCHANGED)
    if image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)
    image = np.float64(image) / 255.0
    model_name = "REAL_ESRGAN_x4plus"
    models = get_model_list()
    assert model_name in models, "Invalid model name!"
    net = load_model(model_name, models[model_name])

    input_images = np.expand_dims(image, axis=0)
    result = net.inference(input_images, inference_mode="enhance")
    output_image = np.uint8(result[0] * 255.0)

    cv2.imwrite(output_image_path, output_image)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_dir", help="Input directory with PNG images")
    args = parser.parse_args()

    input_dir = args.input_dir
    output_dir = "enhanced"
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".png"):
            input_image_path = os.path.join(input_dir, filename)
            output_image_path = os.path.join(output_dir, filename)
            enhance_image(input_image_path, output_image_path)
