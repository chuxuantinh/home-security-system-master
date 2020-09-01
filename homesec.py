import face_recognition
import cv2
import scipy
import time
import http.client,urllib
print("Importing libraries done!")

PUSH_TOKEN = "anyueood7nhqfrbhymg8e1abdnq3o8"
PUSH_USER = "ukjfv6ef91fxuxoa4ngf166n7ihk55"
flag=0

# Get a reference to webcam #0 (the default one)
print("Trying to get reference to webcam..."),
print("Webcam acquired")

video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.

print("Loading known images..."),
himalay_image = face_recognition.load_image_file("himalay.jpg")
himalay_face_encoding = face_recognition.face_encodings(himalay_image)[0]

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

elon_image = face_recognition.load_image_file("elon.jpg")
elon_face_encoding = face_recognition.face_encodings(elon_image)[0]

bachchan_image = face_recognition.load_image_file("bachchan.jpg")
bachchan_face_encoding = face_recognition.face_encodings(bachchan_image)[0]
print("Done!")

# Create arrays of known face encodings and their names
known_face_encodings = [
    himalay_face_encoding,	
    obama_face_encoding,
    elon_face_encoding,
    bachchan_face_encoding
]
known_face_names = [
    "Himalay",
    "Barack Obama",
    "Elon Musk",
    "Amitabh Bachchan"
]
print("Starting face recognition...")
# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

def sendPush( msg ):
	conn = http.client.HTTPSConnection("api.pushover.net:443")
	conn.request("POST", "/1/messages.json",
		urllib.parse.urlencode({
			"token": PUSH_TOKEN,
			"user": PUSH_USER,
			"message": msg,
		}), { "Content-type": "application/x-www-form-urlencoded" })

	conn.getresponse()
	return
    
start = time.time()

while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    #small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    small_frame=scipy.misc.imresize(frame,0.25)
    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)
            message = "Person recognized at your house: " + name
            if flag==0:
                sendPush(message)
                flag=1
            elapsed=0
            elapsed = time.time()-start
            if elapsed > 20:
                sendPush(message)
                start = time.time()

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
print("Releasing webcam...")
video_capture.release()
print("Bye!")
cv2.destroyAllWindows()
