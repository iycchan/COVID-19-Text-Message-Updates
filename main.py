__author__ = "Ian Chan"
__copyright__ = "Copyright 2020, Ian Chan"
__credits__ = ["Ian Chan"]
__license__ = "GPL"
__version__ = "3"
__maintainer__ = "Ian Chan"
__email__ = "me@ian-chan.me"
__status__ = "Production"

import json, requests, time, os
from twilio.rest import Client
import gc
import configparser


config = configparser.ConfigParser()
if os.path.isfile('config.ini'):
    pass
else:
    config['Settings'] = {'Twilio SID': '',
                      'Authentication Token': '',
                      'Phone Numbers': '+18005555551,+18005555552',
                      'From Number' : '+8005555555',
                      'Country': 'US'}
    
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    
    print("Configuration file created")
    print("Edit configuration file then run again")
    print("Press ENTER key to exit")
    input()
    exit()

config.read('config.ini')

settings = config['Settings']
sid = settings.get('Twilio SID')
auth = settings.get('Authentication Token')
fromNumber = settings.get('From Number')
phoneNumbers = settings.get('Phone Numbers')
phoneNumbers = phoneNumbers.split(',')
phoneNumbers = [x.strip(' ') for x in phoneNumbers]
country = settings.get('Country')
country = country.lower()

def tryAndExcept():
    try:
        print("Ready")
        getData()
    except:
        print("Error, restarting")
        tryAndExcept()

def getData():
    gc.collect()
    global oldData
    try:
        with open(country, "r") as rawoldData:
            oldData = rawoldData.read()
        pass
    except:
        print("No previous data")
        oldData = 'none'
    print("Attempting to get data...")
    url = 'http://corona.lmao.ninja/countries/' + country
    r = requests.get(url)
    with open(country, 'wb') as outfile:
        outfile.write(r.content)
        print("Got data!")
    processData()
    
def processData():
    print("Processing data...")
    with open(country, "r") as dataFile:
        data = dataFile.read()
        formattedData = json.loads(str(data))
    compareData(oldData, data, formattedData)
        
def compareData(oldData, newData, data):
    if oldData == newData:
        print("Nothing changed")
        time.sleep(300)
        print("Passing")
        pass
    else:
        sendMessage(data)
        
def sendMessage(data):
    account_sid = sid
    auth_token = auth
    totalCases = data['cases']
    todayCases = data['todayCases']
    totalDeath = data['deaths']
    todayDeath = data['todayDeaths']
    recovered = data['recovered']
    critical = data['critical']
    print("Sending messages...")
    client = Client(account_sid, auth_token)
    for currentNumber in phoneNumbers:
        print("Sending message to: "+currentNumber)
        message = client.messages.create(
        to=currentNumber,
        from_= fromNumber,
        body="COVID-19 Updates\n\nTotal cases: "+str(totalCases)+"\nCases today: "+str(todayCases)+"\nRecovered: "+str(recovered)+"\nTotal deaths: "+str(totalDeath)+"\nDeaths today: "+str(todayDeath))
        print(message.sid)
    pass 
while True:
    tryAndExcept()