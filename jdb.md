## 1 - Conversion trs -> TextGrid

- **Scripts** : le script shell [trans2praat.sh](/scripts/Conversion_trs2TextGrid/trans2praat.sh) permet de lancer le script Perl [trs_to_tg.pl](/scripts/Conversion_trs2TextGrid/trs_to_tg.pl) qui converti les fichiers TRS en TextGrid sur l'ensemble du corpus. La plupart des TextGrids obtenus s'ouvrent correctement sur praat mais pas tous. J'ai essayé de lancer d'autres scripts Perl sur le corpus, même problème. J'ai donc décidé de convertir l'ensemble des fichiers TRS avec SPPAS.

- **SPPAS** : Le logiciel permet de convertir des fichiers TRS en TextGrid, il est possible de lancer la conversion sur plusieurs fichiers en même temps. Sur Linux, le logiciel envoie un message d'erreur pendant la procédure mais il suffit d'attendre, les fichiers sont quand même convertis. Quelques fichiers cependant n'ont pas pu être convertis en raison d'une erreur dans les fichiers TRS.

- **ELAN** : Je n'ai pas trouvé comment convertir tous les fichiers TRS en même temps, j'ai donc converti tous les fichiers un à un. Tous les fichiers ont bien pu être convertis cependant là encore certains TextGrid ne s'ouvrent pas sur praat :

```
Found a string while looking for a real number in text (line..).
"xmax" not read
"xmin" not read
``` 
Il manque les valeurs de xmax ou de xmin pour un interval donné, qui semble correspondre à une balise 
```
<Sync time="2545.216"/>
```
dans le fichier trs. Je travaille à résoudre ce problème mais je n'ai pas encore trouvé comment faire
Liste des fichiers posant problème :
- 5
- 45
- 47
- 55
- 56
- 62
- 67
- 71
- 77
- 79
- 82
- 83

## 2 - Extraction audio + TextGrid du tier du locuteur
Je n'ai pas trouvé ni dans SPPAS, ni dans ELAN une façon d'extraire le tier souhaité du TextGrid et la partie audio correspondante. J'ai donc écrit un script praat pour le faire : [segmentation_tiers_interviewee.praat](/scripts/segmentation_praat/segmentation_tiers_interviewee.praat). 

J'ai lancé le script sur deux des TextGrids obtenus avec ELAN. Il est malheureusement impossible de lancer le script sur l'ensemble du corpus car le tier à extraire n'a jamais le même nom ni le même numéro. 

Le script ne récupère que le tier de la personne interrogée, il est donc censé ne récupérer que sa voix cependant parfois le chercheur parle en même temps que le locuteur ce qui compromet la qualité de l'enregistrement, faut-il supprimer ces intervalles ? 

## 3 - Nettoyage des TextGrids

J'ai pour l'instant laissé cette étape de côté car je ne suis pas sûre des modifications à apporter aux TextGrids. J'ai parcouru les fichiers TRS, manuellement et avec des commandes shell, les annotations semblent assez uniformes sur l'ensemble du corpus.

## 4 - Alignement

- **MFA** : J'ai lancé l'alignement sur les fichiers wav et TextGrid obtenus avec mon script praat. Tout semble avoir fonctionné correctement : certains mots ne sont pas transcrits, notamment ceux avec des -. 