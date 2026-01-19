# Importation des  Libraries utiliser 
import matplotlib.pyplot as plt
import pandas as pd
import sys
from bs4 import BeautifulSoup
from tqdm import tqdm
from datetime import datetime
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import questionary

def scrapperInit():
	brave_path = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
	URL = "https://coinmarketcap.com/fr/currencies/ethereum/"
	answer = questionary.select(
		"Which browser do you use?",
		choices=[
			"Chrome",
			"Brave",
		]).ask()

	with tqdm(total=3, desc="Initializing Scraper") as pbar:
		option = Options()
		if (answer == "Brave"):
			option.binary_location = brave_path
		option.add_argument("--headless")
		service = Service(ChromeDriverManager().install())
		pbar.update(1)
		driver = webdriver.Chrome(service=service, options=option)
		pbar.update(1)
		driver.get(URL)
		WebDriverWait(driver, 10)
		pbar.update(1)
	print(f"{GREEN}Initialization Complete! Starting live tracking...{RESET}\n\n")
	return driver

# Choix des couleurs pour l'affichage des messages
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

# Function sauvegarder les resultats apres la fin du programme : CTRL + C
def programShut():
	# Message d'info et importation de fichier CSV
	print(f"{YELLOW}Prices Tracker stops: you can find .csv and the chart of scrapped data in 'docs/*'{RESET}")
	dt = pd.read_csv("docs/eth_data.csv")

	# Visualisation avec matplotlib
	fig, ax = plt.subplots()
	ax.plot(dt['Time'], dt['Price'])
	ax.axhline(y=float(sys.argv[1]), color='red', linestyle='--', label='Target Price')
	ax.grid(True, axis='y', linestyle='--', alpha=0.7)
	ax.set_title("Eth Price by Time")
	ax.set_xlabel("Time of scrapping")
	ax.set_ylabel("Eth price")
	plt.savefig("docs/eth_price_chart.png")
	plt.show()

try:
	# Protection des parametres: sys.argv
	if (len(sys.argv) != 2):
		print(f"{RED}Argv error: Insert a price for alert!{RESET}")
		sys.exit()
	try:
		priceDetector = float(sys.argv[1])
	except:
		print(f"{RED}Argv error: Insert a valid price!{RESET}")
		sys.exit()

	driver = scrapperInit()
	# Affichage de depart
	print(f"Prices Tracker - made by ABDELKARIM, ZIAD AND OUSSAMA\n")

	# Variables
	price = [str(priceDetector)]
	isBigger = True
	changePerc = 0

	# Function d'affichage en temps reel
	def delete_last_line():
		sys.stdout.write("\033[F") 
		sys.stdout.write("\033[K")

	# Loop infinie pour le scrapping en temps reel
	while True:
		try:
			page_source = driver.page_source
			soup = BeautifulSoup(page_source,"html.parser")

			# lecture d'element de prix base sur le nom de la class
			new_price = [price.text for price in soup.select(".WXGwg")]

			# Condition pour detecter si il est plus grand ou petit pour le choix de couleur 
			if (price[0] == new_price[0]):
				continue
			if (price[0] <= new_price[0]):
				isBigger = True
			else:
				isBigger = False
			data = {
				"Coin":"ethereum",
				"Price":new_price[0],
				"Time":datetime.now().replace(microsecond=0)
			}
			delete_last_line()

			# Affichage en vert au cas d'augmentation et en rouge au contraire
			if (isBigger):
				print(f"Price of {data['Coin']} :{GREEN}{data['Price']}{RESET} at {data['Time']}")
			else:
				print(f"Price of {data['Coin']} :{RED}{data['Price']}{RESET} at {data['Time']}")

			# Stockage dans le fichier CSV si il existe
			try:
				dt = pd.read_csv("docs/eth_data.csv")
				data['Price'] = float(data['Price'].replace('\u202f', '').replace('\xa0', '').replace(',', '.').replace('€', ''))
				dt.loc[len(dt)] = data
				dt.to_csv("docs/eth_data.csv", index=False)

			# Creation de fichier CSV
			except:
				dt = pd.DataFrame([data])
				dt["Price"] = float(dt["Price"].replace('\u202f', '').str.replace('\xa0', '').str.replace(',', '.').str.replace('€', ''))
				dt.to_csv("docs/eth_data.csv", index=False)
			oldPrice = float(price[0].replace('\u202f', '').replace('\xa0', '').replace(',', '.').replace('€', ''))

			# Dectection de prix
			if (priceDetector <= data['Price'] and priceDetector > oldPrice) or (priceDetector >= data['Price'] and priceDetector < oldPrice):
				print(f"{GREEN}Price of {data['Coin']} has reached {priceDetector}{RESET}")
				programShut()
				sys.exit()
			price = [price.text for price in soup.select(".WXGwg")]

			# Sleep: pour eviter la detection des anti bot
			# time.sleep(randint(1, 5))

		except Exception as e:
			print(f"Error waiting for element: {e}")

# Appel de function en cas de 'CTRL + C'
except KeyboardInterrupt:
	programShut()