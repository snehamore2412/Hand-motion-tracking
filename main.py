import cv2
import mediapipe as mp
import webbrowser
# Initialize MediaPipe Hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Setup webcam
cap = cv2.VideoCapture(0)


def detect_character(landmarks):
    thumb_is_open = False
    index_is_open = False
    middle_is_open = False
    ring_is_open = False
    pinky_is_open = False
    
    if landmarks[mp_hands.HandLandmark.THUMB_TIP].y < landmarks[mp_hands.HandLandmark.THUMB_MCP].y:
        thumb_is_open = True

  
    if landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.INDEX_FINGER_PIP].y:
        index_is_open = True

    if landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y:
        middle_is_open = True

   
    if landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y < landmarks[mp_hands.HandLandmark.RING_FINGER_PIP].y:
        ring_is_open = True

    if landmarks[mp_hands.HandLandmark.PINKY_TIP].y < landmarks[mp_hands.HandLandmark.PINKY_PIP].y:
        pinky_is_open = True

    # Character mapping
    if thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
        webbrowser.open("youtube.com")
        return 'L'
        
    elif not thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
        webbrowser.open("google.com")
        return 'I'  # One index finger extended, representing "I"

    elif not thumb_is_open and index_is_open and middle_is_open and not ring_is_open and not pinky_is_open:
        webbrowser.open("Linkedin.com")
        return 'V'  # Index and middle finger extended
        
    elif thumb_is_open and not index_is_open and not middle_is_open and not ring_is_open and not pinky_is_open:
        webbrowser.open("gmail.com")
        return 'E'  # Thumb open, other fingers closed
  
    elif thumb_is_open and index_is_open and middle_is_open and ring_is_open and pinky_is_open:
        webbrowser.open("irctc.com")
        return '5'  # All fingers open (use for "5")
    
    elif thumb_is_open and index_is_open and not middle_is_open and not ring_is_open and pinky_is_open:
         webbrowser.open("facebook.com")
         return 'Y'  # Thumb, index, and pinky extended, representing "Y"
   
    else:
        return 'Unknown'

# Process video stream
with mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        # Convert image to RGB and process with MediaPipe
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = hands.process(image)
        
        # Convert back to BGR for OpenCV
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Detect character based on hand landmarks
                character = detect_character(hand_landmarks.landmark)

                # Display detected character
                cv2.putText(image, f'Character: {character}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Display the image
        cv2.imshow('Hand Gesture Character Detection', image)

        # Exit on pressing 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()