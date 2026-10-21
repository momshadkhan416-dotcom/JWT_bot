import os
import json
import asyncio
import binascii
import requests
import warnings
from urllib3.exceptions import InsecureRequestWarning
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Protobuf modules import (Ensure my_pb2.py and output_pb2.py are in the same folder)
import my_pb2
import output_pb2

warnings.filterwarnings("ignore", category=InsecureRequestWarning)

BOT_TOKEN = "8854493990:AAFTFOWnWkHvqO0nDN95Rxqg4AiOrBXBC4Q"

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
    except Exception:
        return None

def encrypt_message(key, iv, plaintext):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_message = pad(plaintext, AES.block_size)
    return cipher.encrypt(padded_message)

def parse_response(response_content):
    response_dict = {}
    lines = response_content.split("\n")
    for line in lines:
        if ":" in line:
            key, value = line.split(":", 1)
            response_dict[key.strip()] = value.strip().strip('"')
    return response_dict

def process_single_account(uid, password):
    token_data = get_token(password, uid)
    if not token_data or "access_token" not in token_data:
        return None

    try:
        game_data = my_pb2.GameData()
        game_data.timestamp = "2025-05-29 13:11:47"
        game_data.game_name = "free fire"
        game_data.game_version = 1
        game_data.version_code = "1.126.2"
        game_data.os_info = "Android OS 11 / API-30 (RKQ1.201112.002/eng.realme.20221110.193122)"
        game_data.device_type = "Handheld"
        game_data.network_provider = "JIO"
        game_data.connection_type = "MOBILE"
        game_data.screen_width = 720
        game_data.screen_height = 1600
        game_data.dpi = "280"
        game_data.cpu_info = "ARM Cortex-A73 | 2200 | 4"
        game_data.total_ram = 4096
        game_data.gpu_name = "Adreno (TM) 610"
        game_data.gpu_version = "OpenGL ES 3.2"
        game_data.user_id = "Google|c71ff1e2-457f-4e2d-83a1-c519fa3f2a44"
        game_data.ip_address = "182.75.115.22"
        game_data.language = "en"
        game_data.open_id = token_data.get("open_id", "")
        game_data.access_token = token_data.get("access_token", "")
        game_data.platform_type = 4
        game_data.device_form_factor = "Handheld"
        game_data.device_model = "realme RMX1825"
        game_data.field_60 = 30000
        game_data.field_61 = 27500
        game_data.field_62 = 1940
        game_data.field_63 = 720
        game_data.field_64 = 28000
        game_data.field_65 = 30000
        game_data.field_66 = 28000
        game_data.field_67 = 30000
        game_data.field_70 = 4
        game_data.field_73 = 2
        game_data.library_path = "/data/app/com.dts.freefireth-XaT5M7jRwEL-nPaKOQvqdg==/lib/arm"
        game_data.field_76 = 1
        game_data.apk_info = "2f4a7f349f3a3ea581fc4d803bc5a977|/data/app/com.dts.freefireth-XaT5M7jRwEL-nPaKOQvqdg==/base.apk"
        game_data.field_78 = 6
        game_data.field_79 = 1
        game_data.os_architecture = "64"
        game_data.build_number = "2022041388"
        game_data.field_85 = 1
        game_data.graphics_backend = "OpenGLES3"
        game_data.max_texture_units = 16383
        game_data.rendering_api = 4
        game_data.encoded_field_89 = "\x10U\x15\x03\x02\t\rPYN\tEX\x03AZO9X\x07\rU\niZPVj\x05\rm\t\x04c"
        game_data.field_92 = 8999
        game_data.marketplace = "3rd_party"
        game_data.encryption_key = "Jp2DT7F3Is55K/92LSJ4PWkJxZnMzSNn+HEBK2AFBDBdrLpWTA3bZjtbU3JbXigkIFFJ5ZJKi0fpnlJCPDD2A7h2aPQ="
        game_data.total_storage = 64000
        game_data.field_97 = 1
        game_data.field_98 = 1
        game_data.field_99 = "4"
        game_data.field_100 = b"4"

        serialized_data = game_data.SerializeToString()
        encrypted_data = encrypt_message(AES_KEY, AES_IV, serialized_data)
        hex_encrypted_data = binascii.hexlify(encrypted_data).decode('utf-8')

        url = "https://loginbp.ggblueshark.com/MajorLogin"
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 12; ASUS_Z01QD Build/PI)",
            'Connection': "Keep-Alive",
            'Accept-Encoding': "gzip",
            'Content-Type': "application/octet-stream",
            'Expect': "100-continue",
            'X-Unity-Version': "2018.4.11f1",
            'X-GA': "v1 1",
            'ReleaseVersion': "OB54"
        }
        edata = bytes.fromhex(hex_encrypted_data)
        response = requests.post(url, data=edata, headers=headers, verify=False, timeout=10)
        
        if response.status_code == 200:
            example_msg = output_pb2.Lokesh()
            example_msg.ParseFromString(response.content)
            response_dict = parse_response(str(example_msg))
            return response_dict.get("token", None)
    except Exception:
        return None
    return None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["Process File ⚙️", "Vip Status 👑"],
        ["Vip Shop 🛒", "GitHub Status 📊"],
        ["Scheduled Files 📅", "Help 🆘"],
        ["Cancel ❌"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    welcome_text = (
        "👋 Welcome!\n\n"
        "✅ Send your `.json` guest accounts file here to generate real JWT tokens.\n"
        "📁 Files like `jwt_token.json`, `working_account.json`, and `lost_account.json` will be returned instantly."
    )
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "Process File ⚙️":
        await update.message.reply_text("Please upload your `.json` file containing guest accounts now.")
    elif text == "Vip Status 👑":
        await update.message.reply_text("👑 Your VIP Status: Free User")
    elif text == "Vip Shop 🛒":
        await update.message.reply_text("🛒 Contact admin to purchase VIP.")
    elif text == "GitHub Status 📊":
        await update.message.reply_text("📊 GitHub Connection: Connected")
    elif text == "Scheduled Files 📅":
        await update.message.reply_text("📅 No scheduled files.")
    elif text == "Help 🆘":
        await update.message.reply_text("🆘 Send a `.json` file to process tokens.")
    elif text == "Cancel ❌":
        await update.message.reply_text("❌ Cancelled.")
    else:
        await update.message.reply_text("⚠️ Please use the menu buttons or /start.")

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc.file_name.endswith('.json'):
        await update.message.reply_text("❌ Please send a valid .json file only!")
        return

    msg = await update.message.reply_text(f"⏳ Downloading and processing accounts from {doc.file_name}...")
    
    file_path = f"temp_{doc.file_name}"
    try:
        file = await context.bot.get_file(doc.file_id)
        await file.download_to_drive(file_path)

        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        jwt_tokens = {}
        working_accs = {}
        lost_accs = {}
        success_count = 0
        total_count = 0

        accounts_to_process = []
        if isinstance(data, list):
            for acc in data:
                u = str(acc.get("uid", ""))
                p = str(acc.get("password", ""))
                if u and p:
                    accounts_to_process.append((u, p))
        elif isinstance(data, dict):
            for u, p in data.items():
                if u and p:
                    accounts_to_process.append((str(u), str(p)))

        total_count = len(accounts_to_process)

        for uid, password in accounts_to_process:
            token = process_single_account(uid, password)
            if token and token != "N/A":
                jwt_tokens[uid] = token
                working_accs[uid] = password
                success_count += 1
            else:
                lost_accs[uid] = password

        jwt_file = "jwt_token.json"
        working_file = "working_account.json"
        lost_file = "lost_account.json"
        region_file = "accountsUnknown_Region.json"

        for fpath, content in [(jwt_file, jwt_tokens), (working_file, working_accs), (lost_file, lost_accs), (region_file, jwt_tokens)]:
            with open(fpath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=4)

        summary = (
            f"📊 Processing Complete for `{doc.file_name}`\n\n"
            f"✅ Total Accounts: {total_count}\n"
            f"🟢 Successful Tokens: {success_count}\n"
            f"❌ Failed/Lost: {total_count - success_count}"
        )
        await msg.edit_text(summary, parse_mode="Markdown")

        for f_path in [jwt_file, working_file, lost_file, region_file]:
            if os.path.exists(f_path) and os.path.getsize(f_path) > 2:
                with open(f_path, 'rb') as f:
                    await update.message.reply_document(document=f, caption=f"File: {f_path}")
                os.remove(f_path)

    except Exception as e:
        await msg.edit_text(f"❌ Error during processing: {str(e)}")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

async def post_init(application):
    print("🤖 Telegram Bot has started successfully with Real JWT Logic...")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
