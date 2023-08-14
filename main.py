from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler,CallbackContext

TOKEN: Final = "6457069515:AAGXAdJ5W_L77h8AzC-rhmq_Lh_Ckbyy_2I"
BOT_USERNAME: Final = "@tes_iflab_bot"

NIM, MODUL = range(2)
# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Halo! Selamat Datang di Bot IFLAB')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Masukkan NIM terlebih dahulu!')

async def bap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Masukkan NIM terlebih dahulu!')
    return NIM

# Response

def handle_response(text: str) -> str:
    processed: str = text.lower()

    print(processed)
    if 'halo' in processed:
        return 'halo!'
    else:
        return 'error'


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    response: str = handle_response(text)

    await update.message.reply_text(response)

# BAP
def get_nim(update: Update, context:CallbackContext):
    nim = update.message.text
    # flag = True
    context.default['nim'] = nim
    update.message.reply_text("Data Diri! Silahkan masukkan modul praktikum:")
    return MODUL

def get_modul(update: Update, context:CallbackContext):
    modul = update.message.text
    context.default['modul'] = modul
    update.message.reply_text("Modul diinputkan")
    return ConversationHandler.END

# def bap():
#     app = Application.builder().token(TOKEN).build()
#     conv_handler = ConversationHandler(entry_points=[CommandHandler('bap', bap_command)], states={
#         NIM: [MessageHandler(Filters.TEXT & ~Filters.command, get_nim)],
#         MODUL: [MessageHandler(Filters.TEST & ~Filters.command, get_modul)]
#     },
#     fallbacks=[],
#     )
#     app.add_handlers(conv_handler)
    

# Error Handle
async def error(update:Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__=='__main__':
    print('Starting...')
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))

    conv_handler = ConversationHandler(entry_points=[CommandHandler('bap', bap_command)], states={
        NIM: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_nim)],
        MODUL: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_modul)]
    },
    fallbacks=[],)
    app.add_handler(conv_handler)

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls
    print('Polling...')
    app.run_polling(poll_interval=3)
