
# import cv2
# import face_recognition

# # Initialize lists to hold encodings and names
# known_face_encodings = []
# known_face_names = []

# # Load and encode the known images
# known_person1_image = face_recognition.load_image_file("img1.jpg")
# known_person2_image = face_recognition.load_image_file("Image2.jpg")

# # Check for face encodings in the loaded images
# try:
#     known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
#     known_face_encodings.append(known_person1_encoding)
#     known_face_names.append("Prashanta Acharya")
# except IndexError:
#     print("No face found in Image1.jpg")

# try:
#     known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
#     known_face_encodings.append(known_person2_encoding)
#     known_face_names.append("Srijana Subedi")
# except IndexError:
#     print("No face found in Image2.jpg")

# # Start video capture
# video_capture = cv2.VideoCapture(0)

# while True:
#     ret, frame = video_capture.read()

#     # Find all the faces and face encodings in the current frame of video
#     face_locations = face_recognition.face_locations(frame)
#     face_encodings = face_recognition.face_encodings(frame, face_locations)

#     # Loop through each face in this frame of video
#     for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
#         matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
#         name = "Unknown"

#         # Check if a match was found in known_face_encodings
#         if True in matches:
#             first_match_index = matches.index(True)
#             name = known_face_names[first_match_index]

#         # Draw a box around the face
#         cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
#         # Draw a label with a name below the face
#         cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

#     # Display the resulting image
#     cv2.imshow("Video", frame)

#     # Hit 'q' on the keyboard to quit!
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release handle to the webcam
# video_capture.release()
# cv2.destroyAllWindows()


import cv2
import face_recognition
import requests

# Initialize lists to hold encodings and names
known_face_encodings = []
known_face_names = []

# Load and encode the known images
known_person1_image = face_recognition.load_image_file("img1.jpg")
known_person2_image = face_recognition.load_image_file("Image2.jpg")

# Check for face encodings in the loaded images
try:
    known_person1_encoding = face_recognition.face_encodings(known_person1_image)[0]
    known_face_encodings.append(known_person1_encoding)
    known_face_names.append("Prashanta Acharya")
except IndexError:
    print("No face found in img1.jpg")

try:
    known_person2_encoding = face_recognition.face_encodings(known_person2_image)[0]
    known_face_encodings.append(known_person2_encoding)
    known_face_names.append("Srijana Subedi")
except IndexError:
    print("No face found in Image2.jpg")

# ESP32 IP address
ESP32_IP = "http://192.168.97.169"  # Replace with the actual IP address of your ESP32

def send_signal_to_esp32(signal):
    if signal == "on":
        response = requests.get(f"{ESP32_IP}/on")
    elif signal == "off":
        response = requests.get(f"{ESP32_IP}/off")
    
    if response.status_code == 200:
        print(f"ESP32 responded with: {response.text}")
    else:
        print("Failed to send signal")

# Start video capture
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    found_known_face = False

    # Loop through each face in this frame of video
    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        # Check if a match was found in known_face_encodings
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]
            found_known_face = True

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        # Draw a label with a name below the face
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

    if found_known_face:
        send_signal_to_esp32("on")
    else:
        send_signal_to_esp32("off")

    # Display the resulting image
    cv2.imshow("Video", frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()



