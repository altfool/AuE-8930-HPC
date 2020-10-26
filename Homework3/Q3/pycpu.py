import cv2
import time

def main():
    img_path = './mycat.png'
    image = cv2.imread(img_path)

    start = time.time()
    # convert image from RGB to HSV
    img_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    # Histogram equalisation on the V-channel
    img_hsv[:, :, 2] = cv2.equalizeHist(img_hsv[:, :, 2])

    # convert image back from HSV to RGB
    image = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)

    end = time.time()
    print("CPU Time: %.5f s" % (end - start))

    cv2.imwrite('./cpu_mycat.png', image)

if __name__ == '__main__':
    main()
