import cv2
from collections import deque
from services.timetable import get_current_subject
from services.attendance_db import mark_attendance

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("data/trainer.yml")

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Store last predictions for robustness
recent_ids = deque(maxlen=5)

print("[INFO] Attendance system started")

while True:
    ret, frame = cam.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.2, 5)

    for (x, y, w, h) in faces:
        id_, confidence = recognizer.predict(gray[y:y+h, x:x+w])

        if confidence < 60:
            recent_ids.append(id_)

            # Confirm same ID appears multiple times
            if recent_ids.count(id_) >= 3:
                subject = get_current_subject()
                mark_attendance(str(id_), subject)
                recent_ids.clear()  # avoid repeated insert

            label = f"ID: {id_}"
        else:
            label = "Unknown"

        cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.putText(frame, label, (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

    cv2.imshow("Smart Attendance", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
