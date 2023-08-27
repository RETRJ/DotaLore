from bs4 import BeautifulSoup
import requests
import re
import json


def getInfoBox(url: str) -> list:
    print(f'NOW AT: {url} !!!')
    page = requests.get(url)
    html = BeautifulSoup(page.text)
    infoBox = html.find('table', {'class': 'infobox'})
    info = []
    for row in infoBox.find_all('tr'):
        cols = row.find_all('td')
        if len(cols) > 1 and cols[0].text.strip() != 'Cosmetics':
            print({cols[0].text.strip(): [elem.text.strip() for elem in cols[1] if elem.text.strip()]})
            # info.append({cols[0].text.strip(): [elem.text for elem in cols[1].find_all('a') if elem.text]})
            info.append({cols[0].text.strip(',. \n\t'): [elem.text.strip(',. \n\t') for elem in cols[1] if
                                                         elem.text.strip(',. \n\t') and not re.search(
                                                             r"\(.*?\)|\[.*?\]", elem.text.strip())]})
    return info


def getAbilitiesDesc(url: str) -> dict:
    print(f'NOW AT: {url} ABILITIES PARSE!!!')
    page = requests.get(url)
    html = BeautifulSoup(page.text)
    abilities = html.find_all('div', {'class': 'ability-background'})
    info = {'abilities': []}
    for abilka in abilities:
        desc = abilka.find('div', {'class': 'ability-description'}).find_all('div')
        info['abilities'].append(
            {'Ability name': abilka.findNext('span').text.strip(), 'Ability type': desc[-2].text[6:],
             'Ability description': desc[-1].text})
    print(json.dumps(info,indent=1))
    return info


# I fucking hate this unstructured data bruh......
def getFuckingLore(url: str, heroName=None) -> list:
    print(f'NOW AT: {url} LORE PARSE!!! KILL ME!!!')
    page = requests.get(url)
    html = BeautifulSoup(page.text)
    allText = html.find('div', {'class': 'mw-parser-output'}).find_all('li', {'class': None})
    allText2 = html.find_all('p')


    if heroName:
        info = {'Name': [], 'Intro': [], 'Lore': []}
        allText3 = html.find('div', {'class': 'mw-parser-output'}).find('div', {
            'style': 'border:1px solid #AAAAAA; padding:15px; text-align:center;'})
        mn = allText3.text.strip().split('\n')
        info['Name'] = mn[:1]
        info['Intro'] = mn[1:]
    else:
        info = {'Lore': []}

    # blyat kto naxyi sostavlyal stryktury... licho v gov... HTML !!775Gr7856KK(M(*&^#(*&NM^oMN%&*DNM$BJ*(OL):P*$&^Dfnbm*(&o^%$DSBNV *(IKOL^&%$DSbN*(OI&^%dsBNHJM(*OE%WGH
    preCollect = []
    for text in allText:
        if not text.find('audio') and not text.find('a', {'class': 'ext-audiobutton'}) and not text.findParent('table',
                                                                                                               {
                                                                                                                   'class': 'notanavbox'}) and not text.findParent(
                'div', {'class': 'mw-references-wrap mw-references-columns'}) and not text.findParent('div', {
            'class': 'mw-references-wrap'}):  # junk DotaLore
            preCollect.append(re.sub(r'\[.*?\]', '', text.text.strip()))
    for text in allText2:
        if not text.find('audio') and not text.find('a', {'class': 'ext-audiobutton'}) and len(
                text.text.strip()) > 20 and not text.findParent('table',
                                                                {'class': 'notanavbox'}) and not text.findParent('div',
                                                                                                                 {
                                                                                                                     'class': 'mw-references-wrap mw-references-columns'}) and not text.findParent(
                'div', {'class': 'mw-references-wrap'}):  # junk DotaLore
            preCollect.append(re.sub(r'\[.*?\]', '', text.text.strip()))

    if heroName:
        cleared = [str for str in preCollect if not str.endswith(heroName)]
        info['Lore'] = cleared
    else:
        info['Lore'] = preCollect

    print(json.dumps(info,indent=1))
    return info


getFuckingLore('https://dota2.fandom.com/wiki/Luna/Dragon%27s_Blood')#DotaLore
