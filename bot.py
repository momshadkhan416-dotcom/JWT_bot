import os
import json
import requests
import binascii
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import my_pb2
import output_pb2
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 🔑 यहाँ अपना असली Telegram Bot Token डालें (जो BotFather से मिला है)
BOT_TOKEN = "8854493990:AAGkh8BLJI2yEWXuYSvp3UECtIOs69zuuk4"

AES_KEY = b'Yg&tc%DEuh6%Zc^8'
AES_IV = b'6oyZDr22E3ychjM%'

def get_token(password, uid):
    url = "https://ffmconnect.live.gop.garenanow.com/oauth/guest/token/grant"
    headers = {
        "Host": "100067.connect.garena.com",
        "User-Agent": "GarenaMSDK/4.0.19P4 (Vivo Y15c; Android 12; en;IN;)",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "close"
    }
    data = {
        "uid": uid,
        "password": password,
        "response_type": "token",
        "client_type": "2",
        "client_secret": "2ee44819e9b4598845141067b281621874d0d5d7af9d8f7e00c1e54715b7d1e3",
        "client_id": "100067"
    }
    try:
        response = requests.post(url, headers=headers, data=data, verify=False, timeout=10)
        if response.status_code != 200:
            return None
        return response.json()
    except:
        return None

def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded_message)

def parse_response(response_content):
    response_dict = {}
    for line in response_content.split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict

def process_single_account(uid, password):
    token_data = get_token(password, uid)
    if not token_data:
        return None

    game_data = my_pb2.GameData()
    game_data.timestamp = "2025-05-29 13:11:47"
    game_data.game_name = "free fire"
    game_data.game_version = 1
    game_data.version_code = "1.126.2"
    game_data.os_info = "Android OS 11 / API-30"
    game_data.device_type = "Handheld"
    game_data.open_id = token_data["open_id"]
    game_data.access_token = token_data["access_token"]
    game_data.platform_type = 4
    game_data.device_model = "realme RMX1825"
    game_data.encryption_key = "Jp2DT7F3Is55K/92LSJ4PWkJxZnMzSNn+HEBK2AFBDBdrLpWTA3bZjtbU3JbXigkIFFJ5ZJKi0fpnlJCPDD2A7h2aPQ="

    serialized_data = game_data.SerializeToString()
    encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)
    hex_encrypted_data = binascii.hexlify(encrypted_data).decode('utf-8')

    url = "https://loginbp.ggblueshark.com/MajorLogin"
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; ASUS_Z01QD Build/PI)",
        'Content-Type': "application/octet-stream",
        'ReleaseVersion': "OB54"
    }
    
    try:
        response = requests.post(url, data=bytes.fromhex(hex_encrypted_data), headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            example_msg = output_pb2.Lokesh()
            example_msg.ParseFromString(response.content)
            res_dict = parse_response(str(example_msg))
            token = res_dict.get("token", "N/A")
            if token != "N/A":
                return token
    except:
        pass
    return None

# --- Telegram Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("Process File ⚙️"), KeyboardButton("Vip Status 👑")],
        [KeyboardButton("Vip Shop 🛒"), KeyboardButton("GitHub Status 📊")],
        [KeyboardButton("Scheduled Files 📅"), KeyboardButton("Help 🆘")],
        [KeyboardButton("Cancel ❌")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text(
        "👋 स्वागत है!\n\n📂 अपनी गेस्ट अकाउंट्स वाली **.json** फाइल यहाँ भेजें, मैं इसे प्रोसेस करके तुरंत **jwt_token.json**, **working_account.json** और **lost_account.json** फाइलें बना कर वापस भेज दूंगा!",
        reply_markup=reply_markup
    )

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document.file_name.endswith('.json'):
        await update.message.reply_text("❌ कृपया केवल .json फॉर्मेट की फाइल भेजें!")
        return

    msg = await update.message.reply_text("⏳ फाइल डाउनलोड हो रही है और अकाउंट्स प्रोसेस हो रहे हैं, कृपया प्रतीक्षा करें...")

    file = await context.bot.get_file(document.file_id)
    input_path = f"downloaded_{document.message_id}.json"
    await file.download_to_drive(input_path)

    try:
        with open(input_path, 'r') as f:
            accounts = json.load(f)
    except Exception as e:
        await msg.edit_text(f"❌ JSON फाइल रीड करने में एरर आया: {e}")
        return

    jwt_tokens = {}
    working_accs = {}
    lost_accs = {}

    for uid, password in accounts.items():
        token = process_single_account(uid, password)
        if token:
            jwt_tokens[uid] = token
            working_accs[uid] = password
        else:
            lost_accs[uid] = password

    jwt_file = "jwt_token.json"
    working_file = "working_account.json"
    lost_file = "lost_account.json"

    with open(jwt_file, 'w') as f:
        json.dump(jwt_tokens, f, indent=4)
    with open(working_file, 'w') as f:
        json.dump(working_accs, f, indent=4)
    with open(lost_file, 'w') as f:
        json.dump(lost_accs, f, indent=4)

    await msg.edit_text("✅ प्रोसेसिंग पूरी हो गई! फाइलें भेजी जा रही हैं...")

    await update.message.reply_document(document=open(jwt_file, 'rb'), caption="📂 jwt_token.json (Active Tokens)")
    await update.message.reply_document(document=open(working_file, 'rb'), caption="📂 working_account.json (Working Accounts)")
    await update.message.reply_document(document=open(lost_file, 'rb'), caption="📂 lost_account.json (Dead/Invalid Accounts)")

    os.remove(input_path)

async def post_init(application):
    print("🤖 Telegram Bot चालू हो गया है...")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
    
    
  
