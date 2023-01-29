
import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
import cv2
import json
from os import path
import numpy as np

f = open("word_to_video_id.json")
word_to_video_name_dict = json.load(f)

g = open("reference.json")
reference_dict = json.load(g)

def word_to_video(word):
    video_id = word_to_video_name_dict[word][0]
    filepath = 'data/' + word + '/' + video_id + '.mp4'
    cop = cv2.VideoCapture(filepath)
    video = Tk()
    
    video.title("video")


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
        cv2.imshow("video", frame)

        # wait for a key press
        key = cv2.waitKey(25)

        # exit if the user presses 'q'
        if key == ord('q'):
            break

    # release the VideoCapture object
    cop.release()

    # close all windows
    cv2.destroyAllWindows()


#word_to_video('hello')

# Create an instance of TKinter Window or frame
win = Tk()


# Set the size of the window
win.geometry("1200x1500")
win.title("SignLingo")
win.i = 0
win.wordIndex = 0
win.incorrectTimer = 50

#set of premade learning prompts
sentences = ["abdomen", "i love you","last night it was cold outside","I finished my homework", "My uncle is divorced"]
words = ["abdomen", "i love you","past night cold out ","I finish my home work","my uncle divorce"]




win.usersign = " "
cap= cv2.VideoCapture(0)

# Create a Label to capture the Video frames
label =Label(win)
label.grid(row=1, column=1)






# Define function to show frame
def show_frames():
    #print(win.incorrectTimer)


    win.incorrectTimer -=1
    if win.incorrectTimer == 0:
        showVideo(words[win.i].split(" ")[win.wordIndex])


    if win.usersign.split() == words[win.i].split():
        print("success")
        
        win.i = (win.i+1)% len(sentences)
        win.wordIndex = 0
        win.usersign = ""
        win.incorrectTimer = 50
        global sentence
        global signs
        global detected
        sentence.grid_forget()
        signs.grid_forget()
        detected.grid_forget()
    sentence = tk.Label(win,text="Prompt:"+sentences[win.i], font="Verdana 25 ")
    sentence.grid(row=3, column=0)

    
    signs = tk.Label(win ,text="Signs:"+words[win.i],font="Verdana 25")
    signs.grid(row=3, column=2)
    
    detected = Label(win, text = "Detected ASL: " +win.usersign,font="Verdana 25 ")
    detected.grid(row=5, column=1)

    with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
        if cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                #continue

            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            #image = cv2.flip(cv2.cvtColor(image, cv2.COLOR_BGR2BGR),1)
            image = cv2.flip(image,1)
            results = hands.process(image)
            #print('Handedness:', results.multi_handedness)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            vectors = []
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    
                    for i in range(21):
                        vectors.append(hand_landmarks.landmark[i].x)
                        vectors.append(hand_landmarks.landmark[i].y)
                        vectors.append(hand_landmarks.landmark[i].z)
                    mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                #print(results.multi_hand_landmarks)
                
            # Flip the image horizontally for a selfie-view display.
            #cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            
            if cv2.waitKey(5) & 0xFF == 27:
                print("poop")
                
   # Get the latest frame and convert into Image
    #cv2image= cv2.cvtColor(cap.read()[1],cv2.COLOR_BGR2RGB)
    img = Image.fromarray(image)
    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(img.resize((640,360)))
    label.imgtk = imgtk
    label.configure(image=imgtk)
    # Repeat after an interval to capture continiously
    
    getModel(vectors,words[win.i].split()[win.wordIndex])
    label.after(10, show_frames)
      
  
def getModel(vectors,word):
    # print(vectors)
    # print(word)

    if len(vectors) != len(reference_dict[word]):
        difference = 100
    else:
        difference =np.sum(np.absolute(np.array(reference_dict[word])-np.array(vectors)))
    print(difference)
    
    
    if (difference<5 and len(reference_dict[word]) < 100) or (difference<10 and len(reference_dict[word]) > 100):
        win.wordIndex+=1
        #win.i +=1
        poop = win.usersign.split()
        poop.append(word)
        win.usersign=" ".join(poop)
    # else:
    #     incorrect = tk.Label(win,text="incorrect sign detected: ", font="Verdana 25 ", fg="red")
    #     incorrect.grid(row=6, column=1)

        
def showVideo(word):
    print(word)
    word_to_video(word)
    
    
    
    
results = show_frames()
print(results)




win.mainloop()
cap.release()