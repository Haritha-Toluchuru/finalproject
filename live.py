# import cv2
# from ultralytics import YOLO
# import numpy as np

# # Load YOLOv9 model
# model1 = YOLO('fruits_and_vegetable.pt')


# # Class ID to Label mapping
# class_map = {
#     0: "Bitter melon - 17 kcal",
#     1: "Brinjal - 25 kcal",
#     2: "Cabbage - 25 kcal",
#     3: "Calabash - 14 kcal",
#     4: "Capsicum - 20 kcal",
#     5: "Cauliflower - 25 kcal",
#     6: "Cherry - 50 kcal",
#     7: "Garlic - 149 kcal",
#     8: "Ginger - 80 kcal",
#     9: "Green Chili - 40 kcal",
#     10: "Kiwi - 61 kcal",
#     11: "Lady finger (Okra) - 33 kcal",
#     12: "Onion - 40 kcal",
#     13: "Potato - 77 kcal",
#     14: "Sponge Gourd - 20 kcal",
#     15: "Tomato - 18 kcal",
#     16: "Apple - 52 kcal",
#     17: "Avocado - 160 kcal",
#     18: "Banana - 89 kcal",
#     19: "Cucumber - 16 kcal",
#     20: "Dragon Fruit - 60 kcal",
#     21: "Egg - 155 kcal",
#     22: "Guava - 68 kcal",
#     23: "Mango - 60 kcal",
#     24: "Orange - 43 kcal",
#     25: "Oren - 43 kcal",
#     26: "Peach - 39 kcal",
#     27: "Pear - 57 kcal",
#     28: "Pineapple - 50 kcal",
#     29: "Strawberry - 32 kcal",
#     30: "Sugar Apple - 94 kcal",
#     31: "Watermelon - 30 kcal"
# }


# # Open webcam
# cap = cv2.VideoCapture(0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     # Convert frame to RGB
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#     # Run prediction
#     results = model1.predict(source=rgb_frame, conf=0.3, save=False, verbose=False)
#     result = results[0]
#     annotated_frame = result.plot()

#     # Draw class labels with confidence
#     if result.boxes is not None and len(result.boxes) > 0:
#         for box in result.boxes:
#             cls_id = int(box.cls.cpu())
#             conf = float(box.conf.cpu().numpy()[0])
#             label = f"{class_map.get(cls_id, 'Unknown')} {conf:.2f}"
#             x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
#             cv2.putText(annotated_frame, label, (x1, y1 - 10),
#                         cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

#     # Show annotated frame
#     cv2.imshow("Fruits and vegetable Detection", annotated_frame)

#     # Exit on 'q' key
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


import cv2
from ultralytics import YOLO
import numpy as np

# Load YOLOv9 model
model1 = YOLO('fruits_and_vegetable.pt')

# Class ID to Label mapping
class_map = {
    0: "Bitter melon - 17 kcal",
    1: "Brinjal - 25 kcal",
    2: "Cabbage - 25 kcal",
    3: "Calabash - 14 kcal",
    4: "Capsicum - 20 kcal",
    5: "Cauliflower - 25 kcal",
    6: "Cherry - 50 kcal",
    7: "Garlic - 149 kcal",
    8: "Ginger - 80 kcal",
    9: "Green Chili - 40 kcal",
    10: "Kiwi - 61 kcal",
    11: "Lady finger (Okra) - 33 kcal",
    12: "Onion - 40 kcal",
    13: "Potato - 77 kcal",
    14: "Sponge Gourd - 20 kcal",
    15: "Tomato - 18 kcal",
    16: "Apple - 52 kcal",
    17: "Avocado - 160 kcal",
    18: "Banana - 89 kcal",
    19: "Cucumber - 16 kcal",
    20: "Dragon Fruit - 60 kcal",
    21: "Egg - 155 kcal",
    22: "Guava - 68 kcal",
    23: "Mango - 60 kcal",
    24: "Orange - 43 kcal",
    25: "Oren - 43 kcal",
    26: "Peach - 39 kcal",
    27: "Pear - 57 kcal",
    28: "Pineapple - 50 kcal",
    29: "Strawberry - 32 kcal",
    30: "Sugar Apple - 94 kcal",
    31: "Watermelon - 30 kcal"
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
    results = model1.predict(source=input_frame, conf=0.3, save=False, verbose=False)
    result = results[0]
    annotated_frame = result.plot()

    # Draw class labels with confidence
    if result.boxes is not None and len(result.boxes) > 0:
        for box in result.boxes:
            cls_id = int(box.cls.cpu())
            conf = float(box.conf.cpu().numpy()[0])
            label = f"{class_map.get(cls_id, 'Unknown')} {conf:.2f}"
            x1, y1, x2, y2 = map(int, box.xyxy.cpu().numpy()[0])
            cv2.putText(annotated_frame, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

    # Show annotated frame
    cv2.imshow("Fruits and Vegetable Detection", annotated_frame)

    # Exit on 'q' key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
