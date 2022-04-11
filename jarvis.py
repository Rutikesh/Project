from pydoc import describe
import webbrowser as wb
import webbrowser
import scipy as sp
import speech_recognition as sr
import pyttsx3
import datetime
import smtplib
from secrete import senderemail, epwd, to
from email.message import EmailMessage
import os
import wikipedia
import pywhatkit
import requests
import runner
import wolframalpha
from newsapi import NewsApiClient

engine = pyttsx3.init()

def speak(audio):
	engine.say(audio)
	engine.runAndWait()

def getvoices(voice):
	voices = engine.getProperty('voices')
	# print(voices[1].id)
	if voice == 1:
		engine.setProperty('voice',voices[0].id)
		speak("hello this is jarvis")

	if voice == 2:
		engine.setProperty('voice',voices[1].id)
		speak("hello this is Friday")
	

def time():
	Time = datetime.datetime.now().strftime("%I:%M:%S") # hour= I minutes = M seconds = S
	speak("the current time is: ")
	speak(Time)

def date():
	year = int(datetime.datetime.now().year)
	month = int(datetime.datetime.now().month)
	date = int(datetime.datetime.now().day)
	speak("the current date is: ")
	speak(date)
	speak(month)
	speak(year)

def greeting():
	hour = datetime.datetime.now().hour
	if hour >=6 and hour <= 12:
		speak("Good morning sir")
	elif hour >=12 and hour <= 18:
		speak("Good afternoon sir")
	elif hour >=18 and hour < 24 :
		speak("Good evening sir")
	else:
		speak("Good night sir")
	speak("jarvis at your servies, please tell me hoe can i help you?")


# def wishme():
# 	speak("wellcome back sir")
# 	time()
# 	date()
# 	greeting()
# 	speak("jarvis at your servies, please tell me hoe can i help you?")

def takecommandMic():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("Listening...")
		r.pause_threshold =1
		audio =r.listen(source)
	try:
		print("recognizning")
		query = r.recognize_google(audio, language="en-IN")
		print(f": Your Command : {query}\n")
	except Exception as e:
		print(e)
		speak("say that again Please...")
		return"None"
	return query

def sendEmail(receiver,subject,content):
	server = smtplib.SMTP('smtp.gmail.com',587)
	server.starttls
	server.login(senderemail,epwd)
	email = EmailMessage()
	email['From'] = senderemail
	email['To'] = receiver
	email['subject'] = subject
	email.set_content(content)
	server.send_message(email)
	server.close()

def searchgoogle():
	speak("what should i search for?")
	search = takecommandMic()
	wb.open('https://www.google.com/search?q='+search)

def news():
	newapi= NewsApiClient(api_key='a1a230e9886b4f15a4e2a8b5277b02b9')
	speak("what topic you need the news about?")
	topic = takecommandMic()
	data =newapi.get_top_headlines(q=topic,language ='en',page_size = 4)
	newsdata = data['articles']
	for x,y in enumerate(newsdata):
		print(f'{x} {y["description"]}')
		speak(f'{x} {y["description"]}')

if __name__ == "__main__":
	clear = lambda: os.system('cls')
	clear()
	getvoices(2)
	greeting()
	# wishme()
	while True:
		query = takecommandMic().lower()
		
		if 'time' in query:
			time()

		elif 'date' in query:
			date()

		elif 'email' in query:
			email_list = {
				'testemail':'gfrrbzvkwtaiqwtibl@bvhrs.com'
			}
			try:
				speak('To whom you want to send the mail ?')
				name = takecommandMic() 
				receiver = email_list[name]
				speak("what is the subject of the mail ?")
				subject = takecommandMic()
				speak('what should i say?')
				content = takecommandMic()
				sendEmail(receiver,subject,content)
				speak("email has been send")
			except Exception as e:
				print(e)
				speak("unable to end the email")
		
		elif'wikipedia' in query:
			speak("Searching Wikipedia...")
			query = query.replace("wikipedia", "")
			results =  wikipedia.summary(query, sentences = 3)
			speak("According to Wikipedia")
			print(results)
			speak(results)

		elif'search' in query:
			searchgoogle()

		elif 'youtube' in query:
			speak("what should i search for on youtub?")
			topic = takecommandMic()
			pywhatkit.playonyt(topic)

		elif 'where is' in query:
			query = query.replace('where is',"")
			location = query
			speak("User asked to locate")
			speak(location)
			webbrowser.open("https://www.google.nl/maps/place/"+location+"")

		elif "where i am" in query or "where are we" in query:
				speak("wait sir let me check")
				try:
					ipAdd = requests.get('https://api.ipify.org').text
					print(ipAdd)
					url = 'https://get.geojs.io/v1/ip/geo/'+ipAdd+'.json'
					geo_requests = requests.get(url)
					geo_data = geo_requests.json()
					# print(geo_data)
					city = geo_data['city']
					state = geo_data['state']
					country = geo_data['country']
					speak(f"Sir im not sure, but we are in {city} city {state} state of {country} country")
				except Exception as e:
					speak("Sorry Sir, Due to network issue i am not able to find where we are.")
					pass     

		elif 'game' in query:
			from runner import game
			game()

		elif 'calculate' in query:
			app_id = '9T2EHT-6J8J4WLJKW'
			client = wolframalpha.Client(app_id)
			index = query.lower().split().index('calculate')
			query = query.split()[index + 1:]
			res = client.query(' '.join(query))
			answer = next(res.results).text
			print("The answer is " + answer)
			speak("The answer is " + answer)

		elif 'what is' in query or 'who' in query :
			app_id = '9T2EHT-6J8J4WLJKW'
			client = wolframalpha.Client(app_id)
			res = client.query(query)
			
			try:
				print (next(res.results).text)
				speak(next(res.results).text)
			except StopIteration:
				print("No result")

		elif'weather' in query:
			speak("Which city's weather to check")
			city = takecommandMic()
			url="https://api.openweathermap.org/data/2.5/weather?q="+city+"&units=imperial&appid=7e5bdf1c4bdda393b6e11e734520644e"
			
			res = requests.get(url)
			data = res.json()
			
			weather = data['weather'] [0] ['main']
			temp= data['main']['temp']
			desp= data['weather'][0]['description']
			temp = round((temp - 32) * 5/9)
			print(weather)
			print(temp)
			print(desp)
			speak(f'weather in {city} city is like')
			speak('Temperature: {} degree celcius'.format(temp))
			speak('weather is {} '.format(desp))

		elif'news' in query:
			news()