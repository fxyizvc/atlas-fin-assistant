from telegram.ext import Application, MessageHandler, filters
from document_handler import handle_document

# Add handler alongside voice and text handlers
app.add_handler(MessageHandler(filters.Document.PDF, handle_document))