import os
import time
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

# حماية من السبام - ذاكرة مؤقتة
user_last_msg = {}

async def check_flood(user_id):
    now = time.time()
    if user_id in user_last_msg:
        if now - user_last_msg[user_id] < 2: # اذا بعت رسالتين بأقل من ثانيتين
            return True
    user_last_msg[user_id] = now
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # حماية: لا تظهر معلومات حساسة
    user_id = update.effective_user.id
    if await check_flood(user_id):
        return
    
    keyboard = [
        [InlineKeyboardButton("🎁 FREE", callback_data='free')],
        [InlineKeyboardButton("👑 VIP 5$", callback_data='vip5')],
        [InlineKeyboardButton("🔴 LIVE 1$/min", callback_data='cam')],
        [InlineKeyboardButton("💎 MONTHLY 50$", callback_data='vip50')],
        [InlineKeyboardButton("🌐 WEBSITE", url='https://brxxq2027k1.neocities.org')]
    ]
    markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "BRXXQ EMPIRE V10 PROTECTED 👑\nSecured & Hidden System Active 🛡️",
        reply_markup=markup
    )
    # اشعار مخفي للادمن فقط - انت بتشوف مين فات
    if ADMIN_ID != 0:
        try:
            await context.bot.send_message(chat_id=ADMIN_ID, text=f"👤 User {user_id} started bot: @{update.effective_user.username}")
        except:
            pass

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = q.from_user.id
    if await check_flood(user_id):
        return
        
    if q.data == 'free':
        await q.message.reply_text("FREE: https://brxxq2027k1.neocities.org")
    elif q.data in ['vip5','cam','vip50']:
        await q.message.reply_text("Contact: @BRXXQ to unlock 🔒\nProtected payment system 🛡️")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if await check_flood(user_id):
        await update.message.reply_text("Slow down bro 🛡️")
        return
    await update.message.reply_text("Use /start 👑")

def main():
    if not BOT_TOKEN:
        print("ERROR: BOT_TOKEN not set! Set it in Render Env")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("BRXXQ V10 PROTECTED BOT Started - Hidden Mode ON 🛡️👑")
    app.run_polling()

if __name__ == "__main__":
    main()
