#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function
from __future__ import division
import sys
import os
import csv
from math import log10
from collections import defaultdict

words = []										# liste de mots
last_word_docid_pair = None									# pour le calcul du wordcount
df_t_dict = defaultdict(lambda: set())				# pour le calcul du df_t
docid_list = set()										# nombre de doc dans la collection


'''
***INPUT DATA*** | sortie de la fonction MAP triée sur stdin : word,docid\twordcount\tword_per_doc\tdf_t
	KEY: paire (word,docid)
	VALUE: wordcount\tword_per_doc\tdf_t

>>>> FOR #1 - Traitement de chaque ligne
	# 1. Calcule le "WordCount" en additionnant le nombre d'occurrences de chaque clés (mot,docid) et l'ajoute à la liste "words"
	# 2. Calcule df_t en construisant un dictionaire df_t_dict (key=word:value=set(docid))
	# 3. Calcule le nombre de document N dans la collection en construisant un set de chaque docid

>>>> FOR #2 - Traitement de la liste finale de mot "words"
	# 5. Donne les valeurs finale de df_t pour chaque mot
	# 6. Calcule TF-IDF
	# 7. Affichage sur chaque ligne de stdout : <word,docid______TFIDF>

***OUTPUT DATA*** | sur chaque ligne de stdout : <word,docid______TFIDF>
	KEY: paire (word,docid)
	VALUE: TFIDF

***OUTPUT DATA*** | fichier words_top20_tfidf_docid<docid>.csv
	top 20 des mots ayant la plus forte pondération pour chaque document
'''

for line in sys.stdin:
	# get key/values
	line = line.strip()
	key,wordcount,wordcount_per_doc,df_t = line.split("\t")
	wordcount_per_doc=int(wordcount_per_doc)
	wordcount = int(wordcount)
	df_t = int(df_t)
	word,docid = key.split(",")
	docid = int(docid)
	word_docid_pair = (word,docid)
	# 1. Calcule le "WordCount"
	if last_word_docid_pair is None:						# Traitement du 1er mot
		last_word_docid_pair = word_docid_pair
		last_wordcount = 0
		last_wordcount_per_doc = wordcount_per_doc
		last_df_t = df_t
	if word_docid_pair == last_word_docid_pair:
		last_wordcount += wordcount
	else:
		words.append([last_word_docid_pair,last_wordcount,last_wordcount_per_doc,last_df_t])
		# set new values
		last_word_docid_pair = word_docid_pair
		last_wordcount = wordcount
		last_wordcount_per_doc = wordcount_per_doc
		last_df_t = df_t
	# 2. Calcule df_t
	dic_value = df_t_dict[word]
	dic_value.add(docid)
	df_t_dict[word] = dic_value
	# 3. Calcule le nombre de document N dans la collection
	docid_list.add(docid)

# ajout du dernier mot non traité par l'étape 1
words.append([last_word_docid_pair,last_wordcount,last_wordcount_per_doc,last_df_t])
# 3. Calcule le nombre de document N dans la collection
N = len(docid_list)

for word_block in words:
	word,docid,wordcount,wordcount_per_doc,df_t = word_block[0][0],int(word_block[0][1]),int(word_block[1]),int(word_block[2]),int(word_block[3])
	# 5. Donne les valeurs finale de df_t & wordcount_per_doc à chaque mot
	df_t = len(df_t_dict[word])
	# 6. Calcule TF-IDF = wordcount x wordcount_per_doc x log10(N/df_t)
	word_block.append(wordcount * wordcount_per_doc * log10(N/df_t))
	TFIDF = word_block[4]
	# 7. ***OUTPUT DATA*** | ensemble de paires ((mot, doc_ID), TF-IDF) sur chaque ligne de stdout
	key_formated = '{:_<30}'.format("%s,%i" % (word,docid))
	print("%s\t%i\t%i\t%i\t%.*f" % (key_formated,wordcount,wordcount_per_doc,df_t,5,TFIDF))


# RESULTATS DE TEST - TOP 20 tf-idf for each document sent to words_top20_tfidf_<docid>.csv
for docid in docid_list:
	words_top20_tfidf = sorted([word_block for word_block in words if word_block[0][1] == docid], key=lambda x: x[4], reverse=True)[:20]
	document_name = 'words_top20_tfidf_docid'
	document_name +="%s" %(docid)
	with open('%s.csv' % document_name, 'w') as f:
		csv.writer(f).writerow(words_top20_tfidf)
