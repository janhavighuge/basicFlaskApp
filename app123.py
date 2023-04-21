from flask import Flask, render_template, request
import cv2
import time
import collections
from deepface import DeepFace

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_detection', methods=['POST'])
def start_detection():
    global emotion_list, cap
    cap = cv2.VideoCapture(0)
    capture_duration = 10
    start_time = int(time.time())
    emotion_list = []
    while int(time.time()) - start_time < capture_duration:
        try:
            ret, frame = cap.read()
            if not ret:
                raise Exception("Error reading frame")
        except Exception as e:
            print("Error reading frame:", e)
            time.sleep(0.1)
            continue
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        try:
            emotions = DeepFace.analyze(rgb_frame, actions=['emotion'])
        except Exception as e:
            print("Error analyzing frame:", e)
            time.sleep(0.1)
            continue
        dominant_emotion = emotions[0]['dominant_emotion']
        emotion_list.append(dominant_emotion)
        cv2.imshow('frame', frame)
        cv2.waitKey(1)
        time.sleep(0.1)
    cap.release()
    cv2.destroyAllWindows()
    if emotion_list:
        counter = collections.Counter(emotion_list)
        dominant_emotion = counter.most_common(1)[0][0]
        return dominant_emotion
    else:
        return "No emotions detected in the video"

@app.route('/stop_detection', methods=['POST'])
def stop_detection():
    global cap
    cap.release()
    cv2.destroyAllWindows()
    return "Emotion detection stopped"

if __name__ == '__main__':
    app.run(debug=True)
