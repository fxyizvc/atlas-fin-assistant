import json
import yfinance as yf

def get_stock_quote(symbol: str) -> str:
    """Fetches real-time price, daily change, and 52-week bounds for a stock ticker.
    
    Args:
        symbol (str): The stock ticker symbol (e.g., 'AAPL', 'MSFT').
        
    Returns:
        str: A formatted market data summary or an error message.
    """
    try:
        # Clean ticker string
        symbol = symbol.strip().upper().replace("$", "")
        ticker = yf.Ticker(symbol)
        
        # fast_info provides rapid access to live price data
        fast_info = ticker.fast_info
        
        # Use history to reliably get the last market close price
        # fast_info does not contain a previous_close attribute
        hist = ticker.history(period="2d")
        if hist.empty or len(hist) < 2:
            # Fallback if history data is insufficient
            prev_close = fast_info.open if fast_info.open else fast_info.last_price
        else:
            prev_close = hist['Close'].iloc[-2]

        last_price = round(fast_info.last_price, 2)
        prev_close = round(prev_close, 2)
        
        # Calculate daily change percentage
        change_pct = round(((last_price - prev_close) / prev_close) * 100, 2)
        sign = "+" if change_pct >= 0 else ""
        
        return (
            f"REAL-TIME MARKET DATA FOR {symbol}:\n"
            f"- Current Price: ${last_price}\n"
            f"- Previous Close: ${prev_close}\n"
            f"- Today's Change: {sign}{change_pct}%\n"
            f"- 52-Week High: ${round(fast_info.year_high, 2)}\n"
            f"- 52-Week Low: ${round(fast_info.year_low, 2)}"
        )
    except Exception as e:
        return f"Could not fetch real-time data for symbol '{symbol}'. Error: {str(e)}"


# Formatted tool definition matching the Python implementation capabilities
GET_STOCK_QUOTE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_stock_quote",
        "description": (
            "Fetches current real-time stock price, day change percentage, and 52-week highs/lows. "
            "The model must first extract or resolve the company name into a standard stock ticker symbol "
            "(e.g., Apple becomes AAPL) before calling this tool."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The resolved uppercase stock ticker symbol only (e.g., 'AAPL', 'NVDA', 'MSFT'). Do not pass full company names."
                }
            },
            "required": ["symbol"]
        }
    }
}
