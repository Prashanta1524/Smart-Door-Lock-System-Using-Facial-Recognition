import cv2
import numpy as np
from pyzbar import pyzbar

# Initialize the camera
vid = cv2.VideoCapture(0)
vid.set(3, 640)  # Set the width of the camera feed
vid.set(4, 740)  # Set the height of the camera feed

while True:
    success, img = vid.read()
    barcodes = pyzbar.decode(img)  # Use pyzbar.decode instead of decode
    for barcode in barcodes:
        text = barcode.data.decode('utf-8')
        print(text)
        polygon_Points = np.array([barcode.polygon], np.int32)
        polygon_Points = polygon_Points.reshape(-1, 1, 2)
        rect_Points = barcode.rect
        cv2.polylines(img, [polygon_Points], True, (255, 255, 0), 5)
        cv2.putText(img, text, (rect_Points[0], rect_Points[1]), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 0), 2)
    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Add a condition to break the loop when 'q' is pressed
        break

vid.release()
cv2.destroyAllWindows()