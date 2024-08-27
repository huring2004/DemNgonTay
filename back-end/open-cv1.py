import cv2
import time
import os
import hand
cap = cv2.VideoCapture(0)
FolderPath = "photo-finger"
lst = os.listdir(f"../{FolderPath}") # đường dẫn ảnh trong thư mục photo-finger
img = []
for i in lst:
    tmp = cv2.imread(f"../{FolderPath}/{i}")
    img.append(tmp)

# Tạo cửa sổ và đặt chế độ toàn màn hình
# cv2.namedWindow('My Cam', cv2.WND_PROP_FULLSCREEN)
# cv2.setWindowProperty('My Cam', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

pTime = 0

dec = hand.handDetector(detectionCon=0.55) #detector

fgid = [4,8,12,16,20]

while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame,(900,700))
    frame = dec.findHands(frame)
    lmList = dec.findPosition(frame, draw= False) # tìm 20 điểm và đẩy vào list

    # tính fps
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    # show fps
    cv2.putText(frame,f"FPS: {int(fps)}",(120,40),
                cv2.FONT_HERSHEY_PLAIN,3, (300,20,100),3)

    if (len(lmList) != 0):
        fingers = []
        # code for short finger
        if(lmList[fgid[0]][1] > lmList[fgid[0]-1][1] ):
            fingers.append(1)
        else: fingers.append(0)
        # code for long finger
        for id in range(1,5):
            if(lmList[fgid[id]][2] < lmList[fgid[id]-2][2]):
                fingers.append(1)
            else: fingers.append(0)
        tmp = fingers.count(1)
        # h, w, c = img[tmp-1].shape
        # frame[:h, :w] = img[tmp-1]
        cv2.putText(frame, f"So: {tmp}", (120, 90),
                    cv2.FONT_HERSHEY_PLAIN, 3, (300, 20, 100), 3)

    cv2.imshow("My Cam", frame)
    if cv2.waitKey(1) == ord(" ") : break # nhấn phím space để kết thúc


cap.release()
cv2.destroyAllWindows()

