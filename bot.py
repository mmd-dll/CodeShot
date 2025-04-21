from telebot import TeleBot
from telebot.types import Message,CallbackQuery
from telebot.types import ReplyKeyboardMarkup
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from image import image_generate
from time import sleep
from random import randint

bot = TeleBot("YOUR-TOKWN")

data = {
    'admins':[],
    'started':[],
    'users':[],
    'used':[],
    'bot_username':'codeShutter_Bot'
}
progress = {}
id_used = []

def UserPannel():
    button = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add('فعلا هیچی')
    # button = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add('افزودن به گروه ➕')
    # button.add('ثبت نظر 🤝','درباره ما ℹ️')
    return button

def is_gap(message:Message):
    chatType = message.chat.type
    if chatType in ['group','supergroup']:
        return True
    else:
        return False

def generate_id():
    while True:
        the_id = randint(10000,99999)
        if the_id in id_used:
            pass
        else:
            break
    return the_id
    
def code_main(codeid):
    defult = InlineKeyboardButton('پیش‌فرض⛓️',callback_data=f'def_{codeid}')
    custom = InlineKeyboardButton('کاستوم 🪄',callback_data=f'cus_{codeid}')
    button = InlineKeyboardMarkup(row_width=1)
    button.add(defult,custom)
    return button

def dark_or_light(codeid):
    dark = InlineKeyboardButton('دارک',callback_data=f'dark_{codeid}')
    light = InlineKeyboardButton('لایت',callback_data=f'light_{codeid}')
    button = InlineKeyboardMarkup(row_width=2)
    button.add(dark,light)
    return button

def datk():
    styles = [
        'monokai', 'vim', 'native', 'fruity',
        'solarized-dark', 'paraiso-dark', 'gruvbox-dark', 'dracula'
    ]
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for style in styles:
        button = InlineKeyboardButton(style, callback_data=f"style_{style}")
        markup.add(button)
    
    return markup

def send_as_file(codeid):
    send_file = InlineKeyboardButton('ارسال فایل',callback_data=f'file_{codeid}')
    button = InlineKeyboardMarkup(row_width=1)
    button.add(send_file)
    return button

def light():
    styles = [
        'default', 'xcode', 'emacs', 'friendly',
        'autumn', 'igor', 'murphy', 'pastie',
        'paraiso-light', 'gruvbox-light', 'borland', 'trac',
        'bw', 'solarized-light', 'tango'
    ]
    
    markup = InlineKeyboardMarkup(row_width=2)
    
    for style in styles:
        button = InlineKeyboardButton(style, callback_data=f"style_{style}")
        markup.add(button)
    
    return markup

@bot.message_handler(commands=['start'])
def Welcome(message:Message):
    userID = message.from_user.id
    if is_gap(message):
        gap_id = message.chat.id
        if message.text == f'/start@{data["bot_username"]}':
            if userID not in data['users']:
                data['users'].append(userID)
            with open('welcome.png', 'rb') as photo:
                bot.send_photo(gap_id,photo,'درود دوست من\n\nروی کدی که میخوای /codepic رو ریپلای کن و لذت ببر...',reply_to_message_id=message.message_id)
    else:
        if userID in data['admins']:
            pass
        else:
            if userID not in data['started']:
                data['started'].append(userID)
            if userID not in data['users']:
                data['users'].append(userID)
            bot.reply_to(message,'درود به ربات کد شاتر خوش اومدی',reply_markup=UserPannel())

@bot.message_handler(commands=['codepic'])
def CodePic(message:Message):
    userid = message.from_user.id
    if is_gap(message):
        if message.text.startswith(f'/codepic'):
            if message.reply_to_message:
                text = message.reply_to_message.text
                codeid = generate_id()
                progress[codeid] = {
                    'code':text,
                    'mode':'def',
                    'chatid':message.from_user.id
                }
                progress[userid] = codeid
                bot.reply_to(message,'خب شات کد رو چطور بسازم؟',reply_markup=code_main(codeid))
            else:
                bot.reply_to(message,'روی یک پیام ریپلای بزن')
    else:
        dont_have_gap = InlineKeyboardButton('گروهی نداری؟',url='https://t.me/programersG')
        add_to_gap = InlineKeyboardButton('رباتو به گروهت اد کن',url=f'https://t.me/{data["bot_username"]}?startgroup=true')
        button = InlineKeyboardMarkup(row_width=1)
        button.add(dont_have_gap,add_to_gap)
        bot.reply_to(message,'از این کد توی گروه استفاده کنید',reply_markup=button)


@bot.callback_query_handler(func=lambda call:call.data.startswith('def_'))
def defult_shut(call:CallbackQuery):
    pid = call.data.split('_')[1]
    if call.from_user.id == progress[int(pid)]['chatid']:
        a = image_generate(code=progress[int(pid)]['code'],name=f'{pid}')
        if a == 'Done':
            bot.delete_message(call.message.chat.id,call.message.message_id)
            with open(f'{pid}.png', 'rb') as photo:
                bot.send_photo(call.message.chat.id,photo,caption=f'by @{data["bot_username"]}',reply_markup=send_as_file(pid))
        else:
            bot.delete_message(call.message.chat.id,call.message.message_id)
            bot.send_message(call.message.chat.id,a)
        sleep(30)
        import os
        os.remove(f'{pid}.png')
        progress.pop(int(pid))
    else:
        bot.answer_callback_query(call.id,'این برای شما نیست',show_alert=True)

@bot.callback_query_handler(func=lambda call:call.data.startswith('cus_'))
def start_custom_code(call:CallbackQuery):
    userID = call.from_user.id
    pid = call.data.split('_')[1]
    if userID == progress[int(pid)]['chatid']:
        bot.edit_message_text('خب نوع تم مورد نظر رو انتخاب کن',call.message.chat.id,call.message.message_id,reply_markup=dark_or_light(pid))
    else:
        bot.answer_callback_query(call.id,'این برای شما نیست',show_alert=True)
        
@bot.callback_query_handler(func=lambda call:call.data.startswith('dark_'))
def datk_(call:CallbackQuery):
    pid = call.data.split('_')[1]
    if call.from_user.id == progress[int(pid)]['chatid']:
        bot.edit_message_text('تم مورد نظر رو انتخاب کن',call.message.chat.id,call.message.message_id,reply_markup=datk())
    else:
        bot.answer_callback_query(call.id,'این برای شما نیست',show_alert=True)

@bot.callback_query_handler(func=lambda call:call.data.startswith('light_'))
def datk_(call:CallbackQuery):
    pid = call.data.split('_')[1]
    if call.from_user.id == progress[int(pid)]['chatid']:
        bot.edit_message_text('تم مورد نظر رو انتخاب کن',call.message.chat.id,call.message.message_id,reply_markup=light())
    else:
        bot.answer_callback_query(call.id,'این برای شما نیست',show_alert=True)

@bot.callback_query_handler(func=lambda call:call.data.startswith('style_'))
def custome_code_gen(call:CallbackQuery):
    style_name = call.data.split('_')[1]
    userid = call.from_user.id
    if userid in progress:
        pid = progress[userid]
        code = progress[int(pid)]['code']
        bot.delete_message(call.message.chat.id,call.message.message_id)
        a = image_generate(code,style_name,pid)
        if a == 'Done':
            if call.message.reply_to_message:
                with open(f'{pid}.png', 'rb') as photo:
                    bot.send_photo(call.message.chat.id,photo,caption=f'by @{data["bot_username"]}',reply_to_message_id=call.message.reply_to_message.message_id,reply_markup=send_as_file(pid))
            else:
                with open(f'{pid}.png', 'rb') as photo:
                    bot.send_photo(call.message.chat.id,photo,caption=f'by @{data["bot_username"]}',reply_markup=send_as_file(pid))
        sleep(30)
        import os 
        os.remove(f'{pid}.png')
        progress.pop(int(pid))
    else:
        bot.answer_callback_query(call.id,'این برای شما نیست',show_alert=True)
    
@bot.callback_query_handler(func=lambda call:call.data.startswith('file_'))
def send_file(call:CallbackQuery):
    try:
        pid = call.data.split('_')[1]
        with open(f'{pid}.png', 'rb') as file:
            bot.send_document(call.message.chat.id, file,caption=f'by @{data["bot_username"]}',reply_to_message_id=call.message.message_id)
    except:
        bot.answer_callback_query(call.id,'فایل حذف شده',show_alert=True)
print('bot started')
bot.infinity_polling()
