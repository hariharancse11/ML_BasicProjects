# Imports
import cv2
import pytesseract
from gtts import gTTS
from playsound import playsound


# Connects pytessaract(wrapper) to the trained tesseract module
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Video feed
# video = cv2.VideoCapture(0)
#
# # Setting width and height for video feed
# video.set(3, 640)
# video.set(4, 480)

# Image feeds
img = cv2.imread('img.png')
#cv2.imshow('Image Window', img)
#cv2.waitKey()

# Obtain height and width of each image
h1Img, w1Img, none1 = img.shape
#print(img.shape)
# Convert images into bounding box values: x, y, w, h
box1 = pytesseract.image_to_boxes(img)
#print(box1)

# Convert images into bound data values: x, y, w, h
data = pytesseract.image_to_data(img)
#print(data1)


def hlEachLetter(img):
    for a in box1.splitlines():
        a = a.split()
        x, y = int(a[1]), int(a[2])
        w, h = int(a[3]), int(a[4])

        cv2.rectangle(img, (x, h1Img-y), (w, h1Img-h), (0,0,255), 2)

        cv2.putText(img, a[0], (x, h1Img - y-25), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

    cv2.imshow('Image Window', img)
    cv2.waitKey()

def hlEachWord(img):
    for z,a in enumerate(data.splitlines()):
        if z != 0:
            a = a.split()
            if len(a) == 12:
                x, y = int(a[6]), int(a[7])
                w, h = int(a[8]), int(a[9])

                cv2.rectangle(img, (x,y), (x+w, y+h), (255,0,0), 2)

                cv2.putText(img, a[11], (x-15, y), cv2.FONT_HERSHEY_PLAIN, 2, (255,0,0), 2)
    cv2.imshow('image Window', img)
    cv2.waitKey()

def videoToText():
    #Video feed
    video = cv2.VideoCapture("https://19.16.1.6:8080/video")

    #setting widht and height of video feed
    video.set(3,640)
    video.set(4,480)

    while True:
        extra, frames = video.read()
        dataVid = pytesseract.image_to_data(frames)

        for z, a in enumerate(dataVid.splitlines()):
            if z != 0:
                a = a.split()
                if(len(a)==12):
                    x,y = int(a[6]), int(a[7])
                    w, h = int(a[8]), int(a[9])

                    cv2.rectangle(frames, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    cv2.putText(frames, a[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
            cv2.imshow('Video Window', frames)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                video.release()
                cv2.destroyAllWindows()
                break

def textToSpeech():
    # Open the file with write permission
    filewrite = open("quotes.txt", "w")
    for z, a in enumerate(data.splitlines()):
        # Counter
        if z != 0:
            # Converts 'data1' string into a list stored in 'a'
            a = a.split()
            # Checking if array contains a word
            if len(a) == 12:
                # Storing values in the right variables
                x, y = int(a[6]), int(a[7])
                w, h = int(a[8]), int(a[9])
                # Display bounding box of each word
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                # Display detected word under each bounding box
                cv2.putText(img, a[11], (x - 15, y), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 1)
                # Writing to the file
                filewrite.write(a[11] + " ")
    filewrite.close()
    # Open the file with read permission
    fileread = open("quotes.txt", "r")
    language = 'en'
    line = fileread.read()
    if line != " ":
        fileread.close()
        speech = gTTS(text=line, lang=language, slow=False)
        speech.save("test.mp3")
    # Output the bounding box with the image
    cv2.imshow('Image output', img)
    cv2.waitKey(0)
    playsound("test.mp3")




while True:
    option = input("Select 1-9:  ")
    print("\n")
    if option == '1':
        hlEachLetter(img)
    if option == '2':
        hlEachWord(img)
    if option == '3':
        videoToText()
    if option == '4':
        textToSpeech()