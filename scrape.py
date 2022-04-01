import requests
from bs4 import BeautifulSoup as bs
import time
import os

def scrape_sg():
  while True:
    response = requests.get("https://onemotoring.lta.gov.sg/content/onemotoring/home/driving/traffic_information/traffic-cameras/woodlands.html")
    soup = bs(response.text, "lxml")
    images = ["https:"+i['src'] for i in soup.select(".road-snapshots img")]
    for image in images:
      if not 'nocamera' in image:
        response = requests.get(image)
        folder = image.split("/")[-1].split("_")[0]
        if not os.path.exists(folder):
          os.mkdir(folder)
        with open(folder+"/"+os.path.basename(image), "wb") as f:
          f.write(response.content)
    time.sleep(40)

def scrape_my():
  print(requests.get("https://p3.fgies.com/kl8/img/K001W.jpg?rnd=1648792169914", headers={
    "Accept": "image/avif,image/webp,*/*",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.5",
    "Alt-Used": "p3.fgies.com",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Host": "p3.fgies.com",
    "Referer": "https://p3.fgies.com/kl8/",
    "Sec-Fetch-Dest": "image",
    "Sec-Fetch-Mode": "no-cors",
    "Sec-Fetch-Site": "cross-site",
    "TE": "trailers",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
  }).content)

scrape_sg()