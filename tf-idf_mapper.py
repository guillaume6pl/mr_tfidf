#!/usr/bin/env python
#coding: utf-8

from __future__ import print_function
from __future__ import division
import sys
import re

words=[]
doc_id=0;
line_number=1
wordcount = 1
wordcount_per_doc = 0
df_t=1

for line in sys.stdin:
	'''
	0. ***INPUT DATA*** | récupère le contenu de chaque fichier texte sur la sortie stdin
	1. Associe un ID au document lu
	2. Tokénise en mots
	3. Formatte chaque mot extrait
	4. Ajoute les mots de la ligne à la liste complète de mots
	5. Calcule le nombre de mot dans le document analysé
	6. ***OUTPUT DATA*** | Chaque mot est retourné sur stdout sur la forme suivante :
	    - <key>\t<value>
	    - <key> : 'word',docid
	    - <value> : wordcount,wordcount_per_doc, df_t
	'''
	# Supprimer les espaces
	line = line.strip()

	# 1. Associe un ID au document lu
	if line_number==1:
		if line=='1903':
			doc_id=2
			line_number=0
		else:
			doc_id=1
			line_number=0

	# 2. Tokénise en mots
	words_in_line = line.split()

	# 3. Formatte chaque mot extrait
	# lower case
	words_in_line = [word.lower() for word in words_in_line]
	# Suppression des ponctuations et des caractères numériques (with regex)
	words_in_line = [re.sub(r'[^\w]', '', word) for word in words_in_line]
	# filtering stop words
	stopwords=[]
	for line in open('stopwords_en.txt'):
		stopwords.append(line.strip())
	words_in_line = [word for word in words_in_line if word not in stopwords]
	# Suppression des mots de moins de 3 caractères
	words_in_line = [word for word in words_in_line if len(word)>2]

	# 4. Ajoute les mots de la ligne à la liste complète de mots
	words += words_in_line

	#4. Calcule le nombre de mot par ligne et ajoute "wordcount_per_doc" à la liste de mots
	wordcount_per_doc += len(words_in_line)

# 5. ***OUTPUT DATA*** | Chaque mot est retourné sur stdout
for word in words:
	print("%s,%i\t%i\t%i\t%i" % (word,doc_id,wordcount,wordcount_per_doc, df_t))
