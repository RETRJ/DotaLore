import crawler
import parser
import json
import csv

def autoParseWiki(needUpdate=False):
    data_file = 'data/data.csv'
    if needUpdate:
        data_file = crawler.updateData()
    with (open(data_file, 'r', newline='', encoding='utf-8') as csvfile):
        csv_reader = csv.reader(csvfile, delimiter=';')
        universeData = {'Universe':{}}

        for row in csv_reader:

            parsed = [{'Associated': parser.getInfoBox(row[2])}]

            if row[0] == 'Heroes' and row[2].endswith('/Lore'):
                parsed.append(parser.getAbilitiesDesc(row[3]))
                parsed.append(parser.getFuckingLore(row[2], row[1]))
            else:
                parsed.append(parser.getFuckingLore(row[2]))
            print(parsed)
            if row[0] not in universeData['Universe']:
                universeData['Universe'][row[0]] = {}
            universeData['Universe'][row[0]].update({row[1] : parsed})
        with open('data/universeInfo.json', 'w') as jsn:
            json.dump(universeData, jsn, indent=1)

autoParseWiki()