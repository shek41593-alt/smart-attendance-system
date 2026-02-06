import cv2
import numpy as np
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

faces = []
labels = []

dataset_path = "data/dataset"

print("[INFO] Reading dataset...")

if not os.path.exists(dataset_path):
    print("[ERROR] Dataset folder not found!")
    exit()

for student_id in os.listdir(dataset_path):
    student_path = os.path.join(dataset_path, student_id)

    if not os.path.isdir(student_path):
        continue

    print(f"[INFO] Processing student ID: {student_id}")

    for img_name in os.listdir(student_path):
        img_path = os.path.join(student_path, img_name)
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if img is None:
            print(f"[WARN] Could not read image: {img_path}")
            continue

        faces_detected = detector.detectMultiScale(img)

        if len(faces_detected) == 0:
            print(f"[WARN] No face detected in {img_path}")
            continue

        for (x, y, w, h) in faces_detected:
            faces.append(img[y:y+h, x:x+w])
            labels.append(int(student_id))

print(f"[INFO] Total faces collected: {len(faces)}")

if len(faces) == 0:
    print("[ERROR] No faces found. Training aborted.")
    exit()

recognizer.train(faces, np.array(labels))

os.makedirs("data", exist_ok=True)
recognizer.save("data/trainer.yml")

print("Training completed. Model saved as trainer.yml")
