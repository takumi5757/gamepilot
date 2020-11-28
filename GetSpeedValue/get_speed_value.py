from PIL import ImageGrab
from PIL import Image
import sys
import pyocr
import pyocr.builders


def get_speed_value(tool):
    """ディスプレイ左上に置いた1280*720のeurotruck2の画面から、speedを読み取る
    Args:
        tool(module):OCR(tesseract)
    """
    bbox = (1000, 510, 1020, 530)

    while True:
        try:
            temp_pil_im = ImageGrab.grab(bbox=bbox)

            txt = tool.image_to_string(
                temp_pil_im,
                lang="eng",
                builder=pyocr.builders.DigitBuilder(tesseract_layout=6),
            )
            if txt.isdigit():
                print(f"speed:{int(txt)}")

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
    import cv2

    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
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
    ocr_tool = setup_ocr()
    get_speed_value(ocr_tool)