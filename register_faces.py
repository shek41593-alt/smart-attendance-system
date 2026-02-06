import cv2
import os

student_id = input("Enter Student ID: ").strip()
dataset_path = f"data/dataset/{student_id}"
os.makedirs(dataset_path, exist_ok=True)

cam = cv2.VideoCapture(0)
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

count = 0
print("Look at the camera. Press 'q' to exit.")

while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        count += 1
        face = gray[y:y+h, x:x+w]
        cv2.imwrite(f"{dataset_path}/{count}.jpg", face)
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)

    cv2.imshow("Register Face", img)

    if cv2.waitKey(1) & 0xFF == ord('q') or count >= 20:
        break

cam.release()
cv2.destroyAllWindows()
print(f"Collected {count} images for student {student_id}")
