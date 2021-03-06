import requests
global date
import bs4 as bs 
from datetime import datetime
import pytz
import json,time,django
from treciproj import settings
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "treciproj.settings")
django.setup()
from RaceApp.models import Country
global headers
headers = {'user-agent': 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)', 'origin': 'https://www.equibase.com',
                'x-requested-with': 'XMLHttpRequest'}
def get_table(table):
    #soup = bs.BeautifulSoup(table,'lxml')
    i=0
    dictlist = []
    for tr in table.find_all('tr'):
            i+=1
            tds = tr.find_all('td')
            if(i==1):
                sire = (tds[0].text)
            if(i==3):
                dict = {
            'sire' : sire,
            'name' : tds[0].text,
            'foals' : tds[2].text,
            'starters' : tds[3].text,
            'winners' :  tds[4].text,
            'BW (%)' : tds[5].text,
            'earnings' : tds[6].text,
            'ael' : tds[7].text,
            }
            # print(dict)
                dictlist.append(dict)
            if(i==5):
                sire = (tds[0].text)
            if(i==7):
                dict = {
            'sire' : sire,
            'name' : tds[0].text,
            'mares' : tds[1].text,
            'foals' : tds[2].text,
            'starters' : tds[3].text,
            'winners' :  tds[4].text,
            'BW (%)' : tds[5].text,
            'earnings' : tds[6].text,
            'ael' : tds[7].text,
            }   
                #print(dict)
                dictlist.append(dict)
            if(i==9):
                sire = (tds[0].text)
            if(i==11):
                dict = {
                'sire' : sire,
                'mares' : tds[1].text,
                'foals' : tds[2].text,
                'starters' : tds[3].text,
                'winners' :  tds[4].text,
                'BW (%)' : tds[5].text,
                'earnings' : tds[6].text,
                'ael' : tds[7].text,
                }   
                #print(dict)
                dictlist.append(dict)
    return(dictlist)
def get_horses(racelist):
    for race in racelist:
        horselist = []
        #http://www.equibase.com/static/entry/
        url = race['URL']
        #print(url)
        try:
            reqhor = requests.get(url)
        except:
            time.sleep(6)
            reqhor = requests.get(url)
        supa = bs.BeautifulSoup(reqhor.text, 'lxml')
        for tr in supa.find_all('tr'):
            tds = tr.find_all('td')
        #print(type(tds))
            if(len(tds)==8 or len(tds)==9):
                #print(tds)
                horsename = tds[2].text.strip(' \t\n\r').strip()[:-5].replace(" ", "%20")
                #print(horsename)
                print("itsthis")
                horseurl = 'http://www.equineline.com/Free5XPedigreeSearchResults.cfm?horse_name=' + horsename + '&page_state=LIST_HITS&foaling_year=&dam_name=&include_sire_line=Y'
                print(horseurl)
                try:
                    horsereq = requests.get(horseurl,headers=headers)
                except:
                    time.sleep(6)
                    horsereq = requests.get(horseurl,headers=headers)
                soup = bs.BeautifulSoup(horsereq.text, 'lxml')
                #print(soup)
                try:
                    horsrl = soup.find('a').get('href')
                except:
                    print("Captcha error")
                    time.sleep(6)
                    time.sleep(6)
                    horsereq = requests.get(horseurl,headers=headers)
                    soup = bs.BeautifulSoup(horsereq.text, 'lxml') 
                try:
                    horsrl = soup.find('a').get('href')
                except:
                    print("-- MENJAJ --")
                    time.sleep(12)
                    horsereq = requests.get(horseurl,headers=headers)
                    soup = bs.BeautifulSoup(horsereq.text, 'lxml') 
                    try:
                        horsrl = soup.find('a').get('href')
                    except:
                        print("-- MENJAJ --")
                        time.sleep(12)
                        horsereq = requests.get(horseurl,headers=headers)
                        soup = bs.BeautifulSoup(horsereq.text, 'lxml')
                url = 'http://www.equineline.com/' + horsrl
                start = url.find('reference_number=')
                end = url.find('&registry')
                refnum = url[start+17:end]
                print(refnum)
                link = 'http://www.equineline.com/Free5XPedigreeNickingDisplay.cfm?page_state=DISPLAY_REPORT&reference_number=' + refnum
                #print(url)
                #print(link)
                try:
                    maker = requests.get(link,headers=headers)
                except:
                    time.sleep(6)
                    maker = requests.get(link,headers=headers)
                supica = bs.BeautifulSoup(maker.text,'lxml')
                #print(supica)
                table = supica.find('table')
                #print(table)
                #print(type(table))
                if(table is None):
                    time.sleep(6)
                    maker = requests.get(link,headers=headers)
                    supica = bs.BeautifulSoup(maker.text,'lxml')
                    table = supica.find('table')
                    if(table is None):
                        time.sleep(6)
                    maker = requests.get(link,headers=headers)
                    supica = bs.BeautifulSoup(maker.text,'lxml')
                    table = supica.find('table')
                inftab = get_table(table)
                horsedict = {
                        'P#' : tds[0].text.strip(' \t\n\r').replace(" ", ""),
                        'PP' : tds[1].text,
                        'Name' : tds[2].text.strip(' \t\n\r').strip()[:-5],
                        'Jockey': tds[4].text,
                        'Wgt' : tds[5].text,
                        'Trainer' : tds[6].text,
                        'M/L' : tds[7].text,
                        'Info' : inftab,
                }
                horselist.append(horsedict)
        race['Horses'] = horselist
    return racelist


def get_events():
    global date
    r = requests.get('http://www.equibase.com/static/foreign/entry/index.html?SAP=TN#Australia')
    soup = bs.BeautifulSoup(r.text,'lxml')

    tables = soup.find_all('table')

    table = tables[1] #australijskitejbl
    tr = table.find_all('tr')
        #Featured Tracks	Today	Tomorrow	Future	Past
    length = len(tr)
    eventlist = []
    for i in range(1,length,1):
        tds = tr[i].find_all('td')
        #print(tds[1])
        name = tds[0].text
        print(tds[1])
        url = 'http://www.equibase.com' + tds[1].find('a').get('href')
        date = tds[1].find('a').text
        if(date==''):
            print("No event today at " + name)
        else:
            print(url)
            #url = 'http://www.equibase.com' + tds[1].find('a').get('href')
            events = {
                'date' : date,
                'name' : name,
                'url' : url,
            }
            eventlist.append(events)
    print(eventlist)
    get_races(eventlist)

def get_races(eventlist):
    for race in eventlist:
        global date
        url = race['url']
        date = race['date']
        try:
            r = requests.get(url)
        except:
            time.sleep(6)
            r = requests.get(url)
        racelist = []
        soup = bs.BeautifulSoup(r.text,'lxml')
        for tr in soup.find_all('table'):
            tds = tr.find_all('td')
            length = len(tds)
            for i in range(0,length,7):
                #print(tds[i])
                #print(tds)
                x = tds[2+i].text.strip(' \t\n\r')
            # print("X = " + x)
                #print(dir(x))
            # x = str(x)
                #print(type(x))
                x = x.replace(" ", "")
               # print(tds[0])
                url = tds[0+i].find('a')
                #print(url)
                url = 'http://www.equibase.com' + url.get('href')
                tabledic = {
                    'Race: ' : tds[0+i].text,
                    'URL' : url,
                    'Purse' : tds[1+i].text,
                    'Race Type' : x,
                    'Distance' : tds[3+i].text,
                    'Surface' : tds[4+i].text,
                    'Starters' : tds[5+i].text,
                    'Est. Post' : tds[6+i].text,
                    'Horses' : [],
                }
                #print(type(tabledic))
                racelist.append(tabledic)
        race['races'] = get_horses(racelist)
    jsonero = json.dumps(eventlist)
    print("DATE:", date) #datum
    o = Country('2','Australia',jsonero,date) #datum
    o.save()
    
    noder = requests.post('replaceme.com', json=jsonero)
    #jsonero = json.dumps(eventlist)
    #print(jsonero)
    #f = open('racehelpme.json', 'w')
    #f.write(jsonero)
    #f.close()
                #horses['Horses'] = get_horses(horses)

    
#get_events()

while(1):
    #r = requests.get('https://www.equibase.com/static/entry/index.html')
    #soup = bs.BeautifulSoup(r.text,'lxml')
    aa = Country.objects.get(id=2)
    dated = aa.date
    try:
        r = requests.get('http://www.equibase.com/static/foreign/entry/index.html?SAP=TN#Australia')
    except:
        time.sleep(6)
        r = requests.get('http://www.equibase.com/static/foreign/entry/index.html?SAP=TN#Australia')
    soup = bs.BeautifulSoup(r.text,'lxml')
    #print(soup)
    tables = soup.find_all('table')

    table = tables[1] #australijskitejbl
    tr = table.find_all('tr')
    #Featured Tracks	Today	Tomorrow	Future	Past
    length = len(tr)
    eventlist = []
    for i in range(1,length,1):
        tds = tr[i].find_all('td')
        #print(tds[1])
        name = tds[0].text
        print(tds[1])
        url = 'http://www.equibase.com' + tds[1].find('a').get('href')
        date = tds[1].find('a').text
        if(date==''):
            print("No event today at " + name)
        else:
            print(url)
            #url = 'http://www.equibase.com' + tds[1].find('a').get('href')
            events = {
                'date' : date,
                'name' : name,
                'url' : url,
            }
            eventlist.append(events)
    baba = eventlist[0]['date']
    if(dated==baba): 
        print("No new races for date ", dated) #proverava ako je dd jednak dd u u bazi ako jeste spava, ako nije zove event
        print("\nSleeping for 20 minutes")
        time.sleep(1200)
        continue 
    else:
        print("New race! Scraping.")
        get_events()

