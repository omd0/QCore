import json

with open(file="json/surahs.json", mode='r', encoding='utf-8') as f:
    SurahsList = json.load(f)["chapters"]

with open(file="json/radio.json", mode='r', encoding='utf-8') as f:
    RadioList = json.load(f)["Radios"]

with open(file="json/shiks.json", mode='r', encoding='utf-8') as f:
    Shiks = json.load(f)["reciters"]


########################################################################################################}

class Radio:
    def __init__(self, n: int):
        with open(file="json/radio.json", mode='r', encoding='utf-8') as f:
            self.RadioList = json.load(f)["radios"]
        if 0 < n < 117:
            self.url = self.RadioList[n]["radio_url"]
            self.name = self.RadioList[n]["name"]


def getSurahN(SurahName):
    try:
        for distro in SurahsList:
            SurahID = (distro['chapter_number'])
            ENname = (distro['name_simple'])
            ARname = (distro['name_arabic'])
            if (ARname or ENname) == SurahName:
                return (SurahID)
    except:
        return None


########################################################################################################}
############-Replaceer-###############
def replacer(basestr, toBeRemove, newchar):
    for i in toBeRemove:
        if i in basestr:
            basestr = basestr.replace(i, newchar)
    return basestr

    #############-Searcher-###############


class search:
    def __init__(self, json, word):
        self.value = None
        self.items = None
        for items in json:
            for values in items.items():
                for v in values:
                    # ch = {}
                    if word in v:
                        self.value = v
                        self.items = items
                    else: pass
                    # else:
                    #     ch[values] = {}
                    #     acs = []
                    #     for c in word:
                    #         for a in c:
                    #             ac = ''
                    #             if a == ' ':
                    #                 acs.append(ac)
                    #             else:
                    #                 ac += a
                    #     for w in acs:
                    #         if w in word: ch[values] += 1
                    #     ch[values]['i'] = items
                    #     for max in
                    #     max(ch)





########################################################################>
def getAyahsArray(SurahID: int, NewLine: bool = None):
    if 1 <= SurahID <= 114:
        N = format(SurahID, "01")
        file = "json/surah/surah_" + str(N) + ".json"
        with open(file=file, mode='r', encoding='utf-8') as f:
            VesrseList = json.load(f)
        Vesrses = []
        try:
            i = 0
            while (VesrseList['count']) >= i:
                text = VesrseList['verse']["verse_" + str(i)] + "(" + str(i) + ")"
                if i == 0:
                    Vesrses.append(replacer(text + ",", ['(', '0', ')'], ''))
                    if NewLine: Vesrses.append("\r\n")
                else:
                    Vesrses.append(text)
                    if NewLine: Vesrses.append("\r\n")
                i += 1
        except:
            i = 1
            while (VesrseList['count']) >= i:
                text = VesrseList['verse']["verse_" + str(i)] + "(" + str(i) + ")"
                Vesrses.append(text)
                if NewLine: Vesrses.append("\r\n")
                i += 1
        return (Vesrses)
    else:
        return (["erorr"])


def getAyahsText(SurahID: int, NewLine: bool = None):
    Ayat = getAyahsArray(SurahID, NewLine)
    H = len(Ayat)
    text = ""
    i = 0
    while H > 0:
        text = text + " " + Ayat[i]
        i += 1
        H -= 1
    return text


# Example
# print(getAyahsText(1, True))
########################################################################################################}
def urlP(PageN: int):
    if 1 <= PageN <= 604:
        link = 'http://www.mp3quran.net/api/quran_pages_arabic/' + str(format(PageN, "03")) + '.png'
    else:
        link = 'https://image.flaticon.com/icons/png/512/8/8798.png'
    return (link)


class getQPage:
    def __init__(self, SurahID: int):
        for distro in SurahsList:
            SurahN = (distro['chapter_number'])
            StP = (distro['start_page'])
            EnP = (distro['end_page'])
            Name = (distro['name_arabic'])
            if SurahN == SurahID:
                self.Count = EnP - StP + 1
                self.StartPage = StP
                self.EndPage = EnP
                self.NP = [StP]
                self.SurahName = Name
                N = StP
                while EnP != N:
                    N += 1
                    self.NP.append(N)


########################################################################################################}

class QPage:
    def __init__(self, Surah: {int, str}):
        try:
            ID = int(Surah)
        except:
            ID = int(getSurahN(Surah))

        self.Surah = getQPage(ID)
        self.Name = getQPage(ID).SurahName
        self.ID = ID


########################################################################################################}
class QuranMP3:
    def __init__(self, Surah, Shik: str):
        self.SurahLink = None
        self.ID = None
        name = search(Shiks, Shik)
        self.name = name.items['name']
        if name.items is not None:
            url = name.items['Server']
            self.ID = format(QPage(Surah).ID, "03")
            self.SurahLink = url + '/' + self.ID + '.mp3'


# print(QuranMP3("البقرة", "الباسط").SurahLink)
# print(search(Shiks, 'yasser').items['Server'].split()[0])
# m = ['ss', 2, 'kwk']
# if str(2) in str(m):
#     print(True)