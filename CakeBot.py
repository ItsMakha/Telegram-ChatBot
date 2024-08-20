from typing import Final
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CommandHandler, ContextTypes
import spacy

# Load the spaCy model (make sure to download the model first, e.g., `python -m spacy download en_core_web_sm`)
nlp = spacy.load("en_core_web_sm")

token: Final = '7306843774:AAHiA6YcIcc2Z3fmj2_J6hbyWOUMMPqjaeU'
bot_username: Final = '@swazibakesbot'


FIXED_LATITUDE = -23.874676
FIXED_LONGITUDE = 29.412008

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, do you need help!")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I am Robo Baker. Welcome to Swazi Bakes, how may I help you?")

async def custom(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Custom command")

def message_probability(user_message, recognised_words, single_response=False, required_words=[]):
    message_certainty = 0
    has_required_words = True

    # Check for recognized words in the tokenized message
    for token in user_message:
        if token.text.lower() in recognised_words:
            message_certainty += 1

    percentage = float(message_certainty) / float(len(recognised_words)) if recognised_words else 0

    for word in required_words:
        if word.lower() not in [token.text.lower() for token in user_message]:
            has_required_words = False
            break

    if has_required_words or single_response:
        return int(percentage * 100)
    else:
        return 0

def handler(text: str):
    # Use spaCy to process the text and tokenize it
    processed = nlp(text)
    highest_prob_list = {}
    send_location = False

    def response(bot_response, list_of_words, single_response=False, required_words=[], send_location_flag=False):
        nonlocal highest_prob_list, send_location
        probability = message_probability(processed, list_of_words, single_response, required_words)
        highest_prob_list[bot_response] = probability
        if probability > 50 and send_location_flag:
            send_location = True
        
    # Basic Greetings and Farewells
    response('Hello! Welcome to Swazi Bakes, where sweetness is guaranteed. How can I make your day sweeter?', 
            ['hello', 'hi', 'hey', 'greetings'], single_response=True)
    response('Goodbye! Don’t forget to grab a slice of happiness on your way out!', 
            ['bye', 'goodbye', 'see you', 'later'], single_response=True)
    # Location and Operating Hours
    response('Swazi Bakes is located in the heart of Limpopo, Polokwane. You can find us at [insert specific address if available].', 
             ['where', 'location', 'find', 'bakery'], required_words=['location'])

    # Location and Operating Hours
    response('Swazi Bakes is located in the heart of Limpopo, Polokwane. You can find us at [insert specific address if available].', 
            ['where', 'location', 'find', 'bakery'], required_words=['location'])
    response('Swazi Bakes is located in the heart of Limpopo, Polokwane. You can find us at [insert specific address if available].', 
            ['where', 'location', 'find','based', 'bakery'], required_words=['based'])
    response('Swazi Bakes is located in the heart of Limpopo, Polokwane. You can find us at [insert specific address if available].', 
            ['where', 'location', "located",'find','based', 'bakery'], required_words=['located'])
    response('We’re open Monday through Friday, from 9 AM to 5 PM. Perfect time to grab a cake for any occasion!', 
            ['when', 'hours', 'open', 'close', 'working','work','time'], required_words=['hours'])
    response('We’re open Monday through Friday, from 9 AM to 5 PM. Perfect time to grab a cake for any occasion!', 
            ['when', 'hours', 'open', 'close','working','work', 'time'], required_words=['time'])

    # Cake Prices
    response('Our cake tiers are priced as follows: Tier 1 is R200, Tier 2 is R500, Tier 3 is R750, Tier 4 is R1200, and our elegant Wedding cakes range from R2000 to R5000.', 
            ['how much','what','does','are','price','cake','cost'], required_words=['price'])
    response('Our cake tiers are priced as follows: Tier 1 is R200, Tier 2 is R500, Tier 3 is R750, Tier 4 is R1200, and our elegant Wedding cakes range from R2000 to R5000.', 
            ['how much','what','does','are','price','cake','cost'], required_words=['cost'])
    response('Looking for something special? Our custom cakes start at R200. Let’s create something unforgettable!', 
            ['custom', 'special', 'cake','cakes', 'price'], required_words=['custom'])

    # Cake Types and Flavors
    response('We bake a delightful variety of cakes, including vanilla, chocolate, red velvet, and even specialty flavors like caramel swirl! What’s your favorite?', 
            ['what', 'types','flavour','flavours','have','offer'], required_words=['flavor'])
    response('Our best-selling cakes are the classic chocolate cake and the red velvet cake. Which one would you like to try?', 
            ['what','recommend', 'best', 'popular','what','flavour','which', 'favorite'], required_words=['flavor'])

    # Cake Orders and Customization
    response('You can place an order through our website or give us a call using this telephone number: 081 278 6730, or just drop by the bakery in Polokwane. Need something custom? Just let us know what you’re dreaming of!', 
            ['how', 'order', 'cake', 'buy', 'customize'], required_words=['order', 'cake'])
    response('You can place an order through our website or give us a call using this telephone number: 081 278 6730, or just drop by the bakery in Polokwane. Need something custom? Just let us know what you’re dreaming of!', 
            ['i','would','like','to', 'order', 'cake', 'buy', 'customize'], required_words=['cake'])
    response('Our custom cakes are made just for you! Tell us your theme or idea, and we’ll create a masterpiece.', 
            ['custom', 'cake', 'design', 'personalized'], required_words=['custom', 'cake'])
    response('Our custom cakes are made just for you! Tell us your theme or idea, and we’ll create a masterpiece.', 
            ['custom', 'cake', 'design', 'personalized'], required_words=['personalized', 'cake'])

     # Delivery and Pickup (all related to location)
    response('We offer convenient pickup at our Polokwane location, or we can deliver straight to your door. Delivery fees may apply.', 
             ['delivery', 'pickup', 'get', 'cake', 'where', 'how', 'deliver'], required_words=['delivery', 'pickup'], send_location_flag=True)
    response('Want your cake delivered? We’ve got you covered! Just let us know your location when placing your order.', 
             ['do', 'deliver', 'delivery', 'send'], required_words=['deliver', 'delivery'], send_location_flag=True)
    response('Want your cake delivered? We’ve got you covered! Just let us know your location when placing your order.', 
             ['do', 'offer', 'delivery', 'deliveries', 'send'], required_words=['deliver', 'delivery', 'deliveries'], send_location_flag=True)
    response('Want your cake delivered? We’ve got you covered! We deliver as soon as your order is fresh out of the the oven.', 
             ['do', 'how', 'long', 'take', 'deliver', 'delivery', 'send'], required_words=['deliver'], send_location_flag=True)
    response('Want your cake delivered? We’ve got you covered! We deliver as soon as your order is fresh out of the the oven.', 
             ['i', 'would', 'like', 'my', 'cake', 'delivered', 'deliver', 'delivery', 'send'], required_words=['deliver'], send_location_flag=True)
    

    # Ingredients and Dietary Needs
    response('We use only the finest ingredients in our cakes. Need something gluten-free or vegan? We can do that too!', 
            ['ingredients', 'what\'s in', 'gluten', 'vegan', 'allergies'], required_words=['ingredients', 'gluten', 'vegan'])
    response('All our cakes are made with love and care. Have specific dietary needs? Just ask, and we’ll make it happen.', 
            ['what', 'type','ingredients','ingredient','special', 'diet', 'can', 'you'], required_words=['ingredients'])
    response('We use a whole bunch of recipes to bake our cakes but mainly depending on the flavour of the cake. The basic format is [Recipe]', 
            ['what', 'type','ingredients','ingredient','special', 'diet', 'can', 'you'], required_words=['ingredients'])

    # Occasion Suggestions
    response('Need a cake for a birthday, wedding, or any celebration? We’ve got the perfect cake for every occasion!', 
            ['birthday', 'wedding', 'party', 'event', 'celebration'], required_words=['cake', 'birthday', 'wedding'])
    response('Celebrating something special? Our cakes are perfect for any occasion. What are you celebrating today?', 
            ['special', 'occasion', 'celebrate', 'event'], required_words=['special', 'occasion'])

    # General Information and Assistance
    response('For more information about our cakes and services, feel free to ask! I’m here to help you make the perfect choice.', 
            ['info', 'information', 'details', 'more', 'tell'], required_words=['info', 'information'])
    response('If you have any questions, just ask! I’m here to make your Swazi Bakes experience as sweet as possible.', 
            ['help', 'assistance', 'question', 'support'], required_words=['help'])
    response('If you have any questions, just ask! I’m here to make your Swazi Bakes experience as sweet as possible.', 
            ['help', 'assistance', 'question', 'support'], required_words=['question'])

    # Encouraging Interaction and Final Notes
    response('Our cakes are not just desserts; they’re moments of joy. Let’s make your next celebration unforgettable!', 
            ['suggest', 'recommend', 'something', 'special'], required_words=['suggest', 'recommend'])
    response('We’re always baking up something new! Follow us for the latest flavors and specials.', 
            ['new', 'specials', 'latest', 'update'], required_words=['new', 'specials'])

    # Handling Complex or Unrecognized Queries
    response('I’m not sure I understand, but I’m here to help with anything cake-related! Could you please rephrase?', 
            ['huh', 'what', 'confused', 'don’t', 'understand'], single_response=True)
    
    best_match = max(highest_prob_list, key=highest_prob_list.get)
    return best_match, send_location

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')
    if message_type == 'group':
        if bot_username in text:
            new_text = text.replace(bot_username, '').strip()
            response, send_location = handler(new_text)
        else:
            response, send_location = handler(text)
    else:
        response, send_location = handler(text)
        
    print('Bot:', response)
    await update.message.reply_text(response)
    
    if send_location:
        await context.bot.send_location(chat_id=update.effective_chat.id, latitude=FIXED_LATITUDE, longitude=FIXED_LONGITUDE)      

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    print('Starting Bot...')
    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help))
    application.add_handler(CommandHandler('custom', custom))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error)
    print("Polling...")
    application.run_polling(poll_interval=3)
              