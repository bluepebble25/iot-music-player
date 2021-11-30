import cv2
import numpy as np   
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import time

# Face detection XML load and trained model loading
face_detection = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
emotion_classifier = load_model('emotion_model.hdf5', compile=False)
EMOTIONS = ["Angry" ,"Disgusting","Fearful", "Happy", "Sad", "Surpring", "Neutral"]
preds = None

# Video capture using webcam
camera = cv2.VideoCapture(0)

while True:
    # Capture image from camera
    ret, frame = camera.read()
    
    # Convert color to gray scale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Face detection in frame
    faces = face_detection.detectMultiScale(gray,
                                            scaleFactor=1.1,
                                            minNeighbors=5,
                                            minSize=(30,30))
    
    # Create empty image
    canvas = np.zeros((250, 300, 3), dtype="uint8")
    
    # Perform emotion recognition only when face is detected
    if len(faces) > 0:
        # For the largest image
        face = sorted(faces, reverse=True, key=lambda x: (x[2] - x[0]) * (x[3] - x[1]))[0]
        (fX, fY, fW, fH) = face
        # Resize the image to 48x48 for neural network
        roi = gray[fY:fY + fH, fX:fX + fW]
        roi = cv2.resize(roi, (48, 48))
        roi = roi.astype("float") / 255.0
        roi = img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        
        # Emotion predict
        preds = emotion_classifier.predict(roi)[0]
        emotion_probability = np.max(preds)
        label = EMOTIONS[preds.argmax()]
        
        # Assign labeling
        cv2.putText(frame, label, (fX, fY - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
        cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
 
        # Label printing
        for (i, (emotion, prob)) in enumerate(zip(EMOTIONS, preds)):    # zip은 두 인자를 튜플쌍의 형태로 반환 (EMOTIONS값 1, preds값 1),(EMOTIONS값 2, preds값 2) 
            text = "{}: {:.2f}%".format(emotion, prob * 100)    # 아마도 비율?
            w = int(prob * 300)
            cv2.rectangle(canvas, (7, (i * 35) + 5), (w, (i * 35) + 35), (0, 0, 255), -1)
            cv2.putText(canvas, text, (10, (i * 35) + 23), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 2)
        
        
    # Open two windows
    ## Display image ("Emotion Recognition")
    ## Display probabilities of emotion
    cv2.imshow('Emotion Recognition', frame)
    cv2.imshow("Probabilities", canvas)

    time.sleep(0.1) # 프레임을 조금 낮춰주기 위함
    
    # q to quit
    k = cv2.waitKey(1) & 0xFF
    if k == ord('q') or k == 27:
        break
    if k == ord('c'): #preds != None 에러, 멈춤 -> 항상 preds의 값은 None이 아님 최소한 하나의 거짓이 있어야함 애매모호 -> 사람이 안보이는 경우는 예측할 값이 없는거잖아 -> 근데  c를 누르는거면 사람이 있는거니까 거기까지는 생각안해도 될 듯 
            percent = max(preds)    # 표정 예측치 중 가장 큰 값
            index = np.where(percent == preds)[0][0]    # 가장 큰 표정 예측치의 index 값 구하기
            print(EMOTIONS[index], percent*100)
            break
    
# Clear program and close windows
camera.release()
cv2.destroyAllWindows()
