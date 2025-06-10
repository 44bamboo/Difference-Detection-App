import cv2

cap = cv2.VideoCapture(1)

cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
cap.set(cv2.CAP_PROP_AUTO_WB, 0)

count = 1
while(True):
    ret, frame = cap.read()
    cv2.imshow("output", frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    if key == ord('s'):
        print("test")
        cv2.imwrite('D:/new_project/IMG/test' + str(count)+'.jpg', frame)
        count = count + 1

