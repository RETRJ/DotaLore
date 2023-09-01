import networkx as nx
import json
import csv
from pyvis.network import Network
from IPython.display import display, HTML
import community.community_louvain as cm

def getTopicsFor(name: str, deep=False) -> set:
    if deep:
        with open('data/universeInfo.json', 'r', encoding='utf-8') as jsn:
            data = json.load(jsn)

            edges = []

            layer1 = set([name])
            layer2 = set([name])



            for theme in data['Universe']:#theme World, Hero etc.
                for item in data['Universe'][theme]:#item here
                    if item == name:
                        if theme == "Heroes":
                            abilki = data['Universe'][theme][item][1]
                            abilities_data = abilki.get('abilities', None)
                            if abilities_data:
                                for i in abilities_data:
                                    layer1.add(i['Ability name'])
                                    egde = (i['Ability name'], item)
                                    edges.append(egde)



                    for ass in data['Universe'][theme][item][0]['Associated']:

                        for FINNALY in ass:
                            for i in ass[FINNALY]:
                                if i == name or item == name:
                                    if i != item:
                                        layer1.add(i)
                                        egde = (i, item)
                                        edges.append(egde)

            for theme in data['Universe']:#theme World, Hero etc.
                for item in data['Universe'][theme]:#item here



                    for ass in data['Universe'][theme][item][0]['Associated']:

                        for FINNALY in ass:
                            for i in ass[FINNALY]:
                                if i in layer1 or item in layer1:
                                    if i != item:
                                        layer2.add(i)
                                        egde = (i, item)
                                        edges.append(egde)


            #print(layer2)
            #print(len(layer2))
            #print(edges)

            #print(len(edges))
            return layer2
            G = nx.Graph()

            G.add_edges_from(edges)

            net = Network(width='1600px', height='1600px', bgcolor='#171717', font_color='white')

            scale = 1.09
            node_deg = dict(G.degree)
            node_deg.update((x, 10 + y ** scale + (50 * (x == name))) for x, y in node_deg.items())
            nx.set_node_attributes(G, node_deg, 'size')
            cum = cm.best_partition(G)
            nx.set_node_attributes(G, cum, 'group')


            options = '''const options = {
          "physics": {
            "barnesHut": {
              "gravitationalConstant": -8000,
              "centralGravity": 4,
              "springLength": 500,
              "springConstant": 0.002,
              "damping": 0.15,
              "avoidOverlap": 0.2
            },
            "maxVelocity": 70,
            "minVelocity": 0.75
          }
        }
            '''
            net.set_options(options=options)

            net.from_nx(G)

            html = net.generate_html()
            with open(f"HTMLs/items/{name}.html", mode='w', encoding='utf-8') as fp:
                fp.write(html)
            display(HTML(html))
            #net.show('lore.html', notebook=False)
            return layer2
    else:
        with open('data/universeInfo.json', 'r', encoding='utf-8') as jsn:
            data = json.load(jsn)

            edges = []

            layer1 = set([name])

            for theme in data['Universe']:  # theme World, Hero etc.
                for item in data['Universe'][theme]:  # item here
                    if item == name:
                        if theme == "Heroes":
                            abilki = data['Universe'][theme][item][1]
                            abilities_data = abilki.get('abilities', None)
                            if abilities_data:
                                for i in abilities_data:
                                    layer1.add(i['Ability name'])
                                    egde = (i['Ability name'], item)
                                    edges.append(egde)

                    for ass in data['Universe'][theme][item][0]['Associated']:

                        for FINNALY in ass:
                            for i in ass[FINNALY]:
                                if i == name or item == name:
                                    if i != item:
                                        layer1.add(i)
                                        egde = (i, item)
                                        edges.append(egde)
        return layer1

#print(getTopicsFor('Dark Willow'))

def getStr(name: str, vip: bool) -> str:
    ans = ""
    tmp = ""

    with open('data/universeInfo.json', 'r', encoding='utf-8') as jsn:
        data = json.load(jsn)
        for theme in data['Universe']:#theme World, Hero etc.
            for item in data['Universe'][theme]:#item here
                if item == name:
                    if theme == "Heroes" and len(data['Universe'][theme][item]) == 3:
                        if vip:
                            if len(data['Universe'][theme][item][2]['Name'][0].split(',')) > 1:
                                ans += f"\"{data['Universe'][theme][item][2]['Name'][0].split(',')[0].strip()}\" also know as \"{data['Universe'][theme][item][2]['Name'][0].split(',')[1].strip()}\".\n"
                            else:
                                ans += f"{data['Universe'][theme][item][2]['Name'][0]}:\n"

                            ans += f"{name}'s Introduction:\n\t{data['Universe'][theme][item][2]['Intro'][0]}\n"

                            if data['Universe'][theme][item][2]['Lore'] is not None:
                                ans += 'Lore:\n'
                            for i in data['Universe'][theme][item][2]['Lore']:
                                tmp += f"\t{i}\n"

                            abilki = data['Universe'][theme][item][1]
                            abilities_data = abilki.get('abilities', None)
                            if abilities_data:
                                tmp+=f"{name}'s Abilities and Skills:\n"
                                for i in abilities_data:
                                    tmp += f"\t{i['Ability name']}: {i['Ability description']}\n"
                    else:
                        ans+=f"{name}:\n"
                        ans += 'Lore:\n'
                        for i in data['Universe'][theme][item][1]['Lore']:
                            tmp += f"\t{i}\n"


                #for ass in data['Universe'][theme][item][0]['Associated']:
#
                #    for FINNALY in ass:
                #        for i in ass[FINNALY]:
                #            if i == name or item == name:
                #                if i != item:
                #                    ans += f"{name}'s introduction: {}"


        return ans+tmp


getStr("Shadow Shaman", True)
#data_file = 'data/data.csv'
#with (open(data_file, 'r', newline='', encoding='utf-8') as csvfile):
#    csv_reader = csv.reader(csvfile, delimiter=';')
#    maxName = ""
#    max = -1
#    for row in csv_reader:
#       data = getTopicsFor(row[1])
#       if len(data) > max:
#           max = len(data)
#           maxName = row[1]
#           print(f'NEW MAX: {maxName} --> {max}')
#