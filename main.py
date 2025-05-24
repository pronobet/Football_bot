import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import openai

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Récupération des tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise Exception("Erreur : TELEGRAM_TOKEN ou OPENAI_API_KEY non définis dans les variables d'environnement.")

openai.api_key = OPENAI_API_KEY

# Liste des championnats et compétitions ciblées (exemple)
TARGET_COMPETITIONS = [
    "Premier League",
    "Ligue 1",
    "La Liga",
    "Bundesliga",
    "Serie A",
    "Champions League",
    "Europa League",
    "Coupe du Monde",
    "Euro"
]

def start(update: Update, context: CallbackContext):
    msg = ("Salut ! Je suis ton bot de pronostics football.\n"
           "Envoie /pronostic pour recevoir le pronostic du jour sur les grands championnats et compétitions.")
    update.message.reply_text(msg)

def generate_pronostic():
    """
    Fonction qui appelle OpenAI pour générer un pronostic.
    Tu peux améliorer le prompt pour plus de précision.
    """
    prompt = (
        "Tu es un expert en football. Donne un pronostic pour les matchs du jour "
        "dans les championnats suivants : " + ", ".join(TARGET_COMPETITIONS) + ". "
        "Donne le résultat le plus probable avec un court argument."
    )
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=100,
            temperature=0.7
        )
        pronostic = response.choices[0].text.strip()
        return pronostic
    except Exception as e:
        logger.error(f"Erreur OpenAI: {e}")
        return "Désolé, je n'ai pas pu récupérer le pronostic pour le moment."

def pronostic(update: Update, context: CallbackContext):
    update.message.reply_text("Je prépare le pronostic du jour, un instant ...")
    pronostic_text = generate_pronostic()
    update.message.reply_text(pronostic_text)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("pronostic", pronostic))

    updater.start_polling()
    logger.info("Bot démarré")
    updater.idle()

if __name__ == "__main__":
    main()
