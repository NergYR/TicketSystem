import json
import os
import sys
import barcode
from datetime import datetime
import hashlib 

def generate_barcode(data, name):
    # Generate barcode image
    name = "barcodes/" + name
    print("Generating barcode for data: ", data[:10])
    barcode_data = barcode.get_barcode_class("code128")
    barcode_object = barcode_data(data[:10], writer=barcode.writer.ImageWriter())
    barcode_object.save(name)
    print("Barcode image generated successfully.")
    
    
def save_user_data(name, firstname, birth, email, checkoutid):
    # Save user data to file
    iden= hashlib.md5((name+firstname+birth+email+datetime.now().strftime("%Y%m%d%H%M%S")).encode()).hexdigest()
    user_data = {
        "name": name,
        "firstname": firstname,
        "birth": birth,
        "email": email,
        "checkoutid": checkoutid,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id": iden,
        "barcode": iden[:10]
    }
    try:
        with open("user_data.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Ensure existing_data is a list
    if not isinstance(existing_data, list):
        existing_data = []

    # Append new data
    existing_data.append(user_data)

    # Write updated data
    with open("user_data.json", "w") as file:
        json.dump(existing_data, file, indent=4)
    
    generate_barcode(iden, f"barcode_{iden}")
    print("User data saved successfully.")
    
    filename = f"tickets/ticket_{user_data['id']}.json"  
    with open(filename, "w") as file:
        json.dump(user_data, file, indent=4)  
    print("Ticket saved successfully.")

    # append ticket id + checkoutid to file tickets/tickets.json
    ticket_info = {
        "ticket_id": user_data['id'],
        "checkout_id": checkoutid
    }
    
    try:
        with open("tickets/tickets.json", "r") as file:
            existing_data = json.load(file)
    except FileNotFoundError:
        existing_data = []

    # Ensure existing_data is a list
    if not isinstance(existing_data, list):
        existing_data = []

    # Append new data
    existing_data.append(ticket_info)

    # Write updated data
    with open("tickets/tickets.json", "w") as file:
        json.dump(existing_data, file, indent=4)
        
save_user_data("Jon", "Jon", "1990-01-01", "jon@gmail.com", "123456")
 