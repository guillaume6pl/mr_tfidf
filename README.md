tf-idf_mapper.py - tf-idf_reducer.py
======

## Objectif
tf-idf_mapper.py / tf-idf_reducer.py sont 2 scripts qui calculent la pondération tf-idf de chaque mots issu d'une collection de documents texte selon le modèle MAP/REDUCE. Ces deux scripts seront exécuté via Hadoop.

tf-idf = Term Frequency-Inverse Document Frequency
- mesure statistique permet d'évaluer l'importance d'un terme contenu dans un document, relativement à une collection
- la présence d'un terme rare de la requête dans le contenu d'un document fait croître le « score » de ce dernier
- Poids = Term Frequency * Inverse Document Frequency

Formule utilisée :
TFIDF = WordCount × WordPerDoc × log(N/df_t)
    - WordCount représente la fréquence d'un mot t dans un document d
    - WordPerDoc représente le nombre de mots dans un document d
    - df_t qui représente la fréquence du terme dans la collection, soit le nombre de documents dans lequel le mot t est présent
    - N est le nombre de documents dans notre collection


## Architecture de tf-idf_mapper
***INPUT DATA*** | récupère le contenu de chaque fichier texte sur la sortie stdin
1. Associe un ID au document lu
2. Tokénise en mots
3. Formatte chaque mot extrait
4. Renvoie sur stdout les "output data"
***OUTPUT DATA*** | Chaque mot est retourné avec un count = 1 sur stdout sur la forme suivante :
    - <key>\t<value>
    - <key> : word,docid
    - <value> : wordcount\tword_per_doc\tdf_t


## Architecture de tf-idf_reducer
***INPUT DATA*** | sortie de la fonction MAP triée sur stdin : word,docid\twordcount\tword_per_doc\tdf_t
	KEY: paire (word,docid)
	VALUE: wordcount\tword_per_doc\tdf_t
***FOR #1 - Traitement de chaque ligne***
1. Calcule le "WordCount" en additionnant le nombre d'occurrences de chaque clés (mot,docid) et l'ajoute à la liste "words"
2. Calcule df_t en construisant un dictionaire df_t_dict (key=word:value=set(docid))
3. Calcule le nombre de document N dans la collection en construisant un set de chaque docid
***FOR #2 - Traitement de la liste finale de mot "words"***
5. Donne les valeurs finale de df_t pour chaque mot
6. Calcule TF-IDF
7. Affichage sur chaque ligne de stdout les "output data"
***OUTPUT DATA*** | sur chaque ligne de stdout : <word,docid______TFIDF>
	KEY: paire (word,docid)
	VALUE: TFIDF
***OUTPUT DATA*** | fichier words_top20_tfidf_docid<docid>.csv
	top 20 des mots ayant la plus forte pondération pour chaque document




## Instructions
0. Récupérer les fichiers de la collection
Pour ce projet, nous considérons 2 documents texte :
- callwild
- defoe-robinson-103.txt
Ces 2 fichiers dans le répertoire /input/tf-idf sur hdfs
```
$ wget http://www.textfiles.com/etext/FICTION/defoe-robinson-103.txt
$ wget http://www.textfiles.com/etext/FICTION/callwild
hdfs dfs -copyFromLocal defoe-robinson-103.txt /input
hdfs dfs -copyFromLocal callwild /input
```

1. Démarrer hadoop
```
$ start-dfs.sh
```

2. Lancer les scripts via hadoop-streaming
```
$ cd <path_to_scripts>
$ hadoop jar <path_tohadoop_dir>/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar \
	-input /input/tf-idf/* \
	-output /results/tf-idf \
	-mapper tf-idf_mapper.py \
	-reducer tf-idf_reducer.py
```

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.3.jar \
	-input /input/tf-idf/* \
	-output /results/tf-idf \
	-mapper tf-idf_mapper.py \
	-reducer tf-idf_reducer.py

3. Récupérer les output data :
- output du reducer sur hdfs:/results/tf-idf/part-00000 : renvoie la liste exhaustive des pairs (<mot>,docid) triée et le TF-IDF associé
- jeu de résultats test
	* "words_top20_tfidf_docid1.csv" : contient le top 20 des mots ayant la plus forte pondération dans le document 1
	* "words_top20_tfidf_docid2.csv" : contient le top 20 des mots ayant la plus forte pondération dans le document 2


## Performance


## Résultats de test - Les 20 premiers mots ayant la plus forte pondérations dans le document 1 et 2
Ces 2 listes sont retournées par deux requêtes à la fin du script "tf-idf_reducer.py".

* Document 1
'friday'			2233776.526174811
'thoughts'			1385191.0301977878
'myself'			898502.2898580246
'board'				886023.0913877742
'viz'				836106.2975067728
'corn'				761231.1066852708
'cave'				748751.9082150204
'voyage'			736272.7097447701
'had'				711314.3128042694
'providence'		673876.7173935184
'labor'				648918.3204530177
'powder'			648918.3204530177
'deliverance'		574043.1296315157
'england'			511647.13728026394
'coast'				499167.93881001364
'sail'				499167.93881001364
'ships'				486688.7403397633
'storm'				436771.94645876193
'brazils'			424292.7479885116
'goats'				424292.7479885116

* Document 2
'buck'				1345213.0426536284
'dogs'				481354.1877866019
'thornton'			348122.2250956674
'sled'				257868.31488567957
'spitz'				257868.31488567957
'francois'			223485.8729009223
'bucks'				201996.846660449
'trail'				176210.01517188104
'john'				171912.20992378637
'perrault'			159018.7941795024
'hal'				128934.15744283979
'team'				128934.15744283979
'ice'				120338.54694665047
'traces'			120338.54694665047
'solleks'			116040.74169855581
'dave'				103147.32595427183
'thorntons'			90253.91020998785
'dawson'			85956.10496189319
'mercedes'			85956.10496189319
'throat'			81658.29971379854


## Version
**Version 1.1**
- Les résultats retournés sont différents de la première version. Mais les résultats sont cohérents et en accord le résultats d'autres outils. Je pense donc avoir des valeurs correctes.
- Les performances ont été considérablement améliorées :
	* dans le mapper: en calculant le nombre de mots par document
	* dans le reducer: en réalisant tous les calculs dans 2 boucles seulement
- A l'aide d'un dictionnaire, il a été possible de calculer df_t facilement
- Le nombre de document est calculé à partir d'un set ce qui rend le script beaucoup plus flexible.
- Temps d'exécution (testé sur un macbook 2.4 GHz Intel Core 2 Duo, 8GB 1067 MHz DDR3)
	* v1.0 : ~10 min
	* v1.1 : ~10sec.

## Contact
* e-mail: guillaume.attard@gmail.com
* Twitter: [@guillaumeattard](https://twitter.com/guillaumeattard)
