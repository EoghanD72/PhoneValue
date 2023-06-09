# Import required packages
import cv2
import pytesseract
import sys

# Mention the installed location of Tesseract-OCR in your system
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# Read image from which text needs to be extracted
img_path = sys.argv[1]
img4 = cv2.imread(img_path)
#cv2.namedWindow("output", cv2.WINDOW_NORMAL)  # Create window with freedom of dimensions

imS = cv2.resize(img4, (375, 812))  # Resize image
cv2.imshow("output", imS)  # Show image
cv2.waitKey(0)

img_not = cv2.bitwise_not(imS)
cv2.imshow("Invert1",img_not)
cv2.waitKey(0)
# Preprocessing the image starts

# Convert the image to gray scale
gray = cv2.cvtColor(img_not, cv2.COLOR_BGR2GRAY)
cv2.imshow("gray",gray)

# Performing OTSU threshold
ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

# Specify structure shape and kernel size.
# Kernel size increases or decreases the area
# of the rectangle to be detected.
# A smaller value like (10, 10) will detect
# each word instead of a sentence.
rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 10))

# Applying dilation on the threshold image
dilation = cv2.dilate(thresh1, rect_kernel, iterations=2)

# Finding contours
contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_NONE)

# Creating a copy of image
im2 = img_not.copy()

# A text file is created and flushed
file = open("recognized.txt", "w+")
file.write("")
file.close()

# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
for cnt in contours:
    x, y, w, h = cv2.boundingRect(cnt)

    # Drawing a rectangle on copied image
    rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # Cropping the text block for giving input to OCR
    cropped = im2[y:y + h, x:x + w]

    # Open the file in append mode
    file = open("recognized.txt", "a")

    # Apply OCR on the cropped image
    text = pytesseract.image_to_string(cropped)

    text = text.lower()

    # Appending the text into file
    file.write(text)
    file.write("\n")

    # Close the file
    file.close

    model_file = open("phone_models.txt", "r")

    phone_models = [model.lower().strip() for model in model_file.readlines()]

    for model in phone_models:
        if model in text:
            print(f"Phone model found: {model}")


    im2 = cv2.resize(im2, (375, 812))  # Resize image
    cv2.imshow("output", im2)  # Show image
    cv2.waitKey(0)

    cv2.destroyAllWindows()
