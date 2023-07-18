import cv2
import pytesseract
from PIL import Image
from io import BytesIO
import subprocess

def capture_number_from_camera():
    # Open the camera
    cap = cv2.VideoCapture(0)

    while True:
        # Capture a frame from the camera
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Wait for 'q' key to stop the camera feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close the OpenCV window
    cap.release()
    cv2.destroyAllWindows()

    # Save the captured frame as an image
    image_path = 'captured_frame.jpg'
    cv2.imwrite(image_path, frame)

    return image_path

def recognize_number_from_image(image_path):
    # Read the image using PIL
    image = Image.open(image_path)

    # Perform OCR using Tesseract
    number = pytesseract.image_to_string(image, config='--psm 6')

    # Filter out non-numeric characters
    number = ''.join(filter(str.isdigit, number))

    return number

def make_call_with_number(number):
    # Use termux-api to make a call
    command = f'termux-telephony-call {number}'
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    try:
        # Capture a number from the camera
        print("Please show the number to the camera...")
        image_path = capture_number_from_camera()

        # Recognize the number from the captured image
        recognized_number = recognize_number_from_image(image_path)

        if recognized_number:
            print(f"Recognized Number: {recognized_number}")

            # Make a call using the recognized number
            print(f"Calling {recognized_number}...")
            make_call_with_number(recognized_number)
        else:
            print("No number was recognized.")
    except Exception as e:
        print(f"Error: {e}")
