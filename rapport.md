
## Segmentation automatique avec praat
J'ai extrait les intervalles automatiquement avec Praat. Contrairement au corpus de Léna, les intervalles dans mon corpus sont tous plutôt courts, parfois trop courts. Ils n'éxcedent que très rarement 5 secondes. Ils sont aussi parfois plus courts qu'une seconde et ne contiennent qu'un mot voire seulement un marqueur discursif. 


Pour l'instant, j'ai écrit un script praat qui garde tous les intervalles, peu importe leur durée mais il est possible d'ignorer les cas où les intervalles sont trop courts. 
* Les intervalles que j'ai récupérés font en moyenne 2 secondes, est-ce trop court ? (1.82s pour le premier locuteur et 2.45s pour le deuxième locuteur )
* Lorsque les intervalles ne contiennent qu'un mot, dois-je les concaténer avec leurs voisins ou puis-je simplement les ignorer ?

## Alignement avec MFA ##
J'ai utilisé MFA sur les corpus segmentés. Pour les deux fichiers traités il ne semble pas y avoir de problème. J'ai sauté l'étape de nettoyage des TextGrids car je n'étais pas sûre de ce qu'il fallait garder pour l'alignement. Malgré cela, MFA n'a pas fait beaucoup d'erreur les mots sont presques tous transcrits. Il reste le problème des cas où le locuteur s'interrompt, notés avec un tiret '-'. L'aligneur ne reconnaît alors pas le mot et ne le transcrit pas.  Que faire de ces cas ?

## Travail sur le reste du corpus ##

Il me reste 77 locuteurs à traiter. Je pense écrire un script pour nettoyer les TextGrid en fonction des erreurs repérées manuellement dans les fichiers que j'ai générés. Il me restera alors à lancer manuellement mes scripts pour chaque locuteur, en espérant ne pas rencontrer de problème. 
