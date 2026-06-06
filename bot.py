import os
import logging

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
    ContextTypes,
    filters
)

from converters import word_to_pdf, pdf_to_word


# =====================================
# CONFIGURATION
# =====================================

TOKEN = "BOT_TOKEN"

DOWNLOAD_FOLDER = "downloads"
OUTPUT_FOLDER = "outputs"

os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)


# =====================================
# START COMMAND
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "Send me:\n"
        "📄 DOCX file → I will convert it to PDF\n"
        "📕 PDF file → I will convert it to DOCX"
    )


# =====================================
# DOCUMENT HANDLER
# =====================================

async def handle_document(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    document = update.message.document

    filename = document.file_name

    await update.message.reply_text(
        "⏳ Downloading file..."
    )

    telegram_file = await document.get_file()

    input_path = os.path.join(
        DOWNLOAD_FOLDER,
        filename
    )

    await telegram_file.download_to_drive(
        input_path
    )

    try:

        # =====================================
        # DOCX TO PDF
        # =====================================

        if filename.lower().endswith(".docx"):

            output_filename = (
                os.path.splitext(filename)[0]
                + ".pdf"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                output_filename
            )

            await update.message.reply_text(
                "🔄 Converting Word → PDF..."
            )

            word_to_pdf(
                input_path,
                output_path
            )

            await update.message.reply_document(
                document=open(output_path, "rb"),
                filename=output_filename,
                caption="✅ Conversion completed"
            )

        # =====================================
        # PDF TO DOCX
        # =====================================

        elif filename.lower().endswith(".pdf"):

            output_filename = (
                os.path.splitext(filename)[0]
                + ".docx"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                output_filename
            )

            await update.message.reply_text(
                "🔄 Converting PDF → Word..."
            )

            pdf_to_word(
                input_path,
                output_path
            )

            await update.message.reply_document(
                document=open(output_path, "rb"),
                filename=output_filename,
                caption="✅ Conversion completed"
            )

        else:

            await update.message.reply_text(
                "❌ Unsupported file type.\n"
                "Please send only PDF or DOCX files."
            )

    except Exception as e:

        logging.error(str(e))

        await update.message.reply_text(
            f"❌ Error:\n{str(e)}"
        )

    finally:

        try:
            if os.path.exists(input_path):
                os.remove(input_path)
        except:
            pass

        try:
            if 'output_path' in locals():
                if os.path.exists(output_path):
                    os.remove(output_path)
        except:
            pass


# =====================================
# ERROR HANDLER
# =====================================

async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE
):

    logging.error(
        msg="Exception occurred:",
        exc_info=context.error
    )


# =====================================
# MAIN
# =====================================

def main():

    app = (
        ApplicationBuilder()
        .token(TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        MessageHandler(
            filters.Document.ALL,
            handle_document
        )
    )

    app.add_error_handler(
        error_handler
    )

    print("Bot is running...")

    app.run_polling()


if __name__ == "__main__":
    main()