# PhoneValue
E-commerce is an area of rapid growth. Most consumers prefer the convenience of shopping online to going into physical stores (Oberlo 2022). Most of us would have had or will have an old smartphone that we would no longer use for various reasons and may have purchased a newer mobile. A study completed by Nchawa and Speake (2015) discovered that 40% of people have 3-4 old mobile phones stocked-piled in their house and that the majority of people would purchase or upgrade to a new phone every 1-2 years. 
The second-hand market for used phones is growing at a rapid pace. In 2021 the used and refurbished smartphone market was valued at 251.09 million units and is forecast to grow to 459.86 million units by 2027 (Mordor Intelligence LLP 2022). It is enticing for a buyer to purchase a second-hand phone due to its reduced cost. Sales of second-hand phones are widely seen on online marketplace sites like Ebay, Done Deal and Facebook Marketplace.
The aim of this project is to detect the value of a mobile in regards to its condition using texture and edge detection techniques. The project developed scanned the phone for damage and considered the phone model, before searching on Ebay for a valuation of similar phones.

The project consists of a number of different models needed to be implemented to achieve its goal. A model needs to determine the type of phone, classify its damage/condition then search for similar items online and determine the value of the phone.

# Crack Detection
•	Make sure a phone is present in the image.
•	Take an image of the phone while the screen is on, displaying a white background with no other text. 
To do this save an image on Google Images that is a plain white background. Find this image in your camera roll and zoom in fully. This prevents any text being visible on the screen like battery percentage or the clock. 
By using a white screen, it allows the cracks to become more noticeable to the naked eye and allows crack detection to detect all the cracks that it would otherwise miss if the screen was powered off.
•	Make sure the whole phone is within the boundaries of the image so parts of the phone screen are not cropped out.
•	Try to eliminate as much background noise as possible by getting a close up of the phone with its edges close to the photo boundary.
•	Refrain from blurry images or poor lighting conditions.

# Model Detection
•	Make sure a phone is present in the image.
•	Make sure the whole phone is within the boundaries of the image so parts of the phone screen are not cropped out.
•	Try to eliminate as much background noise as possible by getting a close up of the phone with its edges close to the photo boundary.
•	Make sure that the correct settings page is being photographed, where information of the phone model name is clearly displayed.
•	Refrain from blurry images or poor lighting conditions.
 
 # Sample png images are given some are good quality some less high quality
