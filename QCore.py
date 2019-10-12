import requests
from bs4 import BeautifulSoup
from langdetect import detect
from googleapiclient.discovery import build
import json

########################################################################################################}

def SurahN(Name):
    if detect(Name) == "ar":
        with open(file="json/SListAR.json", mode='r', encoding='utf-8') as f:
            SurahList = json.load(f)
    else:
        with open(file="json/SListEN.json", mode='r', encoding='utf-8') as f:
            SurahList = json.load(f)
    ########################################################################>
    for distro in SurahList:
        SurahID = (distro['id'])
        SurahName = (distro['name'])
        if SurahName == Name:
            return (SurahID)
########################################################################################################}

def ShihkLink(ShikName):
    api_key = "AIzaSyAaXi7rrVDIM1OmDN7LyhbYw5sv7IBk_HQ"
    resource = build("customsearch", 'v1', developerKey=api_key).cse()
    result = resource.list(q=ShikName, cx='009951598625815875856:i3qlhsxwjin').execute()
    return (result['items'][0]['link'])
########################################################################################################}
def getQLink(Surah:{int,str}, ShikName:str):
    headers = {
        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    try:
        int(Surah)
        rn = format(int(Surah), "03")
        str(rn)
    except:
        rn = format(int(SurahN(Surah)), "03")
    ########################################################################>
    str(rn)
    page = requests.get(ShihkLink(ShikName), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.find(attrs={"download": rn + ".mp3"})['href']

    return link
########################################################################################################}


print(getQLink("Qaf", "العجمي"))












