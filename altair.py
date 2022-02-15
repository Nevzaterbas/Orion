import cv2
from pyzbar.pyzbar import decode

used_codes = []

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame,(640,480))
    for code in decode(frame):
        utf8 = code.data.decode('utf-8')
        if utf8 not in used_codes:
            print(utf8)
            used_codes.append(utf8)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break
cap.release()
cv2.destroyAllWindows()
