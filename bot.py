import json, os, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TOKEN") or (open("token.txt").read().strip() if os.path.exists("token.txt") else "")
OWNER_IDS=[8205861351,8652555140]
DATA_FILE="bot_data.json"

def load_data():
    try:
        if not os.path.exists(DATA_FILE):
            return {"files":{"hcv":[],"11th":[],"12th":[],"meadesy":[],"neet":[],"song":[],"group":[]}}
        with open(DATA_FILE,'r') as f: return json.load(f)
    except: return {"files":{"hcv":[],"11th":[],"12th":[],"meadesy":[],"neet":[],"song":[],"group":[]}}

def save_data(data):
    try:
        with open(DATA_FILE,'w') as f: json.dump(data,f)
    except: pass

async def post_init(app):
    try: await app.bot.set_my_commands([BotCommand("start","Start Bot - Menu")])
    except: pass

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb=[[InlineKeyboardButton("NEET Batch", callback_data='neet'), InlineKeyboardButton("11th", callback_data='11th')],[InlineKeyboardButton("12th", callback_data='12th'), InlineKeyboardButton("HCV", callback_data='hcv')],[InlineKeyboardButton("Meadesy", callback_data='meadesy'), InlineKeyboardButton("Song", callback_data='song')],[InlineKeyboardButton("Group Link", callback_data='group'), InlineKeyboardButton("About", callback_data='about')]]
    await update.message.reply_text("Welcome to Aafiya Bot - Owner @Shizuka_72", reply_markup=InlineKeyboardMarkup(kb))

async def btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        q=update.callback_query; await q.answer(); data=load_data(); cat=q.data
        if cat=='about':
            await q.message.reply_text("Aafiya Bot | Owner @Shizuka_72"); return
        files=data["files"].get(cat,[])
        if not files: await q.message.reply_text(cat.upper()+" me kuch nahi hai"); return
        await q.message.reply_text(cat.upper()+" Files:")
        for f in files[-20:]:
            if f.get('type')=='link': await q.message.reply_text(f["file_id"])
            else:
                try: await context.bot.send_document(chat_id=q.message.chat_id, document=f['file_id'], caption=f['name'])
                except: pass
    except: pass

async def save_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.effective_user.id not in OWNER_IDS: return
        data=load_data(); txt=(update.message.caption or update.message.text or "").lower(); full=update.message.text or update.message.caption or ""; cat=None
        if "hcv" in txt: cat="hcv"
        elif "11th" in txt: cat="11th"
        elif "12th" in txt: cat="12th"
        elif "neet" in txt: cat="neet"
        elif "group" in txt: cat="group"
        elif "song" in txt: cat="song"
        elif "meadesy" in txt: cat="meadesy"
        if not cat:
            if update.message.audio: cat="song"
            elif update.message.document and update.message.document.file_name and update.message.document.file_name.lower().endswith(('.mp3','.m4a','.flac','.wav')): cat="song"
            elif "t.me" in txt or "https://" in txt: cat="group"
            else: cat="meadesy"
        if "t.me" in txt or "https://" in txt:
            data["files"][cat].append({"file_id":full,"name":cat,"type":"link"}); save_data(data); await update.message.reply_text(f"Saved to {cat.upper()}"); return
        fid=None; fname="File"
        if update.message.document: fid=update.message.document.file_id; fname=update.message.document.file_name
        elif update.message.video: fid=update.message.video.file_id; fname="Video"
        elif update.message.audio: fid=update.message.audio.file_id; fname=update.message.audio.title or "Song"
        if fid: data["files"][cat].append({"file_id":fid,"name":fname,"type":"file"}); save_data(data); await update.message.reply_text(f"Saved to {cat.upper()} - {fname}")
    except: pass

app=Application.builder().token(TOKEN).post_init(post_init).build()
app.add_handler(CommandHandler("start",start))
app.add_handler(CallbackQueryHandler(btn))
app.add_handler(MessageHandler(filters.ALL,save_all))
print("Aafiya Bot Ready"); app.run_polling()
