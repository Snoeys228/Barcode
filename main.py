import cv2
from pyzbar.pyzbar import decode
import requests
from bs4 import BeautifulSoup
import webbrowser
from tkinter import Tk, messagebox
import time

processed_barcodes = set()

import requests

def check_and_open_ean_product(ean_code):
    # Construct the search URL
    search_url = f"https://www.ean-search.org/?q={ean_code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Send a GET request to the search page
    response = requests.get(search_url, headers=headers)
    
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all <p> tags
        p_tags = soup.find_all('p')
        
        # Check if there are at least three <p> tags
        if len(p_tags) >= 5:
            found = p_tags[3]
            Link = p_tags[4]
            # Check if the third <p> contains the product name information
            found_product = found.find('b')
            if found_product and "No product name found for EAN" not in found_product.text:
                # Find the first <a> tag within the <p> tag that contains the link
                product_link = f"https://www.ean-search.org/ean/{ean_code}"
                # Open the product link in the default web browser
                webbrowser.open(product_link)
                print(f"Opened product page: {product_link}")
            else:
                print(f"No product name found for EAN {ean_code}.")
        else:
            print("Unexpected page structure: Less than 3 <p> tags found.")
    else:
        print(f"Failed to retrieve the page. HTTP Status Code: {response.status_code}")

cap = cv2.VideoCapture(0)

while cap.isOpened():
    succes, frame = cap.read()
    #flip image like mirror image
    frame = cv2.flip(frame,1)
    focus = 0
    cap.set(28,focus)
    detectedBarcode = decode(frame)
    if not detectedBarcode:
        print("no any barcode detected")
    else:
        for barcode in detectedBarcode:
           #if barcode is not blank
           if barcode.data != "":
                cv2.putText(frame, str(barcode.data), (55,55), cv2.FONT_ITALIC,2,(0,255,255),2 )
                processed_barcodes.add(barcode.data)
                break
    cv2.imshow('scanner', frame)
    if cv2.waitKey(1) == ord('q'):
        break
done = set()
print(processed_barcodes)
for barcode in processed_barcodes:
    barcode = barcode.decode('utf-8')
    if barcode not in done:
        check_and_open_ean_product(barcode)
        done.add(barcode)
        
time.sleep(1)
