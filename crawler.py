from bs4 import BeautifulSoup
import requests
import csv

def updateData() -> str:
    file_name = 'data/data.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=';')
        main_dom = 'https://dota2.fandom.com'
        strt_url = 'https://dota2.fandom.com/wiki/Lore'
        page = requests.get(strt_url)
        html = BeautifulSoup(page.text)
        for j in html.find('table', {'class': 'notanavbox'}).find_all('tr'):
            cols = j.find_all('td')
            if len(cols) == 2:
                type = cols[0].text
                for li in cols[1].find_all('li'):
                    data = [type]
                    if type == 'Heroes':
                        data.append(li.text)
                        data.append(main_dom + li.find("a")["href"])
                        data.append((main_dom + li.find("a")["href"]).replace("/Lore", ""))
                        print(f'Found: {data[0]} ---> {data[1]} ---> {data[2]} ---> Abilities are here: {data[3]}')
                    else:
                        data.append(li.text)
                        data.append(main_dom + li.find("a")["href"])
                        print(f'Found: {data[0]} ---> {data[1]} ---> {data[2]}')
                    csv_writer.writerow(data)

    return file_name
