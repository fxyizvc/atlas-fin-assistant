import os
import json
from groq import Groq
from dotenv import load_dotenv
from financial_tools import get_stock_quote

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

USER_SESSIONS = {}

SYSTEM_PROMPT = """You are Atlas, a real-time financial voice assistant.

CRITICAL INSTRUCTIONS FOR TOOL USAGE:
1. ALWAYS call `get_stock_quote` when a user asks about stock prices, updates, quotes, or market updates for any company or ticker (e.g., AAPL, NVDA, TSLA, Apple, Microsoft).
2. NEVER guess stock prices, percentages, or market trends. Always fetch real-time data first via function calling.
3. Keep final responses concise, punchy, and clear for text-to-speech.
"""

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_quote",
            "description": "Fetch real-time stock price, daily change, and 52-week range for a given stock ticker symbol (e.g. AAPL, NVDA, MSFT, TSLA).",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {
                        "type": "string",
                        "description": "The stock ticker symbol, e.g. NVDA, AAPL, MSFT."
                    }
                },
                "required": ["symbol"],
            },
        },
    }
]

def query_llama(prompt: str) -> str:
    """Direct query method for document analysis and unstructured text."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are Atlas, an expert financial analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error analyzing document: {str(e)}"

def generate_response(chat_id: int, user_message: str) -> str:
    if chat_id not in USER_SESSIONS:
        USER_SESSIONS[chat_id] = [{"role": "system", "content": SYSTEM_PROMPT}]
    
    history = USER_SESSIONS[chat_id]
    history.append({"role": "user", "content": user_message})

    if len(history) > 11:
        history = [history[0]] + history[-10:]

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=history,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0.2
        )
        
        response_message = response.choices[0].message

        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)

            if function_name == "get_stock_quote":
                tool_result = get_stock_quote(function_args.get("symbol"))

                history.append(response_message)
                history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": tool_result
                })

                second_response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=history
                )
                bot_reply = second_response.choices[0].message.content
                history.append({"role": "assistant", "content": bot_reply})
                return bot_reply

        bot_reply = response_message.content
        history.append({"role": "assistant", "content": bot_reply})
        return bot_reply

    except Exception as e:
        return f"Atlas encountered a system glitch: {str(e)}"