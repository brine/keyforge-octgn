AttackerColor = "#FF0000"
DefenderColor = "#00FF00"
DamageMarker = ("Damage", "bbc64689-67f3-4378-b2f0-d22a3829459c")
AemberMarker = ("Æmber", "6f12fd99-6f04-4483-9786-44ff654c8a25")
Houses = ["Mars", "Dis", "Brobnar", "Sanctum", "Untamed", "Shadows", "Logos"]

BlueKeyToken = "e6fb13af-e30d-409b-8f6c-b4bfb13aea61"
YellowKeyToken = "33cafd56-4124-40dc-acec-8393567ec824"
RedKeyToken = "c13977a0-55d7-4d58-8c00-045794821556"

diesides = 6

def initializeGame():
    mute()
    #### LOAD UPDATES
    v1, v2, v3, v4 = gameVersion.split('.')  ## split apart the game's version number
    v1 = int(v1) * 1000000
    v2 = int(v2) * 10000
    v3 = int(v3) * 100
    v4 = int(v4)
    currentVersion = v1 + v2 + v3 + v4  ## An integer interpretation of the version number, for comparisons later
    lastVersion = getSetting("lastVersion", convertToString(currentVersion - 1))  ## -1 is for players experiencing the system for the first time
    lastVersion = int(lastVersion)
    for log in sorted(changelog):  ## Sort the dictionary numerically
        if lastVersion < log:  ## Trigger a changelog for each update they haven't seen yet.
            stringVersion, date, text = changelog[log]
            updates = '\n-'.join(text)
            confirm("What's new in {} ({}):\n-{}".format(stringVersion, date, updates))
    setSetting("lastVersion", convertToString(currentVersion))  ## Store's the current version to a setting

def generateDeck(group, x = 0, y = 0):
    mute()
    houseList = list(Houses)
    selectedHouses = []
    rnds = list(rndArray(1,100, 36))
    for x in range(3):
        house = randomItem(houseList, True)
        selectedHouses.append(house)
        rares = queryCard({"House": house, "Rarity": "Rare"})
        uncommons = queryCard({"House": house, "Rarity": "Uncommon"})
        commons = queryCard({"House": house, "Rarity": "Common"})
        for x in range(12):
            i = rnds.pop(0)
            if i < 10:
                me.Deck.create(randomItem(rares), 1)
            elif i < 35:
                me.Deck.create(randomItem(uncommons), 1)
            else:
                me.Deck.create(randomItem(commons), 1)
    notify("{} generated a new Deck ({} {} {}).".format(me, selectedHouses[0], selectedHouses[1], selectedHouses[2]))
                

def randomItem(list, pop = False):
    i = rnd(1, len(list))
    if pop:
        return list.pop(i - 1)
    else:
        return list[i - 1]

def chooseHouse(group, x = 0, y = 0):
    mute()
    num = askChoice("Choose a House:", Houses)
    if num == 0: return
    notify("{} chooses House {}.".format(Houses[num - 1]))

def setDie(group, x = 0, y = 0):
    mute()
    global diesides
    num = askInteger("How many sides?\n\nFor Coin, enter 2", diesides)
    if num != None and num > 0:
        diesides = num
        dieFunct(diesides)

def rollDie(group, x = 0, y = 0):
    mute()
    global diesides
    dieFunct(diesides)

def dieFunct(num):
    if num == 2:
        n = rnd(1, 2)
        if n == 1:
            notify("{} rolls 1 (HEADS) on a 2-sided die.".format(me))
        else:
            notify("{} rolls 2 (TAILS) on a 2-sided die.".format(me))
    else:
        n = rnd(1, num)
        notify("{} rolls {} on a {}-sided die.".format(me, n, num))


def createKeys(group, x = 0, y = 0):
    mute()
    tableCards = [card.model for card in table if card.owner == me]
    for title in queryCard({"Type": "Key"}):
        if title not in tableCards:
            titleCard = table.create(title, x, y, 1)
            x += 10
            if titleCard.isInverted():
                y -= 10
            else:
                y += 10
    notify("{} loaded their Keys.".format(me))

def readyExhaust(card, x = 0, y = 0):
    mute()
    if card.orientation == Rot0:
        card.orientation = Rot90
        notify("{} exhausts {}.".format(me, card))
    else:
        card.orientation = Rot0
        notify("{} readies {}.".format(me, card))

def revealHide(card, x = 0, y = 0):
    mute()
    if card.isFaceUp:
        card.isFaceUp = False
        notify("{} hides {}.".format(me, card))
    else:
        card.isFaceUp = True
        notify("{} reveals {}.".format(me, card))

def reap(card, x = 0, y = 0):
    mute()
    if card.orientation == Rot0:
        card.orientation = Rot90
        me.Æmber += 1
        notify("{}'s {} reaps.".format(me, card))

def action(card, x = 0, y = 0):
    mute()
    if card.orientation == Rot0:
        card.orientation = Rot90
        notify("{}'s {} uses its action.".format(me, card))

def fight(card, x = 0, y = 0):
    mute()
    if card.orientation == Rot0:
        card.orientation = Rot90
        targets = [c for c in table if c.targetedBy == me]
        if len(targets) == 1:
            target = targets[0]
            card.arrow(target)
            notify("{}'s {} fights {}'s {}.".format(card.controller, card, target.controller, target))
        else:
            notify("{}'s {} fights.".format(card.controller, card))

def addAember(card, x = 0, y = 0):
    mute()
    card.markers[AemberMarker] += 1
    notify("{} adds 1 Æmber on {}.".format(me, card))
    
def removeAember(card, x = 0, y = 0):
    mute()
    card.markers[AemberMarker] -= 1
    notify("{} removes 1 Æmber from {}.".format(me, card))

def clearAember(card, x = 0, y = 0):
    mute()
    card.markers[AemberMarker] = 0
    notify("{} removes all Æmber from {}.".format(me, card))
    
def addDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] += 1
    notify("{} adds 1 Damage on {}.".format(me, card))
    
def removeDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] -= 1
    notify("{} removes 1 Damage from {}.".format(me, card))
    
def clearDamage(card, x = 0, y = 0):
    mute()
    card.markers[DamageMarker] = 0
    notify("{} removes all Damage from {}.".format(me, card))

def readyAll(group, x = 0, y = 0):
    mute()
    for c in table:
        if c.controller == me and c.orientation != Rot0:
            c.orientation = Rot0
    notify("{} readies all their cards.".format(me))

def forgeKey(card, x = 0, y = 0):
    mute()
    if "full" in card.alternates:
        if card.alternate == "":
            card.alternate = "full"
            card.markers[AemberMarker] = 0
            notify("{} forges {}.".format(me, card))
        else:
            card.alternate = ""
            notify("{} unforges {}.".format(me, card))

def discard(card, x = 0, y = 0):
    mute()
    notify("{} discards {} from {}.".format(me, card, card.group.name))
    card.moveTo(card.owner.piles["Discard Pile"])

def archive(card, x = 0, y = 0):
    mute()
    notify("{} archives {} from {}.".format(me, card, card.group.name))
    card.moveTo(card.owner.piles["Archives"])

def draw(group, x = 0, y = 0):
    mute()
    drawCard()
    notify("{} draws a card.".format(me))

def drawMany(group, x = 0, y = 0):
    mute()
    if len(group) == 0:
        return
    count = askInteger("Draw how many cards?", 7)
    if count == None or count == 0:
        return
    for card in range(count):
        drawCard()
    notify("{} draws {} card{}.".format(me, count, pluralize(count)))

def drawCard():
    mute()
    if len(me.Deck) == 0:
        for c in me.piles["Discard Pile"]:
            c.moveTo(c.owner.Deck)
        me.Deck.shuffle()
        rnd(1,1)
    if len(me.deck) == 0: return
    card = me.deck[0]
    card.moveTo(card.owner.hand)

def shuffle(group, x = 0, y = 0, silence = False):
    mute()
    for card in group:
        if card.isFaceUp:
            card.isFaceUp = False
    group.shuffle()
    if silence == False:
        notify("{} shuffled their {}".format(me, group.name))

def mulligan(group, x = 0, y = 0):
    mute()
    newCount = len(group)
    if newCount < 0:
        return
    if not confirm("Confirm Mulligan?"):
        return
    notify("{} mulligans.".format(me))
    for card in group:
        card.moveTo(card.owner.Deck)
    shuffle(me.Deck, silence = True)
    for card in me.Deck.top(newCount - 1):
        card.moveTo(card.owner.hand)
        
def randomDiscard(group, x = 0, y = 0):
    mute()
    card = group.random()
    if card == None:
        return
    card.moveTo(card.owner.piles["Discard Pile"])
    notify("{} randomly discards {} from {}.".format(me, card, group.name))
    
def drawArchives(group, x = 0, y = 0):
    mute()
    if len(group) == 0: return
    for card in group:
        card.moveTo(card.owner.hand)
    notify("{} draws their Archives.".format(me))

def viewGroup(group, x = 0, y = 0):
    group.lookAt(-1)

def pluralize(num):
   if num == 1:
       return ""
   else:
       return "s"