
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os, json
from datetime import datetime, timedelta

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

users_file = "users.json"
abbonati = {}
ultimo_messaggio = None

def salva_utenti():
    with open(users_file, "w") as f:
        json.dump(abbonati, f)

def carica_utenti():
    global abbonati
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            abbonati = json.load(f)

def giorni_mancanti(data_str):
    try:
        data = datetime.strptime(data_str, "%Y-%m-%d")
        return (data - datetime.now()).days
    except:
        return -1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in abbonati and giorni_mancanti(abbonati[user_id]["scadenza"]) > 0:
        giorni = giorni_mancanti(abbonati[user_id]["scadenza"])
        await update.message.reply_text(f"✅ Sei già abbonato! Scade il {abbonati[user_id]['scadenza']} (tra {giorni} giorni).")
        return
    keyboard = [[InlineKeyboardButton("🧾 Abbonati con PayPal", url="https://www.paypal.com/ncp/payment/3ZLRX3468NGXJ")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
await message.reply_text("👋 Benvenuto su *Premium Live Win!*", parse_mode="Markdown")

await message.reply_text("📢 Benvenuto su *Premium Live Win!*", parse_mode="Markdown")
await message.reply_text("🎯 Riceverai giocate live in tempo reale solo se sei abbonato.")
await message.reply_text("💰 Prezzo: 15€ per 30 giorni di accesso.")
await message.reply_text("🛒 Dopo il pagamento, il tuo accesso sarà attivato manualmente.")
await message.reply_text("👇 Premi il pulsante qui sotto per abbonarti ora:", reply_markup=reply_markup, parse_mode="Markdown")

        "💶 *Prezzo:* 15€ per 30 giorni di accesso.")
"
        

"
        "👇 Premi il pulsante qui sotto per abbonarti ora:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def id_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Il tuo ID Telegram è: {update.effective_user.id}")

async def attiva(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usa: /attiva ID")
        return
    user_id = context.args[0]
    scadenza = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")
    abbonati[user_id] = {
        "scadenza": scadenza,
        "attivato_il": datetime.now().strftime("%Y-%m-%d"),
        "username": "@" + (update.effective_user.username or "")
    }
    salva_utenti()
    await update.message.reply_text(f"✅ Utente {user_id} abbonato fino al {scadenza}.")

async def rimuovi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usa: /rimuovi ID")
        return
    user_id = context.args[0]
    if user_id in abbonati:
        del abbonati[user_id]
        salva_utenti()
        await update.message.reply_text(f"❌ Utente {user_id} rimosso.")
    else:
        await update.message.reply_text("ID non trovato.")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID:
        return
    if not context.args:
        await update.message.reply_text("Usa: /info ID")
        return
    user_id = context.args[0]
    dati = abbonati.get(user_id)
    if dati:
        await update.message.reply_text(json.dumps(dati, indent=2))
    else:
        await update.message.reply_text("Nessun dato trovato.")

async def attivi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID:
        return
    oggi = datetime.now().strftime("%Y-%m-%d")
    attivi = [uid for uid, dati in abbonati.items() if giorni_mancanti(dati["scadenza"]) > 0]
    await update.message.reply_text(f"Abbonati attivi: {len(attivi)}")

async def invia(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ultimo_messaggio
    if str(update.effective_user.id) != ADMIN_ID:
        return
    testo = update.message.text.replace("/invia", "").strip()
    count = 0
    for uid, dati in abbonati.items():
        if giorni_mancanti(dati["scadenza"]) > 0:
            sent = await context.bot.send_message(chat_id=int(uid), text=testo)
            ultimo_messaggio = {"id": sent.message_id, "text": testo}
            count += 1
    await update.message.reply_text(f"Inviato a {count} utenti.")

async def modifica(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global ultimo_messaggio
    if str(update.effective_user.id) != ADMIN_ID or not ultimo_messaggio:
        return
    testo = update.message.text.replace("/modifica", "").strip()
    count = 0
    for uid, dati in abbonati.items():
        if giorni_mancanti(dati["scadenza"]) > 0:
            try:
                await context.bot.edit_message_text(chat_id=int(uid), message_id=ultimo_messaggio["id"], text=testo)
                count += 1
            except:
                continue
    await update.message.reply_text(f"Messaggio modificato per {count} utenti.")

async def inviofoto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_user.id) != ADMIN_ID:
        return
    if update.message.photo:
        caption = update.message.caption.replace("/inviofoto", "").strip()
        for uid, dati in abbonati.items():
            if giorni_mancanti(dati["scadenza"]) > 0:
                await context.bot.send_photo(chat_id=int(uid), photo=update.message.photo[-1].file_id, caption=caption)

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    carica_utenti()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("id", id_cmd))
    app.add_handler(CommandHandler("attiva", attiva))
    app.add_handler(CommandHandler("rimuovi", rimuovi))
    app.add_handler(CommandHandler("info", info))
    app.add_handler(CommandHandler("attivi", attivi))
    app.add_handler(CommandHandler("invia", invia))
    app.add_handler(CommandHandler("modifica", modifica))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex("^/inviofoto"), inviofoto))

    print("Bot avviato.")
    app.run_polling()
