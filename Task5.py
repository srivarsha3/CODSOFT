import cv2
import numpy as np
import os

# ---------- Load Haar Cascade for Face Detection ----------
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# ---------- Load Training Images and Create Database ----------
def load_training_faces(directory):
    database = {}
    for filename in os.listdir(directory):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            label = filename.split('.')[0]
            image_path = os.path.join(directory, filename)
            img = cv2.imread(image_path)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                face_img = gray[y:y+h, x:x+w]
                face_img = cv2.resize(face_img, (100, 100))  # normalize size
                database[label] = face_img
    return database

# ---------- Compare Faces Using Mean Squared Error ----------
def compare_faces(face1, face2):
    face1 = cv2.resize(face1, (100, 100))
    face2 = cv2.resize(face2, (100, 100))
    error = np.mean((face1 - face2) ** 2)
    return error

# ---------- Recognize Face ----------
def recognize_face(face_img, database, threshold=2000):
    min_error = float('inf')
    recognized_label = "Unknown"
    for label, db_face in database.items():
        error = compare_faces(face_img, db_face)
        if error < min_error:
            min_error = error
            recognized_label = label
    return recognized_label if min_error < threshold else "Unknown"

# ---------- Real-time Recognition ----------
def run_recognition():
    database = load_training_faces("faces/")  # folder with labeled images
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = gray[y:y+h, x:x+w]
            label = recognize_face(face_img, database)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)

        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

