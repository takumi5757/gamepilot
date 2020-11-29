from PIL import ImageGrab
from PIL import Image
import sys
import pyocr
import pyocr.builders
import argparse
import xgboost as xgb
import numpy as np
import cv2


def get_speed_value(mode="xgb"):
    """ディスプレイ左上に置いた1280*720のeurotruck2の画面から、speedを読み取る
    Args:
        tool(module):OCR(tesseract)
    """
    bbox = (1000, 510, 1016, 526)

    if mode == "ocr":
        tool = setup_ocr()
        while True:
            try:
                temp_pil_im = ImageGrab.grab(bbox=bbox)

                speed_value = tool.image_to_string(
                    temp_pil_im,
                    lang="eng",
                    builder=pyocr.builders.DigitBuilder(tesseract_layout=6),
                )
                if txt.isdigit():
                    print(f"speed:{int(speed_value)}")

            except KeyboardInterrupt:
                print("end")
                break

    if mode == "xgb":
        bst = xgb.Booster(model_file="models/xgbClassifier.json")

        while True:
            try:
                temp_pil_im = ImageGrab.grab(bbox=bbox)
                im_normalized = np.asarray(temp_pil_im) / 255.0
                speed_value = bst.predict(xgb.DMatrix(im_normalized.reshape(1, 768)))

                print(f"speed:{int(speed_value)}")

            except KeyboardInterrupt:
                print("end")
                break


def cv2pil(image):
    """OpenCV型→PIL型

    Args:
        image(np.ndarray): OpenCVで読んだ画像データ
    Return:
        new_image(PIL.Image.Image):PIL型の画像データ
    """

    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def pil2cv(image):
    """ PIL型 -> OpenCV型 """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGBA2BGRA)
    return new_image


def setup_ocr():
    """pyocrを立ち上げる

    Return:
        tool(module):OCR(tesseract)
    """
    # OCRの準備
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    # The tools are returned in the recommended order of usage
    tool = tools[0]
    print("Will use tool '%s'" % (tool.get_name()))

    langs = tool.get_available_languages()
    print("Available languages: %s" % ", ".join(langs))
    lang = langs[0]
    print("Will use lang '%s'" % (lang))
    return tool


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ocr", action="store_true", help="use ocr")
    args = parser.parse_args()

    if args.ocr:
        get_speed_value(mode="ocr")
    else:
        get_speed_value(mode="xgb")