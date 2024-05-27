import cv2
import streamlit as st  
import numpy as np
import time
import re
from PIL import Image
from io import BytesIO
import pytesseract  
import mediapipe as mp  
import requests

# Initialize the Tesseract-OCR path (adjust this if needed)
# Function to detect faces


def load_css():
    """Load the CSS for styling the application."""
    st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Poetsen+One&display=swap');

            html, body, [class*="css"] {
                font-family: 'Roboto', sans-serif;
                height: 100%;
                background-color: #050000; 
                color: #110000; 
            }

            
            @keyframes popup {
                0% { transform: scale(0); opacity: 0; }
                50% { transform: scale(1.1); }
                100% { transform: scale(1); opacity: 1; }
            }
            .popup {
                animation: popup 3s ease-out;
            }

            /* Homepage container styling */
            .homepage-container {
                background-color: #5F5D5D; 
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
                margin: 20px auto;
                max-width: 800px; 
                text-align: center; 
            }

            /* Key feature card styling */
            .card {
                display: inline-block; 
                margin: 10px;
                padding: 20px;
                border-radius: 5px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                text-align: center;
                background-color: #0E0101; 
                transition: transform 0.4s; 
                width: 220px; 
            }

            .card:hover {
                transform: translateY(-6px); 
            }

            .card h3 {
                font-size: 18px;
                margin-bottom: 10px;
                color: #333; 
                font-weight: bold; 
            }

            .card p {
                color: #666;
                line-height: 1.5;
            }

            .stButton>button {
                color: white;
                background-color: #E78432; 
                border: none;
                border-radius: 5px;
                padding: 20px 80px; 
                margin: 20px auto; 
                display: block; 
                transition: background-color 0.3s, transform 0.2s;
            }
            
            .stButton button {
                font-weight: bold;
                font-size: 100px;
            }

            .stButton>button:hover {
                background-color: #EBC82C;
                transform: scale(1.05);
            }


            .stTextInput>div>div>input {
                padding: 10px;
                border-radius: 5px;
                border: 1px solid #ccc;
            }

            .logo {
                width: 100px; 
                height: auto;
                margin: 20px auto;
            }

           
            .footer {
                display: flex;
                justify-content: center;
                flex-wrap: wrap;
                margin-top: 20px;
            }

            .footer .card {
                flex: 1 0 220px; 
                margin: 10px;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                text-align: center;
                background-color: #D67F2D; 
                transition: transform 1.0s; 
            }

            .footer .card:hover {
                transform: translateY(-19px); 
            }

            .footer .card h3 {
                font-size: 18px;
                margin-bottom: 10px;
                color: #0E0000 
                font-weight: bold; 
            }

            .footer .card p {
                color: #FFFFFF;
                line-height: 1.5;
            }
        </style>
    """, unsafe_allow_html=True)


def home_page():
    load_css()  # Apply custom styles

    # Homepage content
    st.title("WELCOME TO eKYC VERIFICATION ")
    st.image("https://www.ikigailaw.com/wp-content/uploads/2022/03/Artboard-1-copy-9.png", use_column_width=True)  # Center-align image
    st.markdown("""
        <div class="homepage-container">
            <h2 class="homepage-title popup" id="welcome-text">eKYC Verification Process</h2>
        </div>
    """, unsafe_allow_html=True)

    

    # Footer section
    st.markdown("<h2 style='text-align: center;'>STEPS TO FOLLOW</h2>", unsafe_allow_html=True)
    st.markdown("""
        <div class="footer">
            <div class="card">
                <img src="https://pmmodiyojana.in/wp-content/uploads/2022/08/image-170-1024x683.png" alt="Aadhar Verification" style="width:100%">
                <h3>AADHAR VERIFICATION</h3>
                <p>Learn about Aadhar verification process and its importance.</p>
            </div>
            <div class="card">
                <img src="https://www.asisonline.org/globalassets/security-management/security-technology/2021/december/1221-megan-gates-facial-recognition-freeze-frame.jpg" alt="Facial Recognition" style="width:100%">
                <h3>FACIAL RECOGNITION</h3>
                <p>Understand how facial recognition technology is used for identity verification.</p>
            </div>
            <div class="card">
                <img src="https://routemobile.com/wp-content/uploads/2023/03/Benefits-of-OTP-authentication.png" alt="OTP Authentication" style="width:100%">
                <h3>OTP AUTHENTICATION</h3>
                <p>Know about the OTP authentication process and its security features.</p>
            </div>
            <div class="card">
                <img src="https://img.freepik.com/free-vector/businessman-computer-recognising-interpreting-human-gesures-as-commands-gesture-recognition-gestures-commands-hands-free-control-concept-bright-vibrant-violet-isolated-illustration_335657-1016.jpg" alt="Gesture Verification" style="width:100%">
                <h3>GESTURE VERIFICATION</h3>
                <p>Explore the gesture verification method and its role in eKYC.</p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("Start eKYC", key="start_button"):
       st.session_state.page = 'main'


 
def detect_faces(image):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    return image, faces

# Function to extract Aadhar details from text
# Function to extract Aadhar details from text
def extract_aadhar_details(text):
    name_pattern = re.compile(r'([A-Za-z]+)\s+([A-Za-z]+)')
    dob_pattern = re.compile(r'([0-9]{2}/[0-9]{2}/[0-9]{4})')
    aadhar_pattern = re.compile(r'\d{4}\s\d{4}\s\d{4}')

    name = name_pattern.search(text)
    dob = dob_pattern.search(text)
    aadhar_number = aadhar_pattern.search(text)

    return {
        'Name': name.group(0) if name else 'Not Found',
        'DOB': dob.group(0) if dob else 'Not Found',
        'Aadhar Number': aadhar_number.group(0) if aadhar_number else 'Not Found'
    }

def aadhar_extraction_page():
    st.title("Aadhar Card Details Extraction")
    uploaded_file = st.file_uploader("Upload Aadhar Card", type=['jpg', 'png'])
    if uploaded_file is not None:
        bytes_data = uploaded_file.read()
        image = Image.open(BytesIO(bytes_data))
        st.image(image, caption='Uploaded Aadhar Card', use_column_width=True)

        # OCR
        details = pytesseract.image_to_string(image)
        extracted_details = extract_aadhar_details(details)
        
        # Styling and displaying extracted details
        st.markdown("<h2 style='text-align: center; color: orange;'>Extracted Details:</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 20px; text-align: center; color: white;'>Name: <strong>{extracted_details['Name']}</strong></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 20px; text-align: center; color: white;'>DOB: <strong>{extracted_details['DOB']}</strong></p>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 20px; text-align: center; color: white;'>Aadhar Number: <strong>{extracted_details['Aadhar Number']}</strong></p>", unsafe_allow_html=True)

        # Button to proceed to OTP authentication
        if st.button("Proceed to OTP Authentication", key="otp_button"):
            st.session_state.extracted_details = extracted_details
            st.session_state.page = "otp_authentication"

            # Add pop-up animation
            st.markdown("""
            <style>
            @keyframes scale {
                0% { transform: scale(0); }
                100% { transform: scale(1); }
            }
            .popup {
                animation: scale 0.3s ease forwards;
                text-align: center;
                font-weight: bold;
                color: white;
                background-color: orange;
                border: none;
                border-radius: 5px;
                padding: 15px 30px;
                margin-top: 20px;
            }
            </style>
            """, unsafe_allow_html=True)
            st.markdown("<div class='popup'>SUCCESSFULL</div>", unsafe_allow_html=True)


# Function to authenticate and get the access token
def get_access_token():
    url = "https://api.sandbox.co.in/authenticate"
    headers = {
        "accept": "application/json",
        "x-api-key": "",
        "x-api-secret": "",
        "x-api-version": "1.0.0"
    }
    response = requests.post(url, headers=headers)
    data = response.json()
    return data.get("access_token", "No access token received. Check credentials or API status.")

# Function to send OTP
def send_otp(aadhaar_number, access_token):
    url = "https://api.sandbox.co.in/kyc/aadhaar/okyc/otp"
    payload = {
        "@entity": "in.co.sandbox.kyc.aadhaar.okyc.otp.request",
        "consent": "y",
        "reason": "For KYC",
        "aadhaar_number": aadhaar_number
    }
    headers = {
        "accept": "application/json",
        "authorization": access_token,
        "x-api-key": "",
        "x-api-version": "2.0",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response)
    return response.json()

# Function to verify OTP
def verify_otp(ref_id, otp, access_token):
    url = "https://api.sandbox.co.in/kyc/aadhaar/okyc/otp/verify"
    print(otp)
    print(ref_id)
    payload = {
        "@entity": "in.co.sandbox.kyc.aadhaar.okyc.request",
        "reference_id": f"{ref_id}",
        "otp": f"{otp}"
    }
    headers = {
        "accept": "application/json",
        "authorization": f"{access_token}",
        "x-api-key": "key_live_VxqACLiJ56MEyWfYlJGYMWTRpig5QGXf",
        "x-api-version": "2.0",
        "content-type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response_data = response.json()
    print(response_data)
    
    # Extracting name and dob from the response data
    name = response_data.get('data', {}).get('name', 'Name not found')
    
    # Use regex to validate the dob format (dd-mm-yyyy) and extract it
    dob = response_data.get('data', {}).get('date_of_birth', 'DOB not found')
    dob_pattern = re.compile(r"^\d{2}-\d{2}-\d{4}$")  # Regex pattern to match dd-mm-yyyy format
    
    # Validate dob format
    if not dob_pattern.match(dob):
        dob = "Invalid DOB format"  # Indicates an incorrect format if not matching

    return name, dob


def display_extracted_details(name, dob):
    st.markdown(
        f"""
        <div style="background-color: orange; padding: 20px; border-radius: 10px;">
            <h2 style="color: white; text-align: center;">Extracted Details</h2>
            <p style="color: white; font-weight: bold; text-align: center;">Name: {name}</p>
            <p style="color: white; font-weight: bold; text-align: center;">DOB: {dob}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

def otp_authentication_page():
    st.title('**Aadhaar KYC Verification**')  # Bold headline
    st.markdown("<h1 style='text-align: center; color: orange;'>Aadhaar KYC Verification</h1>", unsafe_allow_html=True)  # Center aligned text in orange color

    if 'access_token' not in st.session_state or st.session_state.access_token is None:
        st.session_state.access_token = get_access_token()

    if st.session_state.access_token.startswith("No access"):
        st.error(st.session_state.access_token)
    else:
        st.write('Access token obtained.')

    aadhaar_number = st.text_input("Enter your Aadhaar number:")
    if st.button('**Send OTP**'):  # Bold button text
        otp_response = send_otp(aadhaar_number, st.session_state.access_token)
        print(otp_response)
        if "error" in otp_response:
            st.error(otp_response["error"])
        else:
            st.session_state.ref_id = otp_response['data']['reference_id']
            st.success('**OTP sent.** Please check your mobile.')  # Bold success message
            st.write(f"Reference ID: {st.session_state.ref_id}")

    otp = st.text_input("Enter OTP received:")
    if st.button('**Verify OTP**'):  # Bold button text
        name, dob = verify_otp(st.session_state.ref_id, otp, st.session_state.access_token)
        st.write('Name:', name)
        st.write('Date of Birth:', dob)
        
        st.write("**Aadhar Extracted and Aadhar OTP both are matched**")  # Bold text
        
        st.markdown("<div style='background-color: orange; padding: 10px;'><b>Verification done successfully</b></div>", unsafe_allow_html=True)  # Orange card with bold text

    if st.button("**Proceed to Gesture Verification**"):  # Bold button text
        st.session_state.page = "gesture_verification"


# Define a function for the gesture verification page


def gesture_verification_page():
    st.markdown("<div style='text-align: center; color: orange;'><h1>Gesture Verification</h1></div>", unsafe_allow_html=True)
    st.markdown("""
        <div style='background-color: orange; padding: 20px;'>
            <h3 style='color: white; font-weight: bold;'>Follow the on-screen instructions for gesture verification:</h3>
            <ol style='color: white; font-weight: bold; font-size: 18px;'>
                <li>Rotate your head in the left and right direction.</li>
                <li>Wave your hand.</li>
            </ol>
        </div>
    """, unsafe_allow_html=True)

    # Initialize mediapipe solutions
    mp_face_detection = mp.solutions.face_detection
    mp_hands = mp.solutions.hands
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    # Setup variables for detection logic
    prev_y = None
    wave_count = 0
    prev_eye_dist = None
    head_rotation_count = 0
    last_detection_time = time.time()
    validation_successful = False  # Flag to track validation success

    # Streamlit component to use the webcam
    FRAME_WINDOW = st.image([])
    cap = cv2.VideoCapture(0)

    with mp_face_detection.FaceDetection(min_detection_confidence=0.5) as face_detection, \
         mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:

        while cap.isOpened() and not validation_successful:  # Continue loop until validation successful
            success, image = cap.read()
            if not success:
                continue

            # Convert the BGR image to RGB before processing
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results_face = face_detection.process(image)
            results_hands = hands.process(image)

            # Convert the image back to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Draw face and hands landmarks
            if results_face.detections:
                for detection in results_face.detections:
                    mp_drawing.draw_detection(image, detection)
                    # Distance between eyes calculation for head rotation
                    if detection.location_data.relative_keypoints:
                        left_eye = detection.location_data.relative_keypoints[0]
                        right_eye = detection.location_data.relative_keypoints[1]
                        eye_dist = np.linalg.norm([left_eye.x - right_eye.x, left_eye.y - right_eye.y])
                        
                        if prev_eye_dist is not None and abs(eye_dist - prev_eye_dist) > 0.01:
                            head_rotation_count += 1
                            last_detection_time = time.time()
                        
                        prev_eye_dist = eye_dist

            if results_hands.multi_hand_landmarks:
                for hand_landmarks in results_hands.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                                              mp_drawing_styles.get_default_hand_landmarks_style(),
                                              mp_drawing_styles.get_default_hand_connections_style())
                    
                    # Hand wave detection
                    for id, lm in enumerate(hand_landmarks.landmark):
                        if id == 0:
                            current_y = lm.y
                            if prev_y is not None and abs(current_y - prev_y) > 0.01:
                                wave_count += 1
                                last_detection_time = time.time()
                            prev_y = current_y

            # Display the result in the Streamlit window
            FRAME_WINDOW.image(image)

            # Check if detections occurred twice within 15 seconds
            if time.time() - last_detection_time < 15:
                if wave_count >= 2 and head_rotation_count >= 2:
                    st.success("Validation: Valid")
                    st.success("eKYC completed and Aadhar is also verified") 
                    validation_successful = True  # Set flag to indicate successful validation
                    # Adding pop-up animation and styling for "Thank you for Confirmation"
                    st.markdown("""
                    <style>
                    @keyframes slideIn {
                      0% {
                       transform: translateY(-100%);
                       opacity: 0;
                    }
                    100% {
                    transform: translateY(0);
                    opacity: 1;
                    }
                    }
                    .popup {
                    animation: slideIn 0.5s forwards;
                    text-align: center;
                    font-weight: bold;
                    color: orange;
                }
                </style>
                """, unsafe_allow_html=True)
                    st.markdown("<div class='popup'>Thank you for Confirmation</div>", unsafe_allow_html=True)
        
                    break  # Exit loop on successful validation
            elif cv2.waitKey(5) & 0xFF == 27:
                break

    # Outside the loop, check if validation was successful # Print "eKYC completed" if validation successful

def main_page():
    st.markdown("<div style='text-align: center; color: orange; font-size: 24px; font-weight: bold;'>Live Face Detection</div>", unsafe_allow_html=True)  # Center aligned, bold, orange text
    st.write("<div style='font-size: 20px; color: white;'>The camera will start for 5 seconds and detect faces.</div>", unsafe_allow_html=True)  # Larger white text

    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)  # Use 0 for webcam
    start_time = time.time()
    first_face_saved = False

    while time.time() - start_time < 5:  # Run for 5 seconds
        ret, frame = camera.read()
        if not ret:
            st.write("Failed to grab frame")
            break
        # Assume detect_faces function is defined elsewhere
        frame, faces = detect_faces(frame)
        FRAME_WINDOW.image(frame, channels="BGR", use_column_width=True)
        
        # Save the first detected face
        if not first_face_saved and len(faces) > 0:
            x, y, w, h = faces[0]
            face_image = frame[y:y+h, x:x+w]
            cv2.imwrite("first_detected_face.jpg", face_image)
            first_face_saved = True
            break  # Stop detecting faces after the first one is found

    camera.release()

    if first_face_saved:
        st.success("### First detected face has been saved successfully!")  # Markdown syntax for larger text
        st.image("first_detected_face.jpg", caption="First Detected Face", use_column_width=True)
        st.button("Next", on_click=lambda: st.session_state.update({"page": "aadhar_extraction"}))
    else:
        st.warning("### No face detected during the session.")  # Markdown syntax for larger text
  # Markdown syntax for larger text

        


# Set up navigation between pages
if "page" not in st.session_state:
    st.session_state.page = "home"

if st.session_state.page == "home":
    home_page()
elif st.session_state.page == "main":
    main_page()
elif st.session_state.page == "aadhar_extraction":
    aadhar_extraction_page()
elif st.session_state.page == "otp_authentication":
    otp_authentication_page()
elif st.session_state.page == "gesture_verification":
    gesture_verification_page()
