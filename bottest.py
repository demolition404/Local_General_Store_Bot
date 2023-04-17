import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from datetime import datetime, timedelta
import time
import pytz
from os import environ
import requests
# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Define your bot token
TOKEN = '6150861818:AAEDdPme7gSXfRA9ur_RSLqwsPshV6ekh9M'

# Define conversation states
SELECT_ITEM, CONFIRM_ORDER, SEND_ORDER, CONFIRM_ORDER_BY_SHOP_OWNER = range(4)

# Define inventory items
inventory = [
    {"name": "banana", "price": 10, "quantity": 5, "weight": 0.5, "type": "Type A", "brand": "Fresh"},
    {"name": "apple", "price": 15, "quantity": 3, "weight": 0.7, "type": "Type B", "brand": "Fresh"},
    {"name": "strawberry", "price": 20, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Fresh"},
    {"name": "chocolate icecream", "price": 50, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Amul"},
    {"name": "vanilla icecream", "price": 50, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Amul"},
    {"name": "cake", "price": 550, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Miomore"},
    {"name": "chicken roll", "price": 60, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Freshly Made"},
    {"name": "veg kathi roll", "price": 70, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Freshly Made"},
    {"name": "egg roll", "price": 50, "quantity": 8, "weight": 1.2, "type": "Type A", "brand": "Freshly Made"},
    {"name": "icecream cake", "price": 650, "quantity": 8, "weight": 5, "type": "Type A", "brand": "TopBrand"},
    # Add more items here
]

# Define command handlers
def error_handler(update, context):
    """Custom error handler function"""
    # Log the error
    print("An error occurred: {}".format(context.error))
    # You can also send a message to the user or take other actions as needed
    # For example:
    # context.bot.send_message(chat_id=update.message.chat_id, text="An error occurred: {}".format(context.error))

def start(update, context):
    """Start the conversation and display available items."""
    reply_keyboard = [[item["name"]] for item in inventory]
    update.message.reply_text(
        'Welcome to the Store!\nPlease select an item to order:',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return SELECT_ITEM

def select_item(update, context):
    """Handle the selected item and request quantity."""
    item_name = update.message.text
    item = next((item for item in inventory if item["name"] == item_name), None)
    if item:
        context.user_data['selected_item'] = item
        update.message.reply_text(
            f'Selected Item: {item["name"]}\n'
            f'Price: Rs{item["price"]}\n'
            f'Remaining Quantity: {item["quantity"]}\n'
            f'Weight: {item["weight"]} kg\n'
            f'Type: {item["type"]}\n'
            f'Brand: {item["brand"]}\n\n'
            f'Please enter the quantity:')
        return CONFIRM_ORDER
    else:
        update.message.reply_text('Invalid item. Please select an item from the list.')
        return SELECT_ITEM

def confirm_order(update, context):
    """Handle the confirmed order and display total cost."""
    selected_item = context.user_data['selected_item']
    quantity = update.message.text
    try:
        quantity = int(quantity)
        if quantity <= 0:
            raise ValueError
        if quantity > selected_item["quantity"]:
            raise ValueError
    except ValueError:
        update.message.reply_text('Invalid quantity. Please enter a valid quantity.')
        return CONFIRM_ORDER
    
    total_cost = selected_item["price"] * quantity
    update.message.reply_text(
        f'Order Details:\n'
        f'Item: {selected_item["name"]}\n'
        f'Price per item: Rs{selected_item["price"]}\n'
        f'Quantity: {quantity}\n'
        f'Total Cost: Rs{total_cost}\n\n'
        f'Please confirm your order (yes/no):',
        reply_markup=ReplyKeyboardMarkup([['Yes', 'No']], one_time_keyboard=True)
    )
    context.user_data['quantity'] = quantity
    return SEND_ORDER

def send_order(update, context):
    """Handle the order confirmation and send message to store owner."""
    user = update.message.from_user
    confirm = update.message.text.lower()
    if confirm == 'yes':
        selected_item = context.user_data['selected_item']
        quantity = context.user_data['quantity']
        total_cost = selected_item["price"] * quantity
        order_details = f'Item: {selected_item["name"]}\n' \
                        f'Price per item: ${selected_item["price"]}\n' \
                        f'Quantity: {quantity}\n' \
                        f'Total Cost: ${total_cost}\n'
        
        # Send order confirmation to store owner
        # store_owner_chat_id = 'Ayandutta934' # Replace with the chat ID of the store owner
        # context.bot.send_message(chat_id=store_owner_chat_id, text=f'New order from {user.username}:\n{order_details}')
        msg = f'New order from {user.username}:\n{order_details}'
        tel_group_id = 'Ayan934'
    
        
        telegram_api_url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id=@{tel_group_id}&text={msg}"
        tel_resp = requests.get(telegram_api_url)
        if tel_resp.status_code == 200:
            print ("Notification has been sent on Telegram") 
        else:
            print ("Could not send Message") 
        
        # Wait for confirmation from store owner
        # context.user_data['order_details'] = order_details
        # context.user_data['user_username'] = user.username
        # return CONFIRM_ORDER_BY_SHOP_OWNER
        update.message.reply_text(
            'Your order has been placed. Thank you for your purchase!\n'
            'Order details:\n'
            f'{order_details}\n'
            'We will contact you shortly with the order status.'
            
        )
        
    else:
        update.message.reply_text('Order not confirmed. Please start a new order if you wish to proceed.')
    
    # Reset conversation data
    context.user_data.clear()
    return ConversationHandler.END

import random
import string
def place_order(user_username, order_details):
    """
    Placeholder function for placing an order.
    This function can be implemented to interact with a database or external API to place the order and update the order status.
    """
    # Assume the order is placed successfully and the order ID is returned
    order_id = generate_order_id()  # Replace with your logic for generating order ID
    order_status = 'pending'  # Replace with your initial order status

    # Update the order details in the database or external API
    update_order_in_database(order_id, user_username, order_details, order_status)

    # Send order confirmation email or notification to store owner
    send_order_confirmation_email(order_id, user_username, order_details)

    # Return the order ID and status for further processing
    return order_id, order_status

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_order_confirmation_email(user_email, order_details):
    # SMTP Server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_username = 'your_email@example.com'
    smtp_password = 'your_email_password'

    # Email details
    sender_email = 'your_email@example.com'
    recipient_email = user_email
    subject = 'Order Confirmation'
    body = f'Thank you for your order! Order details:\n{order_details}'

    # Create the email message
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        smtp_server = smtplib.SMTP(smtp_server, smtp_port)
        smtp_server.starttls()
        smtp_server.login(smtp_username, smtp_password)
        smtp_server.sendmail(sender_email, recipient_email, message.as_string())
        smtp_server.quit()
        print('Order confirmation email sent successfully!')
    except Exception as e:
        print('Failed to send order confirmation email:', e)


from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    order_id = Column(String(10), unique=True)
    user_username = Column(String(255))
    order_details = Column(String(255))
    order_status = Column(Boolean, default=False)

# Update order in database
def update_order_in_database(order_id, user_username, order_details, order_status):
    # Create database connection
    engine = create_engine('your_database_connection_string')
    Session = sessionmaker(bind=engine)
    session = Session()

    # Query order by order_id
    order = session.query(Order).filter_by(order_id=order_id).first()

    if order:
        # Update order details and order_status
        order.user_username = user_username
        order.order_details = order_details
        order.order_status = order_status

        # Commit changes to database
        session.commit()

        # Close session
        session.close()

        return True  # Return True if update was successful
    else:
        # Close session
        session.close()

        return False  # Return False if order was not found

def generate_order_id():
    """Generate a random alphanumeric order ID with a fixed length of 10 characters."""
    order_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(10))
    return order_id

def confirm_order_by_shop_owner(update, context):
    """Handle the confirmation from store owner and place the order."""
    user = update.message.from_user
    confirm = update.message.text.lower()
    if confirm == 'yes':
        order_details = context.user_data['order_details']
        user_username = context.user_data['user_username']

        # Place the order and send confirmation to customer
        order_id, order_status = place_order(user_username, order_details)
       
    else:
        update.message.reply_text('Order not confirmed. Please start a new order if you wish to proceed.')

    # Reset conversation data
    context.user_data.clear()
    return ConversationHandler.END


def cancel(update, context):
    """Handle cancelation of the conversation."""
    update.message.reply_text('Order canceled. Please start a new order if you wish to proceed.',
                              reply_markup=ReplyKeyboardRemove())
    context.user_data.clear()
    return ConversationHandler.END

# Customer side

# Place an order
# Customer side

import socket

# Place an order
# def place_order(customer_name, item_name):
#     print(f"Placing order for {item_name} by {customer_name}...")

#     # Send order request to shop owner
#     order_request = {
#         "customer_name": customer_name,
#         "item_name": item_name
#     }

#     # Assume shop owner's IP address and port number
#     shop_owner_ip = "127.0.0.1"
#     shop_owner_port = 12345

#     # Create socket and connect to shop owner
#     shop_owner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     shop_owner_socket.connect((shop_owner_ip, shop_owner_port))
#     shop_owner_socket.sendall(str(order_request).encode())

#     # Wait for confirmation from shop owner
#     while True:
#         message = shop_owner_socket.recv(1024).decode()

#         if message == "order_confirmed":
#             print("Order confirmed by shop owner.")
#             break
#         elif message == "order_cancelled":
#             print("Order cancelled by shop owner.")
#             break
#         else:
#             print("Waiting for confirmation from shop owner...")

#     # Close socket
#     shop_owner_socket.close()

# # Shop owner side

# import socket

# # Process order request
# def process_order_request():
#     # Assume shop owner's IP address and port number
#     shop_owner_ip = "127.0.0.1"
#     shop_owner_port = 12345

#     # Create socket and bind to shop owner's IP address and port number
#     shop_owner_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     shop_owner_socket.bind((shop_owner_ip, shop_owner_port))
#     shop_owner_socket.listen(1)
#     print("Waiting for order request from customers...")

#     # Accept connection from customer
#     customer_socket, customer_address = shop_owner_socket.accept()
#     print("Connected to customer:", customer_address)

#     # Receive order request from customer
#     order_request = customer_socket.recv(1024).decode()
#     order_request = eval(order_request)

#     customer_name = order_request["customer_name"]
#     item_name = order_request["item_name"]

#     # Confirm order with the shop owner
#     while True:
#         print(f"Order request from {customer_name} for {item_name}.")
#         confirmation = input("Do you want to confirm the order? (yes/no): ")

#         if confirmation.lower() == "yes":
#             customer_socket.sendall("order_confirmed".encode())
#             print("Order confirmed.")
#             break
#         elif confirmation.lower() == "no":
#             customer_socket.sendall("order_cancelled".encode())
#             print("Order cancelled.")
#             break
#         else:
#             print("Invalid input. Please enter yes or no.")

#     # Close sockets
#     customer_socket.close()
#     shop_owner_socket.close()



def main():
    """Start the Telegram bot."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Define conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECT_ITEM: [MessageHandler(Filters.text, select_item)],
            CONFIRM_ORDER: [MessageHandler(Filters.text, confirm_order)],
            SEND_ORDER: [MessageHandler(Filters.text, send_order)],
            CONFIRM_ORDER_BY_SHOP_OWNER:[MessageHandler(Filters.text, confirm_order_by_shop_owner)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dp.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
