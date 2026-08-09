import os
import io
from pypdf import PdfReader
from telegram import Update
from telegram.ext import ContextTypes
import ai_engine

async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    
    # Verify file is a PDF
    if not document.file_name.lower().endswith('.pdf'):
        await update.message.reply_text("Please upload a PDF document for financial analysis.")
        return

    await update.message.reply_text("Downloading and reading your financial document...")

    try:
        # Download file directly into memory
        file_obj = await context.bot.get_file(document.file_id)
        file_bytes = await file_obj.download_as_bytearray()
        
        # Read PDF content
        pdf_reader = PdfReader(io.BytesIO(file_bytes))
        extracted_text = ""
        
        # Limit extraction to first 10 pages for speed/context windows
        for page in pdf_reader.pages[:10]:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"

        if not extracted_text.strip():
            await update.message.reply_text("Unable to extract readable text from this PDF (it might be scanned images).")
            return

        # Truncate to fit LLM context cleanly (~12,000 characters)
        truncated_text = extracted_text[:12000]
        
        caption = update.message.caption or "Provide an executive summary of this financial document with key metrics, revenues, and risks."
        
        prompt = f"""The user uploaded a financial document titled '{document.file_name}'.
User prompt/caption: '{caption}'

DOCUMENT CONTENT:
{truncated_text}

Provide a concise, structured financial analysis based strictly on the text above. Highlight key financial metrics, revenue trends, and primary risks."""

        await update.message.reply_text("Analyzing document content with Atlas AI...")
        
        response = ai_engine.query_llama(prompt)
        await update.message.reply_text(response)

    except Exception as e:
        print(f"PDF Processing Error: {e}")
        await update.message.reply_text("Sorry, an error occurred while processing your PDF document.")