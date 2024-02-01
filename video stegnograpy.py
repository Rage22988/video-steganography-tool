import cv2
#This tool is created by dead of knight
# Function to hide a message in the least significant bits of pixel values
def hide_message(image, message):
    index = 0
    message += "$"  # Adding a delimiter to mark the end of the message
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(len(image[i][j])):
                if index < len(message):
                    # Encode the character's ASCII value into binary
                    image[i][j][k] = image[i][j][k] & 254 | int(format(ord(message[index]), '08b')[-1])
                    index += 1
    return image

# Function to extract a message hidden in the least significant bits of pixel values
def extract_message(image):
    message = ""
    for i in range(len(image)):
        for j in range(len(image[i])):
            for k in range(len(image[i][j])):
                # Extract the LSB of the pixel value and append to the message
                message += str(image[i][j][k] & 1)
    # Splitting the message based on the delimiter
    message = [message[i:i + 8] for i in range(0, len(message), 8)]
    decoded_message = ""
    for byte in message:
        decoded_message += chr(int(byte, 2))
        if decoded_message[-1] == '$':  # Check for the delimiter
            break
    return decoded_message[:-1]  # Removing the delimiter

# Load the video
cap = cv2.VideoCapture(r'D:\Rap\loka.3gp')

# Check if the video is opened successfully
if not cap.isOpened():
    print("Error: Could not open video.")
else:
    # Read and process each frame of the video
    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            # Encoding a message into the frame
            frame = hide_message(frame, "Your secret message")

            # Display the frame
            cv2.imshow('Steganographed Video', frame)

            # Exit when 'q' is pressed
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break
        else:
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
