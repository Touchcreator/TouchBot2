from MeowerBot import Bot
import requests
import json
import random
import keepalive

bot = Bot()

testing = False

jobs = ["You saw some cash spawn in your house, it was ", "You worked so hard and made ", "After your long day at you you made ", "Your cousin gave you ", "Your mom gave you ", "You found some cash laying on the floor, after counting it, it was "]

def quoteget():
  response = requests.get('https://api.quotable.io/random')
  json_data = json.loads(response.text)
  quote = '"' + json_data['content'] + '"' + " -" + json_data['author']
  return quote


def give(user, amount):
  openaccount(user)
  with open("data.json", "r") as f:
    userdata = json.load(f)
  userdata[user]["cash"] += amount
  with open("data.json", "w") as f:
    json.dump(userdata, f, indent=4)

def set(user, amount):
  openaccount(user)
  with open("data.json", "r") as f:
    userdata = json.load(f)
  userdata[user]["cash"] = amount
  with open("data.json", "w") as f:
    json.dump(userdata, f, indent=4)


def openaccount(user):
  with open("data.json", "r") as f:
    users = json.load(f)

  if str(user) in users:
    return False
  else:
    users[str(user)] = {}
    users[str(user)]["cash"] = 0

  with open("data.json", "w") as f:
    json.dump(users, f, indent=4)
  return True


@bot.command(args=0, aname="quote")
def quote(ctx):
  ctx.send_msg(quoteget())


@bot.command(args=0, aname="balance")
def accopen(ctx, user=None):
  openaccount(ctx.user.username)
  if user == None:
    with open("data.json", "r") as f:
      userdata = json.load(f)
    ctx.send_msg(ctx.user.username + "'s Balance:\n" + "Cash: " +
               str(userdata[ctx.user.username]["cash"]))
  else:
    openaccount(user)
    with open("data.json", "r") as f:
      userdata = json.load(f)
    ctx.send_msg(user + "'s Balance:\n" + "Cash: " +
               str(userdata[user]["cash"]))


@bot.command(args=2, aname="send")
def send(ctx, recipient, value):
  openaccount(recipient)
  with open("data.json", "r") as f:
    userdata = json.load(f)
  if userdata[ctx.user.username]["cash"] >= int(value):
    userdata[recipient]["cash"] = userdata[recipient]["cash"] + int(value)
    userdata[ctx.user.username]["cash"] -= int(value)
  else:
    ctx.send_msg("Card declined 💀\nWork and get more cash.")
  with open("data.json", "w") as f:
    json.dump(userdata, f, indent=4)


@bot.command(args=1, aname="work")
def work(ctx):
  openaccount(ctx.user.username)
  earned = random.randint(1, 20)
  ctx.send_msg(random.choice(jobs) + str(earned) + " cash.")
  give(ctx.user.username, earned)

@bot.command(args=2, aname="setvalue")
def setvalue(ctx, user, value):
  if ctx.user.username == 'Touchcreator':
    set(user, int(value))
    ctx.send_msg("Set " + user + "'s amount to " + str(value) + ".")

def login(bot=bot):
  if testing == True:
    bot.send_msg("Hello! I'm TouchBot. Learn the commands yourself idiot.", to="a1972a25-d698-404a-a4a1-d10c2599a4ba")
  else:
    bot.send_msg("Hello! I'm TouchBot2. Learn the commands yourself idiot.", to="home")

keepalive.keep_alive()
bot.callback(login, cbid="login")
bot.run("TouchBot2", "password")
