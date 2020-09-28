import cv2 
from matplotlib import pyplot as plt

# Read the image. 
img = cv2.imread('you_image.png')
# print(img)
# Apply bilateral filter
bilateral = cv2.bilateralFilter(img, 10, 60, 60)

# visualize original and processed images
fig = plt.figure()
fig.add_subplot(1, 2, 1)
plt.imshow(img)
plt.title("original image")
fig.add_subplot(1, 2, 2)
plt.imshow(bilateral)
plt.title("bilateral image")
plt.show()

  
# Save the output. 
cv2.imwrite('bilateral.jpg', bilateral) 
