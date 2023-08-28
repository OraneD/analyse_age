### 1 - Conversion trs -> TextGrid

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

**J'ai reessayé d'ouvrir tous les TextGrids qui posaient problème quelques jours après la conversion, ils s'ouvraient tous. Sûrement un bug de praat donc.**

### 2 - Extraction audio + TextGrid du tier du locuteur
Je n'ai pas trouvé ni dans SPPAS, ni dans ELAN une façon d'extraire le tier souhaité du TextGrid et la partie audio correspondante. J'ai donc écrit un script praat pour le faire : [segmentation_tiers_interviewee.praat](/scripts/segmentation_praat/segmentation_tiers_interviewee.praat). 

J'ai lancé le script sur deux des TextGrids obtenus avec ELAN. Il est malheureusement impossible de lancer le script sur l'ensemble du corpus car le tier à extraire n'a jamais le même nom ni le même numéro. 

Le script ne récupère que le tier de la personne interrogée, il est donc censé ne récupérer que sa voix cependant parfois le chercheur parle en même temps que le locuteur ce qui compromet la qualité de l'enregistrement, faut-il supprimer ces intervalles ? 

### 3 - Nettoyage des TextGrids

J'ai pour l'instant laissé cette étape de côté car je ne suis pas sûre des modifications à apporter aux TextGrids. J'ai parcouru les fichiers TRS, manuellement et avec des commandes shell, les annotations semblent assez uniformes sur l'ensemble du corpus.

### 4 - Alignement

- **MFA** : J'ai lancé l'alignement sur les fichiers wav et TextGrid obtenus avec mon script praat. Tout semble avoir fonctionné correctement : certains mots ne sont pas transcrits, notamment ceux avec des -. 

## 25/08

### - Extraction audio + TextGrid du tier du locuteur

Je n'avais pas pris en compte les cas de chevauchements lors de l'extraction du tiers du locuteur dans les TextGrid. Ils sont tous signalés dans les TextGrids, j'ai donc retravaillé le script qui permet d'extraire le tier et l'audio correspondant, les intervalles où il y a chevauchement sont maintenant indiqués. 

Je devais lancer le script d'extraction pour chaque locuteur car je ne voyais pas comment récupérer les arguments du script spécifiques à chaque locuteur. J'ai fini par trouver une solution et un [script batch](/scripts/segmentation_praat/extract_tiers.bat) permet de lancer le script praat d'extraction sur l'ensemble du corpus. 

Seuls trois dossiers n'ont pas pu être traités : ESLO2_ENT_1069, ESLO2_ENT_1080 et ESLO2_ENT_1081. Les transcriptions TRS pour ces trois locuteurs ne contiennent pas de tier "Turns" qui permet d'indiquer les tours de parole les chevauchements. 

## 27/08

### - Segmentation des intervalles

* Le script [segmentation_interval.praat](/scripts/segmentation_praat/segmentation_interval.praat) permet de découper les TextGrids et fichiers audio en fonction des intervalles présents dans le TextGrid. J'ai ignoré les intervalles indiquant seulement des [rire] ou des [bb] ainsi que ceux qui avaient été annotés comme comprenant un chevauchement. [extract_intervals.bat](/scripts/segmentation_praat/extract_intervals.bat) permet de lancer le script praat sur l'ensemble du corpus. 

- J'ai ensuite procédé à quelques vérifications avant de lancer MFA sur les corpus constitués :

    - Les TextGrids contiennent parfois des mots coupés lorsque le locuteur s'interrompt, notés 'mot-'. MFA ne peut pas transcrire ces mots. Je voulais vérifier s'ils étaient ou non en quantité négligeable dans les corpus. Le script bash [count-.sh](/scripts/count-.sh) permet de calculer, pour chaque locuteur, le pourcentage de TextGrid contenant des mots coupés. En moyenne, ils sont présents dans 1.2% des TextGrids.
    - Je voulais également vérifier, après la segmentation, le temps d'enregistrement final pour chaque locuteur. Les scripts bash [count_duration.sh](/scripts/count_duration.sh) et [duration_1dir.sh](/scripts/duration_1dir.sh) permettent de calculer la durée totale des échantillons audios récoltés pour chaque locuteur. Les durées calculées sont ensuite ajoutées au fichier [age_time.csv](/metadonnes_corpus/age_time.csv). Le script [time_loc.py](/scripts/time_loc.py) permet ensuite, à partir du csv, de générer un [plot](/metadonnes_corpus/durees_echantillons_loc.png) pour visualiser la répartition des temps d'enregistrement par tranches d'âge. 


### - Ajout du module ESLO2 Entretiens Jeunes

- La tranche 20-35 ans avait une durée totale d'enregistrement beaucoup moins grande que les tranches 35-60 et 60-90. J'ai donc téléchargé un autre module d'ESLO2 qui comprend des entretiens avec des jeunes, de 20 à 25 ans. 9 enregistrements sont disponibles. J'ai lancé mes scripts sur l'ensemble des dossiers afin d'obtenir des corpus MFA et n'ai rencontré aucun problème.
- L'ajout des ces 9 locuteurs permet à la tranche 20-35 d'avoir une durée totale d'enregistrement similaire à la tranche 60-90, mais un déséquilibre persiste car la tranche 35-60 a une durée d'enregistrement qui est presque le double de celle des deux autres tranches.



