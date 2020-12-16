from easyocr import Reader
from easyocr.utils import reformat_input
import cv2

image = cv2.imread("doc_734_0.jpg")

reader = Reader(["th", "en"])

img, img_cv_grey = reformat_input(image)
horizontal_list, free_list = reader.detect(img)

results = reader.detect(img_cv_grey, horizontal_list, free_list)

for data in results:
    print(data)
