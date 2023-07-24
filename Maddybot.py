import mysql.connector
from telegram import ReplyKeyboardMarkup, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext, \
    ContextTypes, CallbackQueryHandler
import json

NEW_REGISTRATION, NEW_REGISTRATION_LAST_NAME, NEW_REGISTRATION_MOBILE, NEW_REGISTRATION_EMAIL, NEW_REGISTRATION_ADDRESS, NEW_REGISTRATION_CITY, LOGIN, LOGIN_MOBILE, QUANTITY_SELECTION, INDEX, CONFIRM, EXIT = range(
    12)
cuser = ""

PRODUCTS = [
    {"name": "Milk", "price": 30},
    {"name": "Butter", "price": 20},
    {"name": "Dahi", "price": 10},
    {"name": "Bread", "price": 20},
    {"name": "Cheese", "price": 25}
]

# Replace the placeholders with your actual MySQL database credentials
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "telegrambot",
}

db_connection = mysql.connector.connect(**db_config)
db_cursor = db_connection.cursor()


def products(update: Update, context: ContextTypes):
    update.message.reply_text('We have following products...')

    for product in PRODUCTS:
        name = product["name"]
        price = product["price"]
        print(f"Product: {name}, Price: {price} Rs.")
        update.message.reply_text(name + " : " + str(price) + " Rs.")


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    update.message.reply_text(f"Hello {user.first_name}, please select an option:",
                              reply_markup=ReplyKeyboardMarkup([['New Registration', 'Login', 'Exit']],
                                                               one_time_keyboard=True,
                                                               resize_keyboard=True))
    print(update.message.chat_id)
    return NEW_REGISTRATION


def new_registration(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("You selected New Registration. Please provide the following details:\n"
                              "1. First Name\n"
                              "2. Last Name\n"
                              "3. Mobile No.\n"
                              "4. Email\n"
                              "5. Address\n"
                              "6. City\nFirstly, Enter your mobile number to check already a user or not : ")
    print(NEW_REGISTRATION)

    return NEW_REGISTRATION


def save_user_data(update: Update, context: CallbackContext) -> int:
    mobile = update.message.text
    query = "SELECT NAME FROM users WHERE MOBILE_NO = %s"
    db_cursor.execute(query, (mobile,))
    result = db_cursor.fetchone()

    if result:
        first_name = result[0]
        update.message.reply_text(f"Hello {first_name}, you are our customer please login...")
        return LOGIN

    else:
        update.message.reply_text("You Dont have account, Please register...")

        update.message.reply_text("Please provide your Name.")
        return NEW_REGISTRATION_LAST_NAME


def save_last_name(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['name'] = update.message.text
    update.message.reply_text("Please provide your Mobile No.")
    return NEW_REGISTRATION_MOBILE


def save_mobile(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['mobile'] = update.message.text
    update.message.reply_text("Please provide your Email.")
    return NEW_REGISTRATION_EMAIL


def save_email(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['email'] = update.message.text
    update.message.reply_text("Please provide your Address.")
    return NEW_REGISTRATION_ADDRESS


def save_address(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['address'] = update.message.text
    update.message.reply_text("Please provide your City.")
    return NEW_REGISTRATION_CITY


def save_city(update: Update, context: CallbackContext) -> int:
    user_data = context.user_data
    user_data['city'] = update.message.text

    # Save the user data to the database
    chat_id = update.message.chat_id
    user_data['chat_id'] = chat_id
    query = "INSERT INTO users (NAME, MOBILE_NO, EMAIL, ADDRESS, CITY, CHAT_ID) " \
            "VALUES (%(name)s, %(mobile)s, %(email)s, %(address)s, %(city)s, %(chat_id)s)"
    db_cursor.execute(query, user_data)
    db_connection.commit()

    update.message.reply_text("Thank you for registering! You can now use the Login button.")
    update.message.reply_text("Please select a product:", reply_markup=get_product_keyboard())
    return INDEX


def get_product_keyboard():
    keyboard = []

    for product in PRODUCTS:
        button = [InlineKeyboardButton(f"{product['name']} : {product['price']} Rs.", callback_data=product['name'])]
        keyboard.append(button)
        print(button)

    confirm = [[InlineKeyboardButton("Confirm", callback_data="Confirm")]]
    all_buttons = keyboard + confirm
    return InlineKeyboardMarkup(all_buttons)


sproduct = []
qproduct = []
price = []


def index(update: Update, context: CallbackContext) -> any:
    print("Select Product")
    query = update.callback_query

    if query:
        query.answer()
        product_name = query.data

        if product_name == 'Confirm':
            update.callback_query.edit_message_text("Are you sure : (yes/no)", reply_markup=yesno()) # Here add update.message.reply_text()
            return CONFIRM

        else:
            update.callback_query.edit_message_text(f"You selected: {product_name}\n\n"
                                                    "Please enter the quantity:")

            context.user_data['selected_product'] = product_name
            sproduct.append(product_name)

            return QUANTITY_SELECTION
    else:
        # Handle the situation when query is None (for example, if the function is not triggered by a button press)
        update.message.reply_text("Please select a product from the list.")
        return ConversationHandler.END  # End the conversation or redirect to another state as needed


def select_quantity(update, context: CallbackContext):
    quantity = int(update.message.text)
    qproduct.append(quantity)

    for t in PRODUCTS:
        print("in the for t ")
        print(sproduct[-1])
        if t['name'] == sproduct[-1]:
            if quantity > 1:
                price.append(quantity * t['price'])
                context.user_data['total'] = price
                context.user_data['total_price'] = sum(context.user_data['total'])
                print(":::::::::::::::::::::::::::::::::::::::::::")
                print(quantity * t['price'])
                print(":::::::::::::::::context.user_data['total_price']:::::::::::::::::::::")
                print(context.user_data['total_price'])
                print(type(context.user_data['total_price']))
            elif quantity == 0:
                print("Enter correct value")
                update.message.reply_text("Please enter greater than 0 number...")
            elif isinstance(quantity, str):
                update.message.reply_text("Please enter number not character...")
            else:
                context.user_data['total_price'] = t['price']
                context.user_data['total'] = price

    # Ask for more products or exit
    update.message.reply_text("Product added to your order. "
                              "Please select another product or click 'Confirm' to finish.",
                              reply_markup=get_product_keyboard())
    return INDEX


def confirm(update: Update, context: CallbackContext) -> any:
    user_data = context.user_data
    # user_data['select'] = update.message.text
    # select = user_data['select']
    print("ooooooooooooooooooooooooooooooooooooooooooooooooooooo")
    query = update.callback_query

    if query:
        query.answer()
        ans = query.data
        print("***********************************In the confirm query*******************************************")
        if ans == 'Yes':
            print("{}{}{}{}{}{}{}{}{}{}{}{}{}In the ans{}{}{}{{}{}{}{}{}{}{}{}{}{}{}")
            mobile_no = cuser
            print(mobile_no)
            selected_products = dict(zip(sproduct, qproduct))
            user_data['selected_products'] = "\n".join([f"{key} : {value}" for key, value in selected_products.items()])
            print(user_data['selected_products'])
            print("77777777777777777777777")
            print(update)
            chatid = update.callback_query.message.chat.id # here i'm getting error
            print(chatid)
            user_id = "SELECT ID FROM users WHERE CHAT_ID = %s"
            db_cursor.execute(user_id, (chatid,))
            result = db_cursor.fetchone()
            print(result)
            for item in result:
                tuple_as_strings = str(item)
                print(tuple_as_strings)
                user_data['user_id'] = tuple_as_strings
            print(user_data)
            if type(context.user_data['total']) == list:
                del context.user_data['total']
            query = "INSERT INTO order_list(USER_ID, PRODUCTS, TOTAL) " \
                    "VALUES(%(user_id)s, %(selected_products)s, %(total_price)s)"
            db_cursor.execute(query, user_data)
            db_connection.commit()
        else:
            update.callback_query.edit_message_text("Please select a product:", reply_markup=get_product_keyboard())
            return INDEX
    return update.callback_query.edit_message_text("Thank You for ordering, Your order is submitted :)")


def yesno():
    key = []
    YESNO = ['Yes', 'No']
    for i in YESNO:
        button = [InlineKeyboardButton(f"{i}", callback_data=i)]
        key.append(button)

    return InlineKeyboardMarkup(key)


def login(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("You selected Login. Please enter your Mobile No.")
    return LOGIN_MOBILE


def check_mobile(update: Update, context: CallbackContext) -> int:
    mobile = update.message.text

    # Check if the mobile number exists in the database
    query = "SELECT NAME FROM users WHERE MOBILE_NO = %s"
    db_cursor.execute(query, (mobile,))
    result = db_cursor.fetchone()

    if result:
        first_name = result[0]
        update.message.reply_text(f"Hello {first_name}, welcome back!")
        update.message.reply_text("Please select a product:", reply_markup=get_product_keyboard())
        cuser = mobile
        print(cuser)
        return INDEX

    else:
        update.message.reply_text("Invalid Mobile No. Please try again or register as a new user.")
        return start(update, context)


def exit_chat(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("You selected Exit. Goodbye!")
    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text("Operation cancelled. Please select an option:")
    return EXIT


def main():
    updater = Updater('6266046905:AAEi8pQkDF57EvDmE3OhmHtZn4MF70em7ws', use_context=True)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start),
                      CommandHandler('products', products)],
        states={
            NEW_REGISTRATION: [MessageHandler(Filters.regex('^New Registration$'), new_registration),
                               MessageHandler(Filters.text & ~Filters.command, save_user_data)],
            NEW_REGISTRATION_LAST_NAME: [MessageHandler(Filters.text & ~Filters.command, save_last_name)],
            NEW_REGISTRATION_MOBILE: [MessageHandler(Filters.text & ~Filters.command, save_mobile)],
            NEW_REGISTRATION_EMAIL: [MessageHandler(Filters.text & ~Filters.command, save_email)],
            NEW_REGISTRATION_ADDRESS: [MessageHandler(Filters.text & ~Filters.command, save_address)],
            NEW_REGISTRATION_CITY: [MessageHandler(Filters.text & ~Filters.command, save_city)],
            LOGIN: [MessageHandler(Filters.regex('^Login$'), login)],
            LOGIN_MOBILE: [MessageHandler(Filters.text & ~Filters.command, check_mobile)],
            INDEX: [CallbackQueryHandler(index)],
            CONFIRM: [MessageHandler(Filters.text & ~Filters.command, confirm), CallbackQueryHandler(confirm)],
            QUANTITY_SELECTION: [MessageHandler(Filters.text & ~Filters.command, select_quantity)],
            EXIT: [MessageHandler(Filters.regex('^Exit$'), exit_chat)],
        },
        fallbacks=[MessageHandler(Filters.command, cancel)],
    )

    dp.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
