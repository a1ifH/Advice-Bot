# This a AI chatbox application that takes data from a chosen site and answers questions
import nltk
import newspaper
from newspaper import Article
import random
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Download Punkt
nltk.download('punkt', quiet=True)

# Pulling the website info
website = Article('https://www.menshealth.com/health/a31158940/coronavirus-covid-19-what-to-know/')
website.download()
website.parse()
website.nlp()
scraped = website.text

#Tokenization
text = scraped
_list = nltk.sent_tokenize(text)

# Response function

def index_sort(list_var):
	length = len(list_var)
	list_index = list(range(0, length))

	x = list_var
	for i in range(length):
		for j in range(length):
			if x[list_index[i]] > x[list_index[j]]:
				#swap

				temp = list_index[i]
				list_index[i] = list_index[j]
				list_index[j] = temp

	return list_index

def response(text):
	text = text.lower()
	#Bots Response
	bot_greetings = ['hello!', 'hi!', 'heya!', 'bonjour!', 'dia dhuit!']
	#users greetings
	user_greetings = ['hi', 'hey', 'hello', 'heya', 'howdy', 'whats ups']

	for word in text.split():
		if word in user_greetings:
			return random.choice(bot_greetings)

# Create the bots response

def bot_response(user_input):
	user_input = user_input.lower()
	_list.append(user_input)
	bot_response = ''
	cm = CountVectorizer().fit_transform(_list)
	sim_score = cosine_similarity(cm[-1], cm)
	sim_score_list = sim_score.flatten()
	index = index_sort(sim_score_list)
	index = index[1:]
	response_flag = 0


	j = 0
	for i in range(len(index)):
		if sim_score_list[index[i]] > 0.0:
			bot_response = bot_response+' ' +_list[index[i]]
			response_flag = 1
			j = j+ 1
		if j > 2:
			break

	if response_flag == 0:
		bot_response = bot_response+' '+"I do not understand."

	_list.remove(user_input)


	return bot_response

print("Advice Bot: I am the COVID-19 Advice BOT, ask a question and I shall answer!")
print("Advice Bot: If you want to end the conversation please enter 'leave'.")

exit_list = ['exit', 'goodbye', 'bye', 'quit', 'leave']

while(True):
	user_input = input()
	if user_input.lower() in exit_list:
		print("Advice Bot: Goodbye!")
		break
	else:
		if response(user_input) != None:
			print("Advice Bot: "+ response(user_input))
		else:
			print("Advice Bot:"+ bot_response(user_input))
