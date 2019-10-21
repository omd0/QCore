import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from fake_useragent import UserAgent
import json

UseAgen = UserAgent().ie

with open(file="json/surahs.json", mode='r', encoding='utf-8') as f:
    SurahsList = json.load(f)["chapters"]
########################################################################################################}



def getSurahN(SurahName):
    for distro in SurahsList:
        SurahID = (distro['chapter_number'])
        ENname = (distro['name_simple'])
        ARname = (distro['name_arabic'])
        if (ARname or ENname) == SurahName:
            return (SurahID)
########################################################################################################}
def replacer (basestr, toBeRemove, newchar) :
    for i in toBeRemove :
        if i in basestr:
            basestr = basestr.replace(i, newchar)
    return basestr
########################################################################>
def getAyahsArray(SurahID:int,NewLine:bool=None):
    if 1 <= SurahID <= 114:
        N = format(SurahID, "01")
        file = "json/surah/surah_" + str(N) +".json"
        with open(file=file, mode='r', encoding='utf-8') as f:
            VesrseList = json.load(f)
        Vesrses = []
        try:
            i = 0
            while (VesrseList['count']) >= i:
                text = VesrseList['verse']["verse_" + str(i)] + "(" + str(i) + ")"
                if i == 0:
                    Vesrses.append(replacer(text, ['(','0',')'], ''))
                    if NewLine: Vesrses.append("\r\n")
                else:
                    Vesrses.append(text)
                    if NewLine: Vesrses.append("\r\n")
                i += 1
        except:
            i = 1
            while (VesrseList['count']) >= i:
                text = VesrseList['verse']["verse_"+ str(i)] + "(" + str(i) + ")"
                Vesrses.append(text)
                if NewLine: Vesrses.append("\r\n")
                i += 1
        return (Vesrses)
    else:
        return (["erorr"])

def getAyahsText(SurahID:int,NewLine:bool=None):
    Ayat = getAyahsArray(SurahID,NewLine)
    H = len(Ayat)
    text = ""
    i = 0
    while H > 0:
        text = text + " " + Ayat[i]
        i += 1
        H -= 1
    return (text)



#Example
print(getAyahsText(114, True))
########################################################################################################}




def getPagesN(SurahID):
    for distro in SurahsList:
        SurahN = (distro['chapter_number'])
        StP = (distro['start_page'])
        EnP = (distro['end_page'])
        if SurahN == SurahID:
            return ([StP, EnP])
########################################################################################################}



def getShihkLink(ShikName:str):
    api_key = "AIzaSyAaXi7rrVDIM1OmDN7LyhbYw5sv7IBk_HQ"
    resource = build("customsearch", 'v1', developerKey=api_key).cse()
    result = resource.list(q=ShikName, cx='009951598625815875856:i3qlhsxwjin').execute()
    return (result['items'][0]['link'])
########################################################################################################}




def getQLink(Surah:int, ShikName:str):
    headers = {
        "User-Agent": UseAgen
    }
    int(Surah)
    rn = format(int(Surah), "03")
    str(rn)
    ########################################################################>

    page = requests.get(getShihkLink(ShikName), headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    link = soup.find(attrs={"download": rn + ".mp3"})['href']
    return link
########################################################################################################}



# print(getQLink("الإخلاص", "خالد جليل"))
# print(SurahN("الإخلاص"))
# NDk1MTk0MDgxMDk4NTk2MzYy.XacplA.-eG3SXBHdu5ywvy27bd_1kMhCNU












