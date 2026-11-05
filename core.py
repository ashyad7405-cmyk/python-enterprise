import logging
import requests
from database import get_all_alerts

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def check_market_prices(webhook_url: str = None):
    """Processes real-time evaluation batches against active watch targets."""
    alerts = get_all_alerts()
    if not alerts:
        logging.info("No active market watches set.")
        return

    tickers = [a[0] for a in alerts]
    ticker_ids = ",".join(tickers)
    
    # Public CoinGecko Simple Price endpoint
    api_url = f"https://coingecko.com{ticker_ids}&vs_currencies=usd"
    
    try:
        response = requests.get(api_url, timeout=10)
        response.raise_for_status()
        market_data = response.json()
    except Exception as e:
        logging.error(f"Failed pulling tracking feeds: {e}")
        return

    for ticker, target_price, direction in alerts:
        current_price = market_data.get(ticker, {}).get("usd")
        if current_price is None:
            logging.warning(f"Ticker '{ticker}' market value resolving null.")
            continue

        triggered = False
        if direction == "above" and current_price >= target_price:
            triggered = True
        elif direction == "below" and current_price <= target_price:
            triggered = True

        if triggered:
            msg = f"🚨 ALERT: {ticker.upper()} has crossed {direction} targets! Current: ${current_price} (Target: ${target_price})"
            logging.info(msg)
            if webhook_url:
                send_webhook_notification(webhook_url, msg)

def send_webhook_notification(url: str, message: str):
    try:
        requests.post(url, json={"content": message}, timeout=5)
    except Exception as e:
        logging.error(f"Notification broadcast fault: {e}")
