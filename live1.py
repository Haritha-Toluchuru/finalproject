import cv2
from ultralytics import YOLO
import numpy as np

# Load YOLOv9 model
model12 = YOLO('Fruits_rippen_detection.pt')

class_dict = {
    0: "apple overripe",
    1: "apple ripe",
    2: "apple rotten",
    3: "apple unripe",
    4: "banana overripe",
    5: "banana ripe",
    6: "banana rotten",
    7: "banana unripe",
    8: "grape overripe",
    9: "grape ripe",
    10: "grape rotten",
    11: "grape unripe",
    12: "mango overripe",
    13: "mango ripe",
    14: "mango rotten",
    15: "mango unripe",
    16: "melon overripe",
    17: "melon ripe",
    18: "melon rotten",
    19: "melon unripe",
    20: "orange overripe",
    21: "orange ripe",
    22: "orange rotten",
    23: "orange unripe",
    24: "peach overripe",
    25: "peach ripe",
    26: "peach rotten",
    27: "peach unripe",
    28: "pear overripe",
    29: "pear ripe",
    30: "pear rotten",
    31: "pear unripe"
}

# Open webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Use the frame as-is, without converting to RGB
    input_frame = frame

    # Run prediction on the frame directly
    results = model12.predict(source=input_frame, conf=0.3, save=False, verbose=False)
    result = results[0]
    annotated_frame = result.plot()

    # Draw class labels with confidence
    if result.boxes is not None and len(result.boxes) > 0:
        for box in result.boxes:
            cls_id = int(box.cls.cpu())
            conf = float(box.conf.cpu().numpy()[0])
            label = f"{class_dict.get(cls_id, 'Unknown')} {conf:.2f}"
            x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show annotated frame
    cv2.imshow("Fruit's condition Detection", annotated_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
