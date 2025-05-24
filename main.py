import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import openai

# Configuration du logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Clé OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Token Telegram
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Exemple de matchs du jour (à remplacer par une vraie API)
MATCHES = [
    {"home": "PSG", "away": "Marseille", "date": "2025-05-24"},
    {"home": "Manchester United", "away": "Liverpool", "date": "2025-05-24"},
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Bienvenue sur le bot pronostics foot ! Tape /pronostic pour recevoir un pronostic."
    )

async def pronostic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Je prépare le pronostic du jour, un instant ...")

    # Pour cet exemple, on prend juste le premier match du jour
    match = MATCHES[0]
    match_str = f"{match['home']} vs {match['away']}"

    prompt = (
        f"Tu es un expert en football. Donne-moi un pronostic précis et concis pour le match "
        f"{match_str} qui aura lieu aujourd'hui. Propose le score et une explication courte."
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0.7,
        )
        pronostic_text = response['choices'][0]['message']['content']
        await update.message.reply_text(pronostic_text)
    except Exception as e:
        logger.error(f"Erreur OpenAI: {e}")
        await update.message.reply_text(
            "Désolé, je n'ai pas pu récupérer le pronostic pour le moment."
        )


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pronostic", pronostic))

    print("Bot démarré...")
    app.run_polling()


if __name__ == "__main__":
    main()
