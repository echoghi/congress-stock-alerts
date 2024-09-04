import requests
import re
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Configuration
URL = os.getenv("URL")
JSON_FILE = os.getenv("JSON_FILE")
EMAIL_TO = os.getenv("EMAIL_TO")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def extract_trade_data():
    # Fetch the webpage
    response = requests.get(URL)
    if response.status_code != 200:
        print("Failed to retrieve webpage.")
        return None
    
    # Extract trade data using regex
    trade_data_match = re.search(r"let tradeData = (\[.*?\]);", response.text, re.DOTALL)
    if not trade_data_match:
        print("Trade data not found.")
        return None
    
    # Parse the trade data as JSON
    trade_data = json.loads(trade_data_match.group(1))
    return trade_data

def get_latest_trade(trade_data):
    # Assuming the trades are sorted by date in descending order, the first entry is the most recent trade
    if not trade_data:
        return None

    latest_trade = trade_data[0]
    trade_details = {
        "stock": latest_trade[8],  # Stock name
        "transaction": latest_trade[1],  # Transaction type (Sale/Purchase)
        "filed_date": latest_trade[2],  # Date filed
        "trade_date": latest_trade[3],  # Trade date
        "description": latest_trade[9],  # Description
        "amount": latest_trade[10],  # Amount range
    }
    return trade_details

def load_last_saved_trade():
    try:
        with open(JSON_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None

def save_latest_trade(trade):
    with open(JSON_FILE, 'w') as file:
        json.dump(trade, file)

def send_email(trade):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO
    msg['Subject'] = f"New Congressional Trade: {trade['trade_date']}"
    body = f"New trade detected:\n\nStock: {trade['stock']}\nTransaction: {trade['transaction']}\nFiled Date: {trade['filed_date']}\nTrade Date: {trade['trade_date']}\nDescription: {trade['description']}\nAmount: {trade['amount']}"
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")

def print_trade_details(trade):
    trade_message = (
        f"New trade detected: {trade['transaction']} of {trade['stock']} "
        f"({trade['description']}) for {trade['amount']} on {trade['trade_date']} "
        f"and filed on {trade['filed_date']}."
    )
    print(trade_message)

def main():
    trade_data = extract_trade_data()
    if not trade_data:
        return

    latest_trade = get_latest_trade(trade_data)
    if not latest_trade:
        return

    last_saved_trade = load_last_saved_trade()

    # If no last saved trade or the new trade is more recent, save it, send email, and print details
    if not last_saved_trade or latest_trade['trade_date'] > last_saved_trade['trade_date']:
        save_latest_trade(latest_trade)
        send_email(latest_trade)
        print_trade_details(latest_trade)

if __name__ == "__main__":
    main()
