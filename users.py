import json
import user as u

users = []

def reloadJSON():
    users.clear()
    loadJSON()

def loadJSON():
    f = open("users.json")
    data = json.load(f)
    for i in data:
        users.append(u.User(i.get('name'), i.get('emoji'), i.get('trusted')))
    f.close()

def saveJSON():
    json_string = json.dumps([ob.__dict__ for ob in users])
    f = open("users.json", "w")
    f.write(json_string)
    f.close()

def listUsers():
    toReturn = ""
    for u in users:
        toReturn += "Name: " + u.name + " Emoji: " + u.emoji + " trusted: " + str(u.trusted) + "\n"
    toReturn += "Total Users: " + str(len(users))
    return toReturn

def getUser(name):
    for user in users:
        if (user.name == name):
            return user
    return None

def setEmoji(name, emoji):
    # Check if user exists, if not add them
    if (getUser(name) == None):
        # Add
        users.append(u.User(name, emoji, False))
    else:
        for i in range(len(users)):
            if (users[i].name == name):
                users[i].emoji = emoji
    saveJSON()
            
def isTrusted(name):
    for user in users:
        if (user.name == name and user.trusted):
            return True
    return False

