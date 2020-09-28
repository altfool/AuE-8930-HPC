import cv2
import numpy as np
from matplotlib import pyplot as plt

img = cv2.imread('messi5.jpg',0)
img2 = img.copy()
template = cv2.imread('messi_face.jpg',0)
# print(template)
w, h = template.shape[::-1]

# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']

for meth in methods:
    img = img2.copy()
    method = eval(meth)
    # print(method)
    # Apply template Matching
    match_result = cv2.matchTemplate(img, template, method)
    min_val, max_val, min_pos, max_pos = cv2.minMaxLoc(match_result)
    if method == "cv2.TM_SQDIFF" or method == "cv2.TM_SQDIFF_NORMED":
        top_left = min_pos
    else:
        top_left = max_pos
    # bottom_right = top_left + np.array([w,h])
    bottom_right = (top_left[0]+w, top_left[1]+h)
    # print(top_left, bottom_right)
    cv2.rectangle(img, top_left, bottom_right, 255, 1)

    # visualize
    fig = plt.figure()
    fig.suptitle("{}".format(meth), y=0.78, fontsize=16)
    fig.add_subplot(1, 2, 1)
    plt.imshow(match_result)
    plt.title("match result")
    fig.add_subplot(1, 2, 2)
    plt.imshow(img)
    plt.title("image detection")

    plt.show()
