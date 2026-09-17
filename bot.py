import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    await update.message.reply_text("👑 BRXXQ BOT V20 جاهز\nابعت صورة")

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    photo_id = update.message.photo[-1].file_id
    context.user_data['photo'] = photo_id
    kb = [
        [InlineKeyboardButton("🔓 مجاني", callback_data="free")],
        [InlineKeyboardButton("💰 مدفوع - مغبش", callback_data="paid")]
    ]
    await update.message.reply_text("اختار النوع:", reply_markup=InlineKeyboardMarkup(kb))

async def handle_btn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    photo = context.user_data.get('photo')
    if not photo:
        await q.edit_message_text("ابعت الصورة مرة تانية")
        return
    if q.data == "free":
        await context.bot.send_photo(chat_id=q.message.chat_id, photo=photo, caption="🔓 FREE")
        await q.edit_message_text("✅ تم نشر مجاني")
    else:
        await context.bot.send_photo(chat_id=q.message.chat_id, photo=photo, has_spoiler=True, caption="💰 VIP")
        await q.edit_message_text("✅ تم نشر مدفوع مغبش")

app = Application.builder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
app.add_handler(CallbackQueryHandler(handle_btn))

print("Bot started")
app.run_polling()
