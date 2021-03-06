# -*- coding: utf-8 -*-

#Video Transcription

!pip install  youtube_transcript_api

from youtube_transcript_api import YouTubeTranscriptApi

video = "https://youtu.be/NUzDLpSkQTg"

video_id = video.split("e/")[1]
video_id

YouTubeTranscriptApi.get_transcript(video_id)
transcript = YouTubeTranscriptApi.get_transcript(video_id)

transcript

together = ""
for i in transcript:
    together = together + ' ' + i['text']
print(together)

print(len(together))

#Text Summarization

#Using Hugging Face Transformer(Abstractive Summarization)
!pip install transformers

from transformers import pipeline

summarizer = pipeline("summarization")

itr = int(len(together)/1000)
itr

summary=[]
for i in range(0,itr+1):
  a= i*1000
  b= (i+1)*1000
  result = summarizer(together[a:b],min_length=20,max_length=50)
  summary.append(result)

summary

final_summary =' '.join([str(i) for i in summary])
final_summary = final_summary.replace("[{'summary_text':","")
final_summary = final_summary.replace("\"","")
final_summary = final_summary.replace("}]","")
final_summary = final_summary.replace("''","")
final_summary

#print("Text\n",together)
print("Length of Transcript=",len(together))

#print("Summary\n",final_summary)
print("Length  of Summary by Transformer",len(final_summary))

#Using Spacy Library(Extractive Summarization)
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation

nlp= spacy.load("en_core_web_sm")

doc=nlp(together)

tokens=[token.text for token in doc]
print(tokens)

punctuation=punctuation + '\n' 
word_freq={}
stop_words= list(STOP_WORDS)

for word in doc:
   if word.text.lower() not in stop_words:
     if word.text.lower() not in punctuation:
       if word.text not in word_freq.keys():
         word_freq[word.text]= 1
       else:
         word_freq[word.text]+= 1 
print(word_freq)

max_freq = max(word_freq.values())
for word in word_freq.keys():
   word_freq[word]=word_freq[word]/max_freq 
print(word_freq)

sent_score={}
sent_tokens=[sent for sent in doc.sents]
for sent in sent_tokens:
   for word in sent:
     if word.text.lower() in word_freq.keys():
       if sent not in sent_score.keys():
         sent_score[sent]=word_freq[word.text.lower()]
       else:
         sent_score[sent]+= word_freq[word.text.lower()] 
print(sent_score)

from heapq import nlargest
n = int(len(sent_score)*0.1 )
summary=nlargest(n,iterable=sent_score,key=sent_score.get) 
print(summary)

fi_summary =' '.join([str(i) for i in summary])
print(fi_summary,"\n")
print("Length of Summary by ",len(fi_summary))
