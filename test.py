import cv2
import imutils
import _utils

import sys
import numpy as np
np.set_printoptions(threshold=sys.maxsize)

img = _utils.read_img("test.png")
img = cv2.resize(img, (620, 480))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # convert to grey scale
gray = cv2.bilateralFilter(gray, 11, 17, 17)  # Blur to reduce noise
edged = cv2.Canny(gray, 30, 200)  # Perform Edge detection

# find contours in the edged image, keep only the largest
# ones, and initialize our screen contour
cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:10]
screenCnt = None

# loop over our contours
for c in cnts:
    # approximate the contour
    peri = cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, _utils.APRROX_POLY_DP * peri, True)

    # if our approximated contour has four points, then
    # we can assume that we have found our screen
    if len(approx) == 4:
        screenCnt = approx
        break

if screenCnt is None:
    detected = 0
    print("No contour detected")
else:
    detected = 1

if detected == 1:
    cv2.drawContours(img, [screenCnt], -1, (0, 255, 0), 3)

# Masking the part other than the number plate
mask = np.zeros(gray.shape, np.uint8)
cv2.drawContours(mask, [screenCnt], 0, 255, -1)
print(np.shape(mask))
print(np.shape(img))

# cv2.imshow("mask", mask)
# print(mask)
new_image = cv2.bitwise_and(img,img,mask=mask)


# cv2.imshow('mask', mask)
cv2.waitKey(0)
cv2.destroyAllWindows()