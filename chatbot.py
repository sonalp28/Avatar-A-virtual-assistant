#General Libraries
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet as wn
import re
import aiml
import subprocess
import os
import argparse
from MyKernel import MyKernel
from time import sleep
#end of general libraries



import time, threading
#end of Graphics libraries

DEBUG = True
SHOW_MATCHES = True

def course_code(sentence):
	try:
		words = re.compile('\w+').findall(sentence)
		new_sentence = ""
		for index, word in enumerate(words):
			if (word == "cs") and (index < len(words)-1) and (words[index+1].isdigit()):
				new_sentence = new_sentence + word
			else:
				new_sentence = new_sentence + word + " "
		return new_sentence
	except:
		return sentence

def remove_aiml_char(sentence):
    try:
        new_sentence = sentence.replace("_","")
        new_sentence = new_sentence.replace("*","")
        return new_sentence
    except:
        return sentence

dict = {'NN': 'NOUN', 'JJ': 'ADJ'}
dict['NNS'] = 'NOUN'
dict['NNP'] = 'NOUN'
dict['NNPS'] = 'NOUN'
dict['PRP'] = 'NOUN'
dict['PRP$'] = 'NOUN'
dict['RB'] = 'ADV'
dict['RBR'] = 'ADV'
dict['RBS'] = 'ADV'
dict['VB'] = 'VERB'
dict['VBD'] = 'VERB'
dict['VBG'] = 'VERB'
dict['VBN'] = 'VERB'
dict['VBP'] = 'VERB'
dict['VBZ'] = 'VERB'
dict['WRB'] = 'ADV'

grade_codes = ["ap","aa","ab","bb","bc","cc","cd","dd","dx","fr"]

BOT_INFO = {
    "name": "Avatar",
    "birthday": "December 3rd 2018",
    "location": "Syracuse, NY, USA",
    "master": "Syracuse University",
    "website":"https://www.syracuse.edu/",
    "gender": "Female",
    "age": "20",
    "size": "",
    "religion": "I am AI",
    "party": "Oh yes,of course anytime!"
}

k = MyKernel()
k.learn("aiml/standard/std-startup.xml")
k.respond("LOAD AIML B")

for key,val in BOT_INFO.items():
	k.setBotPredicate(key,val)


class MyApp():
    def __init__(self,name):
        self.name = name
	print("Hi! Welcome to the world of virtual assitance! I am Avatar")
        self.customerName = raw_input("Avatar : Can I know your Name? - ")
        print("Avatar : Hi " + self.customerName + " ! How can I help you? ")
        self.buttonClicked()

    def buttonClicked(self):
        while True:
                myinput = raw_input(self.customerName+" : ")
                found_answer = 0
                with open("text.txt") as myfile:
                        for line in myfile:
                                if line.startswith(myinput.lower()):
                                         found_answer = 1
                                         answer = line.split('?')[-1].strip()
                                         print "Avatar : " + answer
                if found_answer != 1:                        
                        sentence = myinput.lower()
                        sentence = course_code(sentence)
                        stop_words = set(stopwords.words('english'))

                        word_tokens = word_tokenize(sentence)

                        filtered_sentence = [w for w in word_tokens if not w in stop_words]

                        temp = nltk.pos_tag(filtered_sentence)
                       
                        new_sentence = ""
                        for i in temp:
                            try:
                                    z = i[1]
                                    if (dict[z] != None):
                                            part_speech = dict[z]
                                    else:
                                            part_speech = 'NOUN'
                                    if(part_speech == 'NOUN'):
                                            word = wn.morphy(i[0],wn.NOUN)
                                    elif(part_speech == 'VERB'):
                                            word = wn.morphy(i[0],wn.VERB)
                                    elif(part_speech == 'ADV'):
                                            word = wn.morphy(i[0],wn.ADV)
                                    elif(part_speech == 'ADJ'):
                                            word = wn.morphy(i[0],wn.ADJ)
                                    word1 = wn.synsets(word)[0].lemmas()[0].name()
                                    if i[0] in grade_codes:
                                            word1 = i[0]
                            except:
                                    word1 = i[0]
                        new_sentence = new_sentence+" "+word1.lower()
                        new_sentence = remove_aiml_char(new_sentence)

                        if DEBUG:
                                #print("Inside Debug")
                                #printing first output
                                matchedPattern = k.matchedPattern(myinput)
                                response = k.respond(myinput)
                                matchedPattern = k.matchedPattern(new_sentence)
                                if k.formatMatchedPattern(matchedPattern[0]) == "*":
                                        feedback_response = raw_input("Avatar : Sorry I wasn't able to help you with this questions perhaps you can give me the answer - ")
                                        f = open("text.txt","a")
                                        f.write(myinput.lower())
                                        f.write(feedback_response)
                                        f.write("\n")
                                        f.close()
                                        print "Thank you for adding knowledge to my brain!"
                                else:                                        
                                        print("Avatar : " + response)
                                response = k.respond(myinput)
                                response1 = k.respond(new_sentence)
                                if response1 != "" and response1[0] == '$':
                                        response = response1[1:]

if __name__ == "__main__":
        MyApp("Avatar")
