import os
from bs4 import BeautifulSoup
import lxml
import requests
import smtplib
from dotenv import load_dotenv
from pathlib import Path
from datetime import datetime
import pandas as pd
from tkinter import simpledialog, messagebox
import time

load_dotenv()

def check_price(price_limit: float, name: str, link: str):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-GB,de;q=0.8,fr;q=0.6,en;q=0.4,ja;q=0.2",
        "Dnt": "1",
        "Priority": "u=1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Sec-Gpc": "1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
    }

    response = requests.get(link, headers=headers)

    web_page = response.text

    soup = BeautifulSoup(web_page, "lxml")

    price = soup.find("span", class_ = "a-price-whole").get_text(strip=True).split(".") # type: ignore

    float_price = int(price[0])

    title = soup.find(id="productTitle").get_text().strip() # pyright: ignore[reportOptionalMemberAccess]

    print(f"Checking for: {name}\n")

    print(f"Price: {float_price}\n")

    script_dir = Path(__file__).parent
    os.chdir(script_dir)

    log_path = f"{os.getcwd()}\\tracker.log"

    from datetime import datetime

    now = datetime.now()
    now = now.strftime("%d.%m.%Y %H:%M:%S")


    with open(log_path,"a") as log_file:  # "a" = append mode
        log_file.write(f"{float_price};{now};{name}\n") #;{title};{link}\n")
        # log_file.write(f"Timestamp: {now}\n")
        # log_file.write(f"Checking for: {title}\n")
        # log_file.write(f"Current price: {float_price}\n\n")
        
    if float_price < price_limit:
        with smtplib.SMTP(os.environ["SMTP_ADDRESS"]) as connection:
            connection.starttls()
            connection.login(user=os.environ["EMAIL_ADDRESS"], password=os.environ["EMAIL_PASSWORD"])
            connection.sendmail(from_addr=os.environ["EMAIL_ADDRESS"],
                                to_addrs=os.environ["RECIPIENTS"].split(","),##os.environ["RECIPIENTS"],
                                msg=f"Subject:Amazon Price below {price_limit} for {name}\n\n{title} \n is below {price_limit}.\n \n Check the link: {link}".encode("utf-8"))

script_dir = Path(__file__).parent
os.chdir(script_dir)
print(os.getcwd()) 

try:
    df = pd.read_csv(f"{os.getcwd()}\\products_to_track.csv", sep=";")
except FileNotFoundError:
    messagebox.showerror("Missing file", "products_to_track.csv not found.")
    df = pd.DataFrame(columns=["PRICE_LIMIT","NAME","URL"])

for index, row in df.iterrows():
    check_price(row.PRICE_LIMIT, row.NAME, row.URL)

#input("Press Enter to exit...")

time.sleep(3)