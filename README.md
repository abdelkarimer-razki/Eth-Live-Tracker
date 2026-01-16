🪙 Ethereum Live Price Tracker & Alerter
A real-time cryptocurrency web scraper built with Python and Selenium. This tool monitors Ethereum prices on CoinMarketCap, provides live terminal updates with color-coded trends, and alerts you when your target price is reached.

✨ Features
Real-Time Tracking: Scrapes live data directly from CoinMarketCap.

Dual Browser Support: Choose between Chrome or Brave via an interactive CLI prompt.

Target Alerts: Automatically stops and notifies you when Ethereum hits your specified price.

Visual Reports: Generates a Matplotlib line chart (eth_price_chart.png) upon completion.

Data Logging: Automatically saves all tracked data to a structured CSV file for future analysis.

Anti-Bot Protection: Implements randomized sleep intervals and headless browsing to mimic human behavior.

🛠️ Tech Stack
Scraping: Selenium, BeautifulSoup4

Data Management: Pandas

Visualization: Matplotlib

UI/UX: Questionary (CLI menus), tqdm (progress bars)

Driver Management: Webdriver Manager

🚀 Getting Started
Prerequisites
Python 3.x installed.

Google Chrome or Brave Browser installed.

Install the required dependencies:

Bash
pip install matplotlib pandas beautifulsoup4 tqdm selenium webdriver-manager questionary
Installation
Clone this repository:

Bash
git clone https://github.com/yourusername/eth-price-tracker.git
cd eth-price-tracker
Create a folder named docs in the root directory (where the data and charts will be saved):

Bash
mkdir docs
💻 Usage
Run the script by passing your Target Price as a command-line argument.

Bash
# Example: Alert me when ETH reaches 2500.50
python main.py 2500.50
Select Browser: The script will ask if you are using Chrome or Brave.

Initialization: A progress bar will show the status of the Selenium driver setup.

Live Feed: The terminal will display the current price:

🟢 Green: Price increased.

🔴 Red: Price decreased.

Exit: Stop the script manually with CTRL + C or let it reach the target price.

📊 Output
After the program finishes (either by hitting the target or manual exit), check the docs/ folder for:

eth_data.csv: A full log of every price point scraped with timestamps.

eth_price_chart.png: A visual trend chart showing price movements over time.