from bs4 import BeautifulSoup as bs
import pandas as pd
import requests

dataframe = pd.read_csv("Input.csv")
dataframe.head()

for i in range(len(dataframe['URL_ID'])):
  page = requests.get(dataframe['URL'][i], headers={"User-Agent": "Chrome/81.0.4044.141 Safari/537.36"})
  page.content
  soup = bs(page.content, 'html.parser')
  data= soup.find("div",class_="td-post-content")
  text=data.get_text()
  final_text=text.replace("\n","")
  f = open(f"{dataframe['URL_ID'][i]}"+'.txt', 'w')
  f.write(final_text)
  f.close()

from nltk.tokenize import sent_tokenize , word_tokenize
import nltk
nltk.download('punkt')
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
nltk.download('wordnet')

# link was not working so i used set of positive and negative words availabe on internet
file = open('pos.txt','r')
pos_words = file.read().split()
file = open('neg.txt', 'r')
neg_words = file.read().split()

POSITIVE_SCORE =[]
NEGATIVE_SCORE = []
POLARITY_SCORE =[]
SUBJECTIVITY_SCORE = []
AVG_SENTENCE_LENGTH = []
PERCENTAGE_OF_COMPLEX_WORDS = []
FOG_INDEX = []
AVG_NUMBER_OF_WORDS_PER_SENTENCE = []
COMPLEX_WORD_COUNT = []
WORD_COUNT = []
SYLLABLE_PER_WORD = []
PERSONAL_PRONOUNS = []
AVG_WORD_LENGTH = []

for i in range(len(dataframe['URL_ID'])):
  f = open(f"{dataframe['URL_ID'][i]}"+'.txt', "r")
  text = f.read()
  raw_text=str.lower(text)
  sent_text=sent_tokenize(raw_text)
  clean_text_1=[]
  for sent in sent_text:
    clean_text_1.append(sent)
  
  clean_text_2 = [ word_tokenize(i) for i in clean_text_1]
  
  clean_text_3 =[]
  for words in clean_text_2:
    clean=[]
    for w in words :
      res = re.sub(r'[^\w\s]',"",w)
      if res != "":
        clean.append(res)
    clean_text_3.append(clean)

  clean_text_4=[]
  for words in clean_text_3:
    w=[]
    for word in words:
      if not word in stopwords.words('english'):
        w.append(word)
    clean_text_4.append(w)
  port = PorterStemmer() 
  clean_text_5 = []
  for words in clean_text_4:
    w=[]
    for word in words:
      w.append(port.stem(word))
    clean_text_5.append(w)
  wnet = WordNetLemmatizer()
  lem =[]
  for words in clean_text_4:
    w=[]
    for word in words:
      w.append(wnet.lemmatize(word))
    lem.append(w)
  
  pos_count=0
  neg_count=0

  for words in lem:
    for word in words:
      if word in pos_words:
        pos_count += 1
      elif word in neg_words:
        neg_count += 1
  
  POSITIVE_SCORE.append(pos_count)
  NEGATIVE_SCORE.append(neg_count)
  
  #Polarity Score = (Positive Score – Negative Score)/ ((Positive Score + Negative Score) + 0.000001)
  polarity = (pos_count - neg_count)/((pos_count + neg_count)+ 0.000001)

  total_words =0
  for words in lem:
    for word in words:
      total_words += 1
  
  WORD_COUNT.append(total_words)
  
  #Subjectivity Score = (Positive Score + Negative Score)/ ((Total Words after cleaning) + 0.000001)
  sub = (pos_count + neg_count)/((total_words)+0.000001)

  POLARITY_SCORE.append(polarity)
  SUBJECTIVITY_SCORE.append(sub)

  # Average Sentence Length = the number of words / the number of sentences
  total_sent = 0
  for words in lem:
    total_sent += 1

  Avg_Sent_Len = total_words/total_sent 

  AVG_SENTENCE_LENGTH.append(Avg_Sent_Len)

  vowel = ['a', 'e', 'i', 'o', 'u']
  for words in lem:
    complex_count=0
    for word in words:
      vowel_count = 0
      for letter in word:
        if letter in vowel:
          vowel_count += 1
        if vowel_count >= 2 :
          complex_count += 1 
  
  COMPLEX_WORD_COUNT.append(complex_count)

  # Percentage of Complex words = the number of complex words / the number of words 
  per_complex = complex_count/total_words
  
  # Fog Index = 0.4 * (Average Sentence Length + Percentage of Complex words)
  fog = 0.4*(Avg_Sent_Len+per_complex)

  #Average Number of Words Per Sentence = the total number of words / the total number of sentences
  avg_word_sent = total_words / total_sent

  PERCENTAGE_OF_COMPLEX_WORDS.append(per_complex)
  FOG_INDEX.append(fog)
  AVG_NUMBER_OF_WORDS_PER_SENTENCE.append(avg_word_sent)

  #Syllable Count Per Word
  vowel = ['a', 'e', 'i', 'o', 'u']
  for words in lem:
    vowel_count = 0
    for word in words:
      if word[:-2]=='es' or  word[:-2]=='ed':
        continue
      else:
        for letter in word:
          if letter in vowel:
            vowel_count += 1

  syll_per_word = vowel_count/total_words

  #Personal Pronouns
  personal = [ "I", "we" ,"my", "ours", "us" ]
  personal_count = 0
  for words in clean_text_3:
    for word in words:
      if word in personal:
        personal_count +=1  

  letter_count=0
  for words in lem:
    for word in words:
      for letter in word:
          letter_count += 1
  
  #Average Word Length =Sum of the total number of characters in each word/Total number of words
  avg_word_len = letter_count/total_words
  
  SYLLABLE_PER_WORD.append(syll_per_word)
  PERSONAL_PRONOUNS.append(personal_count)
  AVG_WORD_LENGTH.append(letter_count)



df= pd.DataFrame()

df['URL_ID']=dataframe['URL_ID']
df['URL']=dataframe['URL']
df['POSITIVE SCORE']=POSITIVE_SCORE
df['NEGATIVE SCORE']=NEGATIVE_SCORE
df['POLARITY SCORE']=POLARITY_SCORE
df['SUBJECTIVITY SCORE']=SUBJECTIVITY_SCORE
df['AVG SENTENCE LENGTH']=AVG_SENTENCE_LENGTH
df['PERCENTAGE OF COMPLEX WORDS']=PERCENTAGE_OF_COMPLEX_WORDS
df['FOG INDEX']=FOG_INDEX
df['AVG NUMBER OF WORDS PER SENTENCE']=AVG_NUMBER_OF_WORDS_PER_SENTENCE
df['COMPLEX WORD COUNT']=COMPLEX_WORD_COUNT
df['WORD COUNT']=WORD_COUNT
df['SYLLABLE PER WORD']=SYLLABLE_PER_WORD
df['PERSONAL PRONOUNS']=PERSONAL_PRONOUNS
df['AVG WORD LENGTH']=AVG_WORD_LENGTH

df

df.to_csv("Output.csv")