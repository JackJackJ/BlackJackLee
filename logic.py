import json
import urllib.request

data = None
usr = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
def newGame():
    global data
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1',
    headers = {
        'User-Agent': usr
        }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    print(data)


def reshuffle():
    global data
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/shuffle/',
    headers = {
        'User-Agent': usr
    }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())

def draw():
    global data
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/draw',
    headers = {
        'User-Agent': usr
    }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    card = data['cards'][0]['code']
    return card
def hit(playerName):
    global data
    card = draw()
    print(card)
    output = card
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/pile/' + playerName + '/add/?cards='+card,
    headers = {
        'User-Agent': usr
    }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    print(data)
    return output
def dealer():
    global data
    card_list = []
    while score('dealer')<17:
        req = urllib.request.Request(
        'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/draw/?count=1',
        headers = {
            'User-Agent': usr
        }
        )
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
        card = data['cards'][0]['code']
        card_list.append(card)
        req = urllib.request.Request(
        'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/pile/dealer/add/?cards='+card,
        headers = {
            'User-Agent': usr
        }
        )
        response = urllib.request.urlopen(req)
        data = json.loads(response.read())
    return card_list
def initDealer():
    global data
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/draw/?count=1',
    headers = {
        'User-Agent': usr
    }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    card = data['cards'][0]['code']
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/pile/dealer/add/?cards='+card,
    headers = {
        'User-Agent': usr
    }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    return card
def score(playerName):
    global data
    sum = 0
    print(data['deck_id'])
    req = urllib.request.Request(
    'https://deckofcardsapi.com/api/deck/' + data['deck_id'] + '/pile/' + playerName + '/list/',
    headers = {
        'User-Agent': usr
    }
    )
    response = urllib.request.urlopen(req)
    data = json.loads(response.read())
    print(data)
    for i in data['piles'][playerName]['cards']:
        if(i['value'] == "ACE" and sum == 10):
            sum = 21
        elif((i['value'] == "KING" or i['value'] == "QUEEN" or i['value'] == "JACK") and sum == 1):
            sum = 21
        elif(i['value'] == "KING" or i['value'] == "QUEEN" or i['value'] == "JACK"):
            sum += 10
        elif(i['value'] == "ACE"):
            sum += 1
        else:
            sum += int(i['value'])
    return sum