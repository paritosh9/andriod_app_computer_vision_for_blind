import cv2
import numpy as np
import time
from gtts import gTTS
import os
from pathlib import Path

URL = "http://10.0.0.59:8080"

def main():
    cap = cv2.VideoCapture(URL)
    time.sleep (10)

    # REMOVE BELOW 2 LINES , JUST EXPERIMENT
    #cap.release()
    #cv2.destroyAllWindows()

    label_all_prev = ''
    myText = "Please give me few seconds to get started"

    # language is english
    language = 'en'

    # gTTS is Google text to speech library, speech in english
    output = gTTS(text=myText, lang=language, slow=False)
    # output saved in mp3 file
    output.save("objects_detected_audio.mp3")

    # audio file opened and sent to speaker to be read out loud
    os.system("start objects_detected_audio.mp3")

    # Load Yolo
    folder_weights = Path("pre_trained_weights")
    print("folder = ", folder_weights)
    file_to_open_weights = folder_weights/"yolov3.weights"
    folder_cfg = Path("cfg")
    file_to_open_cfg = folder_cfg/"yolov3.cfg"

    net = cv2.dnn.readNet(file_to_open_weights, file_to_open_cfg)
    classes = []
    with open("coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    colors = np.random.uniform(0, 255, size=(len(classes), 3))

    # Loading image
    #cap = cv2.VideoCapture(0)
    #cap = cv2.VideoCapture(URL)

    font = cv2.FONT_HERSHEY_PLAIN
    starting_time = time.time()
    frame_id = 0
    while True:
        _, frame = cap.read()
        frame_id += 1

        height, width, channels = frame.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.2:
                    # Object detected
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.8, 0.3)

        label_all = ''
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                # save out to file
                label_all = label_all + ' ' + label
                confidence = confidences[i]
                color = colors[class_ids[i]]
                cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
                cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 3, color, 3)


        if label_all != label_all_prev :
            if label_all == '':
                label_all = ' nothing significant '
            myText = "I see " + label_all + " in front of us "
            # gTTS is Google text to speech library, speech in english
            output = gTTS(text=myText, lang=language, slow=False)

            # output saved in mp3 file
            output.save("objects_detected_audio.mp3")

            # audio file opened and sent to speaker to be read out loud
            os.system("start objects_detected_audio.mp3")

        label_all_prev = label_all

        elapsed_time = time.time() - starting_time
        fps = frame_id / elapsed_time
        cv2.putText(frame, "FPS: " + str(round(fps, 2)), (10, 50), font, 4, (0, 0, 0), 3)
        cv2.imshow("Image", frame)
        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()