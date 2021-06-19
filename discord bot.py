import random
import json
import pickle
import numpy as np 
import nltk
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import pywhatkit as kit
import discord
import time
import asyncio
import concurrent

lemmatizer = WordNetLemmatizer()

intents = json.loads(open('C:\workspace\git\intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl', 'rb'))
model = load_model('chatbotmodel.h5')
    
def clean_up_sentence(sentence):    
    sentence_words = nltk.word_tokenize(sentence)
    sentence_words = [lemmatizer.lemmatize(word) for word in sentence_words]
    return sentence_words

def bag_of_words(sentence):
    sentence_words = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_words:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_words(sentence)
    res = model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]

    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list = [{'intent': classes[r[0]], 'probability': str(r[1])}]
    return return_list

def get_response(intents_list, intents_json):
    tag = intents_list[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result

def job():
    print("Enter numbers")
    m = int(input())
    n = int(input())
    k = 0
    while k<5:
        m = n*m
        k = k+1
    return m

def whatsapp():
    print("is it a group?")
    ny=input()
    if ny=="no":

       print("Enter phone number")
       x = input()
       print("Enter the message")
       y = input()
       print("Do you want to send it now?yes/no")
       yn = input()
       if yn=="yes":
          kit.sendwhatmsg_instantly(x,y)
       elif yn=="no":
           print("which hour do you want to send the message")
           z = int(input())
           print("which minute do you want to send the message")
           t= int(input())
           kit.sendwhatmsg(x,y,z,t,print_wait_time=False)
       else:
           print("incorrect option please try using lower case")
    elif ny=="yes":
        print("Enter group ID")
        x = input()
        print("Enter the message")
        y = input()
        print("which hour do you want to send the message")
        z = int(input())
        print("which minute do you want to send the message")
        t= int(input())
        kit.sendwhatmsg_to_group(x,y,z,t,wait_time=2)

def youtube():
    print("what do you wanna watch?")
    x = input()
    kit.playonyt(x)

def stop():
    return False

def search():
    print("what do you want to search")
    x = input()
    kit.search(x)


print("chatbot is running")
def bot(message):
 a = False
 if message == "start bot":
     a = True
 while a:
    ints = predict_class(message)
    res = get_response(ints, intents)
    if res=="stop":
        a = stop()
    t = 0
    for x in res:
        if x=='*':
            t += 1
    if t>=1:
        y = res.strip('*')
        u = eval(y+"()")
        return u
    else:
        return res
        
client = discord.Client()

@client.event
async def on_ready():
    print('we have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
    loop = asyncio.get_event_loop()
    x = await loop.run_in_executor(executor,bot,message.content)
    time.sleep(2)
    await message.channel.send(x)


client.run("ODQ3NzI1Njk1MjIwNDQ5Mjgw.YLCQEw.Hqgw-nwE5_LvDraQIUAXr1tWyOo")