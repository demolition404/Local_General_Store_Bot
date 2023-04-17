import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Token for your Telegram bot
TOKEN = '6150861818:AAEDdPme7gSXfRA9ur_RSLqwsPshV6ekh9M'

# Inventory items
inventory = [
    {'item_name': 'Item 1', 'price': 10, 'quantity': 5, 'weight': 1, 'type': 'Type 1', 'brand': 'Brand 1'},
    {'item_name': 'Item 2', 'price': 20, 'quantity': 10, 'weight': 2, 'type': 'Type 2', 'brand': 'Brand 2'},
    {'item_name': 'Item 3', 'price': 30, 'quantity': 8, 'weight': 1.5, 'type': 'Type 1', 'brand': 'Brand 3'},
    {'item_name': 'Item 4', 'price': 15, 'quantity': 3, 'weight': 0.5, 'type': 'Type 2', 'brand': 'Brand 4'},
    {'item_name': 'Item 5', 'price': 25, 'quantity': 7, 'weight': 1, 'type': 'Type 1', 'brand': 'Brand 5'},
    {'item_name': 'Item 6', 'price': 18, 'quantity': 12, 'weight': 2.5, 'type': 'Type 2', 'brand': 'Brand 6'},
    {'item_name': 'Item 7', 'price': 22, 'quantity': 6, 'weight': 1.2, 'type': 'Type 1', 'brand': 'Brand 7'},
    {'item_name': 'Item 8', 'price': 12, 'quantity': 9, 'weight': 0.8, 'type': 'Type 2', 'brand': 'Brand 8'},
    {'item_name': 'Item 9', 'price': 28, 'quantity': 4, 'weight': 1.5, 'type': 'Type 1', 'brand': 'Brand 9'},
    {'item_name': 'Item 10', 'price': 35, 'quantity': 11, 'weight': 2, 'type': 'Type 2', 'brand': 'Brand 10'}
]

# User's current order
current_order = {}

# Conversation states
SELECTING_ITEM, ORDER_CONFIRMATION = range(2)


def start(update, context):
    """Send a welcome message when the /start command is used."""
    update.message.reply_text("Welcome to the General Store Bot! Use the /inventory command to view the available items.")
    inventory_command(update,context)

def inventory_command(update, context):
    """Display the inventory to the user."""
    inventory_list = "Available items:\n"
    for item in inventory:
        inventory_list += f"\nItem Name: {item['item_name']}\n" \
                          f"Price: ${item['price']}\n" \
                          f"Remaining Quantity: {item['quantity']}\n" \
                          f"Weight: {item['weight']} kg\n" \
                          f"Type: {item['type']}\n" \
                          f"Brand: {item['brand']}\n"
    update.message.reply_text(inventory_list)


def select_item(update, context):
    """Prompt the user to select an item from the inventory."""
    # Create a list of item names for the user to choose from
    items = [item['item_name'] for item in inventory]

    # Create a reply keyboard with the list of items
    reply_keyboard = [items[i:i+2] for i in range(0, len(items), 2)]
    update.message.reply_text("Please choose an item from the inventory:", reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SELECTING_ITEM


def add_to_order(update, context):
    """Add the selected item to the user's current order."""
    item_name = update.message.text

    # Find the selected item in the inventory
    selected_item = next((item for item in inventory if item['item_name'] == item_name), None)

    if selected_item:
        # Check if the item is already added to the order
        if item_name in current_order:
            update.message.reply_text("This item is already added to your order.")
        else:
            # Add the item to the current order
            current_order[item_name] = selected_item
            update.message.reply_text(f"{item_name} added to your order.")

    else:
        update.message.reply_text("Invalid selection. Please choose an item from the inventory.")

    return SELECTING_ITEM


def view_order(update, context):
    """Display the current order to the user."""
    order_list = "Current Order:\n"
    total_cost = 0
    for item_name, item in current_order.items():
        order_list += f"\nItem Name: {item_name}\n" \
                      f"Price: ${item['price']}\n" \
                      f"Quantity: 1\n" \
                      f"Total: ${item['price']}\n"
        total_cost += item['price']
    order_list += f"\nTotal Cost: ${total_cost}"
    update.message.reply_text(order_list)


def confirm_order(update, context):
    """Prompt the user to confirm their order."""
    order_list = "Confirm Order:\n"
    total_cost = 0
    for item_name, item in current_order.items():
        order_list += f"\nItem Name: {item_name}\n" \
                      f"Price: ${item['price']}\n" \
                      f"Quantity: 1\n" \
                      f"Total: ${item['price']}\n"
        total_cost += item['price']
    order_list += f"\nTotal Cost: ${total_cost}"

    reply_keyboard = [['Confirm', 'Cancel']]
    update.message.reply_text(order_list, reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return ORDER_CONFIRMATION


def process_order(update, context):
    """Process the user's order and send a message to the store owner."""
    user = update.message.from_user
    choice = update.message.text

    if choice == 'Confirm':
        # Send order confirmation to the user
        order_list = "Order Confirmed:\n"
        total_cost = 0
        for item_name, item in current_order.items():
            order_list += f"\nItem Name: {item_name}\n" \
                          f"Price: ${item['price']}\n" \
                          f"Quantity: 1\n" \
                          f"Total: ${item['price']}\n"
            total_cost += item['price']
        order_list += f"\nTotal Cost: ${total_cost}"
        update.message.reply_text(order_list)

        #        # Send order confirmation to the store owner
        store_owner = 'your_store_owner_username'  # Replace with the username of the store owner
        order_list = "New Order:\n"
        total_cost = 0
        for item_name, item in current_order.items():
            order_list += f"\nItem Name: {item_name}\n" \
                          f"Price: ${item['price']}\n" \
                          f"Quantity: 1\n" \
                          f"Total: ${item['price']}\n"
            total_cost += item['price']
        order_list += f"\nTotal Cost: ${total_cost}"
        context.bot.send_message(chat_id=store_owner, text=order_list)

        # Reset the current order
        current_order.clear()

    else:
        update.message.reply_text("Order cancelled.")

    return ConversationHandler.END


def cancel(update, context):
    """Cancel the current conversation."""
    update.message.reply_text("Order cancelled.")
    current_order.clear()
    return ConversationHandler.END


def main():
    """Main function to start the Telegram bot."""
    # Create the Telegram updater and dispatcher
    updater = Updater(token='6150861818:AAEDdPme7gSXfRA9ur_RSLqwsPshV6ekh9M', use_context=True)  # Replace with your actual bot token
    dispatcher = updater.dispatcher

    # Add conversation handler with the defined states and callbacks
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            SELECTING_ITEM: [MessageHandler(Filters.text, add_to_order)],
            ORDER_CONFIRMATION: [MessageHandler(Filters.regex('^(Confirm|Cancel)$'), process_order)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    # Start the bot
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()


