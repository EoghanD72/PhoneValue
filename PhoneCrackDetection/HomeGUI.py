import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import ImageTk, Image
import subprocess

#temporary images
tempcrackimage = "tempcrackimage/tempcrack.PNG"
crackimg = "crackimg/2.PNG"
tempmodelimage = "tempmodelimage/setting1.PNG"

def detect_model():
    import cv2
    import pytesseract

    # Mention the installed location of Tesseract-OCR in your system
    pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    # Read image from which text needs to be extracted

    img4 = cv2.imread(tempmodelimage)

    imS = cv2.resize(img4, (375, 812))  # Resize image


    img_not = cv2.bitwise_not(imS)

    # Preprocessing the image starts

    # Convert the image to gray scale
    gray = cv2.cvtColor(img_not, cv2.COLOR_BGR2GRAY)


    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    # Specify structure shape and kernel size.
    # Kernel size increases or decreases the area
    # of the rectangle to be detected.
    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (80, 10))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=2)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)

    # Creating a copy of image
    im2 = img_not.copy()

    # A text file is created
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

        # Read all text as lowercase
        text = text.lower()

        # Write the text into file
        file.write(text)
        file.write("\n")

        # Close the file
        file.close

        # Read the file containing all phone models
        model_file = open("phone_models.txt", "r")

        # Reads each line as a phone model
        phone_models = [model.lower().strip() for model in model_file.readlines()]

        # Checks the detected tesseract model against every model in the text file
        # If found the return the match
        for model in phone_models:
            if model in text:
                print(f"Phone model found: {model}")
                finalmodel=model
    return finalmodel




def quality():
    import numpy as np
    import cv2

    img4 = cv2.imread(tempcrackimage) #reads image set in tempcrackimage

    # Resize image
    width, height = 408, 774
    img4 = cv2.resize(img4, (width, height))
    canny_edge = cv2.Canny(img4, 15, 25, L2gradient=True) #applying canny edge detection with variables set for threshold

    # Threshold the edge map to get a binary matrix
    thresh_value = 0.5  # adjust this threshold value between 0 and 1
    _, binary_image = cv2.threshold(canny_edge.astype(np.float32), thresh_value, 1, cv2.THRESH_BINARY)

    # save binary image as text file
    np.savetxt('binary_image.txt', binary_image, fmt='%d')
    #calculate all pixels in image
    total_pixels = binary_image.shape[0] * binary_image.shape[1]
    #count all white pixels in image
    white_pixels = np.count_nonzero(binary_image)
    #calculates percentage of cracks
    edge_percentage = white_pixels / total_pixels * 100

    #prints percentage as well as white pixel amount and total pixels in image
    print("Percentage of cracks detected:", edge_percentage, white_pixels, total_pixels)

    #writes the edgedetected image to crack image. (This will be used later to display in GUI)
    crackimg = cv2.imwrite("crackimg/2.PNG", canny_edge)
    quality1 = ""

    #grade quality based on percentages set for level of cracks
    if edge_percentage <= 1.35:
        print("PHONE IS LIKE NEW")
        quality1 = "New"
    elif edge_percentage > 1.35 and edge_percentage <= 1.75:
        print("PHONE IS EXCELLENT QUALITY")
        quality1 = "Excellent"
    elif edge_percentage > 1.75 and edge_percentage <= 2.15:
        print("PHONE IS GOOD QUALITY")
        quality1 = "Good"
    elif edge_percentage > 2.15 and edge_percentage <= 3.33:
        print("PHONE IS OK QUALITY")
        quality1 = "Fair"
    else:
        print("PHONE IS POOR QUALITY")
        quality1 = "Poor"
    return quality1 #returns the quality so it can be used later in GUI

def price():
    # import selenium
    from selenium import webdriver
    from selenium.webdriver.common.by import By

    #retrieves phone model and quality grade
    model_search = detect_model()
    quality_search = quality()

    #prints imported variables
    print(model_search, " ", quality_search)

    # create a chrome webdriver
    driver = webdriver.Chrome()

    # imports keys which is used to send input to the driver
    from selenium.webdriver.common.keys import Keys

    # opens ebay through the driver
    driver.get("https://www.ebay.ie/")
    # inspect the search box to find its name attribute "_nkw"
    search_box = driver.find_element(By.NAME, "_nkw")
    # fills the seachbox with the model and quality given
    search_box.send_keys(model_search, " ", quality_search)
    # keys.RETURN sends the enter key
    search_box.send_keys(Keys.RETURN)

    # create a set of keywords to exclude
    #These remove ebay results that will skew our results for prices. Eg "IPHONE XR phonecase - 5.99"
    exclude_keywords = {'case', 'empty', 'replacement', 'microphone', 'camera', 'accessory', 'cover', 'dummy', 'fake',
                        'otter', 'battery', 'dummies', 'screen'}

    # Importing BeautifulSoup to navigate HTML
    from bs4 import BeautifulSoup

    # passes the html source code of the webpage
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # finds all the elements given the "s-item" class
    listings = soup.find_all("li", {"class": "s-item"})

    #creates list for prices
    price_list = []

    # looks through all the listings found and extracts name and price then prints
    for listing in listings:
        try:
            name = listing.find("div", {"class": "s-item__title"}).text.strip()
            #pulls prices of only listings that dont include excluded words in title
            if not any(keyword in name.lower() for keyword in exclude_keywords):
                price = listing.find("span", {"class": "s-item__price"}).text.strip()
                #removes string element to allow a float conversion
                price = float(price.replace("EUR", ""))
                #only adds listings that are over €50
                #this is to remove any other ads that are at unrealistically low prices that will skew result
                if price > 50.0:
                    price_list.append(price)
                #finds condition of ad set by seller.
                #They do not always set this correctly so decision was made to not use this and focus on title
                condition = listing.find("span", {"class": "SECONDARY_INFO"}).text.strip()
                #prints listings
                print(name, "\n", price, "\n", condition, "\n")
        except:
            continue
    #converts all to floats
    price_list = [float(x) for x in price_list]
    #prints list
    print(price_list)

    #averages list, prints it then returns it for use in the GUI
    average = sum(price_list) / len(price_list)

    print("average ", average)
    return average
    # closes driver
    driver.quit()

class ImagePage(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.quality2 = ""
        self.master = master
        self.pack()
        self.create_widgets()
        self.file_path = ""
        self.quality=""
        self.create_quality_label()
        #self.scan_image()

    # creates gui elements within the frame
    def create_widgets(self):
        # creates heading at top of page
        heading = tk.Label(self, text="STEP 1 - UPLOAD IMAGE OF PHONE SCREEN - INSTRUCTIONS BELOW",
                           font=("Helvetica", 24, "bold underline"))
        heading.pack(side="top")

        # Add a label with instructions
        instructions = tk.Label(self, text="•	Make sure a phone is present in the image. \n"
                                           "\n"
                                           "•	Take an image of the phone while the screen is on, displaying a white background with no other text. \n"

                                           "                To do this save an image on Google Images that is a plain white background. Find this image in\n"
                                           "                your camera roll and zoom in fully. This prevents any text being visible on the screen like battery\n"
                                           "                percentage or the clock. By using a white screen it allows the cracks to become more noticeable\n"
                                           "                to the naked eye and allows crack detection to detect all the cracks that it would otherwise\n"
                                           "                miss if the screen was powered off. \n"
                                           "\n"
                                           "•	Make sure the whole phone is within the boundaries of the image so parts of the phone screen \n"
                                           "                are not cropped out. \n"
                                           "\n"
                                           "•	Try to eliminate as much background noise as possible by getting a close up of the phone with its \n"
                                           "                edges close to the photo boundary. \n"
                                           "\n"
                                           "•	Refrain from blurry images or poor lighting conditions.",
                                justify="left",
                                font=("Helvetica", 11))
        instructions.pack(side="top")

        # Add a button to go to model detection
        next_page_button = tk.Button(self, text="Continue to Model Detection", command=self.open_model_page)
        next_page_button.pack(side="bottom")

        # Add a button to begin scanning uploaded image
        continue_button = tk.Button(self, text="Scan Phone Screen", command=self.scan_image)
        continue_button.pack(side="bottom")

        # Add a button to upload an image
        upload_button = tk.Button(self, text="Upload Phone Screen", command=self.upload_image)
        upload_button.pack(side="bottom")

        # used to display images
        panel = tk.Label(self)
        panel.pack()

    # creates window and initialises ModelPage
    def open_model_page(self):
        model_window = tk.Toplevel(root)
        model_page = ModelPage(model_window)

    # creates label to display phone quality and returns for later use
    def create_quality_label(self):
        self.quality_label = tk.Label(root, text="Quality: N/A")
        self.quality_label.pack()
        return self.quality_label

    def upload_image(self):
        # Open a file to select an image
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if file_path:
            # opens image, resizes, adds to panel and saves to tempcrackimage
            image = Image.open(file_path)
            image2 = cv2.imread(file_path)
            max_size = (250, 250)
            image.thumbnail(max_size)
            img = ImageTk.PhotoImage(image)
            panel.config(image=img)
            panel.image = img
            self.file_path = file_path
            cv2.imwrite("tempcrackimage/tempcrack.PNG",image2)

    def scan_image(self):
        # calls quality function to begin crack detection
        qua = quality()
        # retrieves returned quality rating from the function and prints
        print(qua)
        text = "Quality: ", quality()
        print(text)
        # edits the quality label to display the discovered quality
        self.quality_label.config(text="Phone Quality Rating: " + qua)

        # opens crack detection image, resizes and adds to panel
        image = Image.open(crackimg)
        max_size = (250, 250)
        image.thumbnail(max_size)
        img = ImageTk.PhotoImage(image)
        panel.config(image=img)
        panel.image = img


class ModelPage(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.file_path_model = ""
        self.create_model_label()
        self.create_price_label()

    # creates gui elements within the frame
    def create_widgets(self):
        # creates heading at top of page
        heading = tk.Label(self, text="STEP 2 - UPLOAD SETTINGS PAGE FOR MODEL DETECTION",
                           font=("Helvetica", 24, "bold underline"))
        heading.pack(side="top")

        # Add a label with instructions
        instructions = tk.Label(self, text="•	Make sure a phone is present in the image. \n"
                                           "\n"
                                           "•	Make sure the whole phone is within the boundaries of the image so parts of the phone screen \n"
                                           "                are not cropped out. \n"
                                           "\n"
                                           "•	Try to eliminate as much background noise as possible by getting a close up of the phone with its \n"
                                           "                edges close to the photo boundary. \n"
                                           "\n"
                                           "•	Make sure that the correct settings page is being photographed, where information of the phone\n"
                                           "                model name is clearly displayed. \n"
                                           "\n"
                                           "•	Refrain from blurry images or poor lighting conditions.\n"
                                           "\n"
                                           "•               ALL INFORMATION IS DISPLAYED ON MAIN SCREEN",
                                justify="left",
                                font=("Helvetica", 11))
        instructions.pack(side="top")

        # Add a button to scan the average price for current phone
        scan_price_button = tk.Button(self, text="Scan Web For Average Value", command=self.scan_price)
        scan_price_button.pack(side="bottom")

        # Add a button to scan the uploaded image for phone model
        scan_model_button = tk.Button(self, text="Scan For Model", command=self.scan_model)
        scan_model_button.pack(side="bottom")

        # Add a button to upload a model
        upload_button = tk.Button(self, text="Upload Settings Page", command=self.upload_image_model)
        upload_button.pack(side="bottom")


    def scan_model(self):
        # calls detect model function to begin tesseract to read the phone model in
        foundmodel = detect_model()
        # prints model returned
        print(foundmodel)
        # edits the model label to display the discovered model
        self.model_label.config(text="Phone Model Detected: "+ foundmodel)

    def scan_price(self):
        # calls price function to begin web skimming to retrieve average price with info given by user
        foundprice = price()
        # prints average price
        print(foundprice)
        # edits the price label to display the average price and round to 2 decimal places
        self.price_label.config(text="Average Price of Similar Phones: €{:.2f}".format(foundprice))

    def upload_image_model(self):
        # Open a file to select an image
        file_path_model = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if file_path_model:
            # opens image, resizes, adds to panel and saves to tempcrackimage
            image = Image.open(file_path_model)
            image2 = cv2.imread(file_path_model)
            max_size = (250, 250)
            image.thumbnail(max_size)
            img = ImageTk.PhotoImage(image)
            panel.config(image=img)
            panel.image = img
            self.file_path_model = file_path_model
            cv2.imwrite("tempmodelimage/setting1.PNG", image2)

    # creates label to display phone model and returns for later use
    def create_model_label(self):
        self.model_label = tk.Label(root, text="Model: N/A")
        self.model_label.pack()
        return self.model_label

    # creates label to display phone price and returns for later use
    def create_price_label(self):
        self.price_label = tk.Label(root, text="Price: N/A")
        self.price_label.pack()
        return self.price_label

# Create the root window
root = tk.Tk()
#sets size of main window
root.geometry("1280x750")
#sets title to homepage
root.title("Homepage")

#displays images
panel = tk.Label(root)
panel.pack()

# Create instances of the image add it to the root window
imagepage = ImagePage(master=root)

# Show the homepage first
imagepage.tkraise()
# Run the main event loop
root.mainloop()
