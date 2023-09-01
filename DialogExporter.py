import json

ex = '''
Scene: A stormy night, with crashing waves and howling winds. Kunkka stands on the deck of his ghostly ship, while Dark Willow appears from the shadows, standing opposite him.

Kunkka: (coldly) Well, well... if it isn't the infamous Mireska Sunbreeze. I've been searching for you.

Dark Willow: (smirking) Oh Admiral, how nice to see you again. Still bitter about losing your precious fleet?

Kunkka: Bitter? No. Furious? Absolutely. You sabotaged us at the Trembling Isle, didn't you? Your presence was no coincidence.

Dark Willow: (laughs) Sabotage is such a harsh word, Admiral. Let's just say I added a little spice to your battle. After all, it was getting boring watching those demons tear through your ships.

Kunkka: You find amusement in chaos and destruction, don't you? The lives lost that day meant nothing to you?

Dark Willow: Lives lost are merely collateral damage in the pursuit of excitement and power. Besides, who needs a navy when you can have chaos on your side?

Kunkka: Chaos... like summoning Maelrawn? That storm unleashed by Tidehunter... did he truly destroy both fleets because of you?

Dark Willow: (shrugs nonchalantly) Tidehunter may have summoned Maelrawn, but it was his own desire for revenge that brought forth such devastation. Don't blame me for his mistakes.

Kunkka: Mistakes?! Look around us! My once mighty fleet reduced to this ghostly vessel while I continue my eternal hunt for you!

Dark Willow: (mockingly) Oh Admiral... if only you knew what true power feels like. Perhaps one day I'll steal that knowledge away from under your nose as well.

Kunkka clenches his fists tightly and takes a step forward, his anger palpable.

Kunkka: You underestimate me, Dark Willow. I've faced demons and survived the wrath of an abyssal god. I will hunt you down and make you pay for what you've done.

Dark Willow: (laughs softly) Hunt away, Admiral. But remember, I thrive in the shadows and feed off chaos. The chase is what keeps me alive.

With that, Dark Willow disappears into thin air, leaving Kunkka seething with rage as he vows to never rest until he exacts his revenge on her.

Kunkka: You may hide now, Mireska Sunbreeze, but your days of mischief are numbered. I will find you... no matter where you may run.

The storm rages on as Kunkka's ghostly ship continues its eternal search for Dark Willow, their bitter rivalry fueling their never-ending battle.'''

def saveDialog(res: str, chars):

    data = []
    strings = res.split('\n')
    strings = [x for x in strings if x and ':' in x and any(j for j in chars if j in x.split(':')[0])]
    first = strings[0].split(':')[0]
    second = strings[1].split(':')[0]
    strings = [x for x in strings if x and (first in x or second in x)]
    strings = [x.replace('(','*').replace(')','*') for x in strings]
    print(f'Dialog between ---> {first} and {second}:\n')
    print(res)
    with open('dialogs/dialogs.json', 'r', encoding='utf-8') as jsn:
        data = json.load(jsn)
        k = len(data)



    data.append({'id': k, 'dialog': []})
    for i in strings:
        data[k]['dialog'].append({'name':i.split(':')[0], 'response':''.join(i.split(':')[1:]).strip()})

    with open('dialogs/dialogs.json', 'w', encoding='utf-8') as jsn:
        json.dump(data, jsn, indent=1)



