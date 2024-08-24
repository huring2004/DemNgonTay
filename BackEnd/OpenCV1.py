import cv2

video = cv2.VideoCapture(0)

while True:
    cv2.imshow("came", video)
