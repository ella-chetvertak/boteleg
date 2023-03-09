import telebot
from telebot import types #
from pathlib import Path
import time
import math
import random
import os

import sqlite3

# MAIN

BOT_TOKEN = "5868080587:AAGoWmJF5iWMGoxMEi-oI7cYXN7LwE68POQ"
print (BOT_TOKEN)
bot = telebot.TeleBot(BOT_TOKEN)

tconv = lambda x: time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(x))

def write (user, message):
  federal = open("Federal.txt", "r+")
  federal.seek(0, 2)
  federal.write(user + "  " + message + "\n")
  federal.close()

# DATABASE

conn = sqlite3.connect('db/teleBotDatabase.db', check_same_thread=False)
cursor = conn.cursor()

def db_table_val(user_id: int, user_name: str, user_surname: str, username: str):
    cursor.execute(f"INSERT INTO `userI` VALUES (NULL, ?, ?, ?, ?)", (user_id, user_name, user_surname, username))
    conn.commit()
    cursor.close()

@bot.message_handler(commands=['register'])
def get_text_messages(message):
  bot.send_message(message.from_user.id, "Ваше ім`я було додано до бази даних")

  us_id = message.from_user.id
  us_name = message.from_user.first_name
  us_sname = message.from_user.last_name
  username = message.from_user.username
		
  db_table_val(user_id=us_id, user_name=us_name, user_surname=us_sname, username=username)

# START, HELP

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")

# WHO

@bot.message_handler(commands=['who'])
def send_who(message):
    user_man = message.from_user.username + ' ' + message.from_user.first_name + ' ' + str (tconv(message.date))
    bot.reply_to(message, user_man)
    write (user_man, "/who")#поч здесь подчеркнуто красним?

# DICE
  
class Dice ():
  
  def diceRand(self):
    self.diceStr = ''
    self.combination = []
    self.pok = 0
    self.sq = 0
    self.fh = 0
    self.thr = 0
    self.twoP = 0
    self.oneP = 0
    self.str = 0
    self.bust = 0
    self.countedBal = 0
    for i in range(1, 6):
      a = random.randint(1, 6)
      self.diceStr += str(a)
      self.combination.append(a)
      if i != 5: self.diceStr += ', '
    Dice.check (self)
    print(self.combination)
    print("Poker: ", self.pok)
    print("Square", self.sq)
    print("Full House: ", self.fh)
    print("Three: ", self.thr)
    print("Two pairs: ", self.twoP)
    print("One pair: ", self.oneP)
    print("Straight: ", self.str)
    print("Bust: ", self.bust)
    aim = None

    if self.pok != 0: aim = "Poker"
    elif self.sq != 0: aim = "Square"
    elif self.fh != 0: aim = "Full House"
    elif self.thr != 0: aim = "Three"
    elif self.twoP != 0: aim = "Two pairs"
    elif self.oneP != 0: aim = "One pair"
    elif self.str != 0: aim = "Straight"
    elif self.bust != 0: aim = "Bust"
    
    return ([self.diceStr, aim, self.countedBal])

  
  def check (self):
    if len(set(self.combination)) == 1:
        self.pok += 1
        self.countedBal = 50
    helpArr = []
    helpArr2 = []
    helpArrK = []
    for k in range(7):
        count = self.combination.count(k)
        if count == 4:
            self.sq += 1
            helpArr2.append(count)
            self.countedBal = k*4*2
        if count == 3:
            helpArr.append(count)
            helpArrK.append(k)
        if count == 2:
            helpArr.append(count)
            helpArrK.append(k)
    if len(helpArr) == 2 and len(set(helpArr)) != 1:
        self.fh += 1
        self.countedBal = (helpArrK[1]*2 + helpArrK[0]*3)*2
    if len(set(helpArr)) == 1 and helpArr[0] == 3:
        self.thr += 1
        self.countedBal = helpArrK[0]*3
    if len(set(helpArr)) == 1 and len(helpArr) == 2:
        self.twoP += 1
        self.countedBal = helpArrK[0]*2 + helpArrK[1]*2
    if len(helpArr) == 1 and helpArr[0] != 3:
        self.oneP += 1
        self.countedBal = helpArrK[0]*2

    arrStraight1 = [1, 2, 3, 4, 5]
    arrStraight2 = [2, 3, 4, 5, 6]
    if self.combination == arrStraight1 or self.combination == arrStraight2:
      self.str += 1
      self.countedBal = 40

    if self.combination != arrStraight1 and self.combination != arrStraight2 and len(helpArr) == 0 and len(helpArr2) == 0:
        self.bust += 1

i = 0

@bot.message_handler(commands=['dice'])
def dicer(message):
  user_man = message.from_user.username + ' ' + message.from_user.first_name + ' ' + str (tconv(message.date))
  diceResult1 = Dice.diceRand(message)
  diceFinal1 = f"{str(diceResult1[0])} \n{str(diceResult1[1])} \n{str(diceResult1[2])}"
  bot.reply_to(message, diceFinal1)

  time.sleep(0.5)

  diceResult2 = Dice.diceRand(message)
  diceFinal2 = f"bot throws \n{str(diceResult2[0])} \n{str(diceResult2[1])} \n{str(diceResult2[2])}"
  bot.send_message(message.chat.id, diceFinal2)

  won = f"game ended \nYou {diceResult1[2]} \nBot {str(diceResult2[2])} \n" + "You won!" if diceResult1[2] > diceResult2[2] else "" + "You lose!(" if diceResult1[2] < diceResult2[2] else "" + "Draw" if diceResult1[2] == diceResult2[2] else ""
  bot.send_message(message.chat.id, won)
  write (user_man, "/dice" + '\n' + diceFinal1)
  write ("bot", '\n' + diceFinal2)
  write ("bot", '\n' + won)

# ECHO

@bot.message_handler(func=lambda m: True)
def echo_all(message):
  bot.reply_to(message, message.text)
  user_man = message.from_user.username + ' ' + message.from_user.first_name + ' ' + str (tconv(message.date))
  write(user_man, message.text)

bot.infinity_polling()

    