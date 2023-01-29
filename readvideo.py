import cv2
import json
from os import path

f = open("word_to_video_id.json")
word_to_video_name_dict = json.load(f)

def word_to_video(word):
    video_id = word_to_video_name_dict[word][0]
    filepath = 'data/' + word + '/' + video_id + '.mp4'
    cop = cv2.VideoCapture(filepath)

    if not cop.isOpened():
        print("Error opening video file")
        exit()

    # read frames from the video
    while True:
        ret, frame = cop.read()

        # check if we have reached the end of the video
        if not ret:
            break

        # do something with the frame, such as displaying it
        cv2.imshow("Video", frame)

        # wait for a key press
        key = cv2.waitKey(25)

        # exit if the user presses 'q'
        if key == ord('q'):
            break

    # release the VideoCapture object
    cop.release()

    # close all windows
    #cv2.destroyAllWindows()


word_to_video('hello')