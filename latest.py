import telebot

# Create a Telegram bot instance with your bot token
bot = telebot.TeleBot('6150861818:AAEDdPme7gSXfRA9ur_RSLqwsPshV6ekh9M')

# Define your inventory items with their attributes
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

# Command handler for /start command
@bot.message_handler(commands=['start'])
def start(message):
    # Send a welcome message to the user
    bot.reply_to(message, 'Welcome to our food store! Please use the /menu command to view our inventory and /order to order.')

# Command handler for /menu command
@bot.message_handler(commands=['menu'])
def menu(message):
    # Display the inventory items to the user
    for item in inventory:
        item_info = f"Name: {item['name']}\nPrice: Rs{item['price']}\nQuantity: {item['quantity']}\nWeight: {item['weight']} kg\nType: {item['type']}\nBrand: {item['brand']}\n\n"
        bot.send_message(message.chat.id, item_info)

# Command handler for /order command
@bot.message_handler(commands=['order'])
def order(message):
    # Create a dictionary to store the user's order
    user_order = {}
    bot.send_message(message.chat.id, 'Please enter the names of the items you would like to order, separated by commas.')

    # Define a message handler to capture the items chosen by the user
    @bot.message_handler(func=lambda m: True)
    def capture_items(message):
        # Split the user's message into item names
        items = message.text.split(',')

        # Loop through the inventory to check if the chosen items are available
        for item in inventory:
            if item['name'] in items:
                # Check if the item is still in stock
                if item['quantity'] > 0:
                    # Add the item to the user's order dictionary
                    user_order[item['name']] = item
                    item['quantity'] -= 1  # Reduce the quantity of the item in the inventory
                else:
                    bot.reply_to(message, f"Sorry, {item['name']} is currently out of stock.")

        # Send a confirmation message to the user with the total cost and the items included in the order
        total_cost = sum(item['price'] for item in user_order.values())
        order_info = f"Total Cost: ${total_cost:.2f}\nItems: {', '.join(user_order.keys())}"
        bot.send_message(message.chat.id, order_info)

        # Send a message to the store owner to accept or decline the order
        bot.send_message('-1001801795050', f"New order received from {message.chat.username}.\n{order_info}")

        # Display the final status of the order to the user
        bot.send_message(message.chat.id, 'Thank you for your order! The store owner will confirm your order shortly.')

        # Remove the message handler for capturing items after the order is confirmed
        # bot.remove_message_handler(capture_items)

# Run the bot
bot.polling()