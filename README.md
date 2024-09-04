# congress-stock-alerts

A Python script to alert you via email when a member of congress publicizes a new stock trade. Trade data from quiverquant.com

## Prerequisites

- Python 3.x installed on your machine.
- A Gmail account with an app password enabled (if 2-Step Verification is enabled).

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/echoghi/congress-stock-alerts
   cd congress-stock-alerts
   ```

2. **Install the Required Python Packages**:

Make sure you have pip installed. Then, run the following command:

```bash
pip install -r requirements.txt
```

3. **Create a `.env` file**:

Create a .env file in the root directory based on the `env-example` file provided.

## Usage

Run either python script to check for the most recent trade data and send an email alert if a new trade is detected.

## How it works

- The script fetches the trade data from the specified quiverquant URL.
- If a new trade is detected (a trade not previously saved in latest_trade.json), it sends an email alert with the trade details.
- The script also prints the trade details in a readable format in the console.

## Notes

- Ensure that your Gmail account has "Allow less secure apps" enabled if not using an app password. However, using an app password is recommended for security reasons.
- If using an app password, ensure you have 2-Step Verification enabled on your Google account.
