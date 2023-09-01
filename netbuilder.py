import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import json
from pyvis.network import Network
from IPython.display import display, HTML
import community.community_louvain as cm

with open('data/universeInfo.json', 'r', encoding='utf-8') as jsn:
    data = json.load(jsn)

    FIND = "Pudge"

    edges = []

    for theme in data['Universe']:#theme World, Hero etc.
        for item in data['Universe'][theme]:#item here
            if item == FIND:
                if theme == "Heroes":
                    abilki = data['Universe'][theme][item][1]
                    abilities_data = abilki.get('abilities', None)
                    if abilities_data:
                        for i in abilities_data:
                            egde = (i['Ability name'], item)
                            edges.append(egde)


            for ass in data['Universe'][theme][item][0]['Associated']:

                for FINNALY in ass:
                    for i in ass[FINNALY]:
                        if i == FIND or item == FIND:
                            #if (theme == "Heroes" or theme == "Characters" or theme == "Items" or theme == "Places") and (FINNALY == "Heroes" or FINNALY == "Characters" or FINNALY == "Items" or FINNALY == "Places"):
                            if i != item:
                                egde = (i, item)
                                edges.append(egde)

    print(edges)
    print(len(edges))
    G = nx.Graph()


    G.add_edges_from(edges)

    net = Network(width='4000px', height='4000px', bgcolor='#171717', font_color='white')

    scale = 1.09
    node_deg = dict(G.degree)
    node_deg.update((x, 10 + y ** scale) for x, y in node_deg.items())
    nx.set_node_attributes(G, node_deg, 'size')
    cum = cm.best_partition(G)
    nx.set_node_attributes(G, cum, 'group')

#    pos = nx.kamada_kawai_layout(G)
#    plt.figure(figsize=(20,12))
#    nx.draw(G, with_labels=True,pos=pos)
#    plt.show()




    options = '''const options = {
  "physics": {
    "barnesHut": {
      "gravitationalConstant": -3000,
      "centralGravity": 4,
      "springLength": 250,
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


    #net.show_buttons(filter_=['physics'])
    #net.toggle_physics(False)




    net.from_nx(G)

    html = net.generate_html()
    with open("HTMLs/Pudge.html", mode='w', encoding='utf-8') as fp:
        fp.write(html)
    display(HTML(html))
    #net.show('lore.html', notebook=False)