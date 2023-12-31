# analyse s cog + pente

path$ = "D:\Memoire\corpus_mfa"
file_save$ = "resultats_corpus_mfa_avec_md.xls"
fileappend 'file_save$' locuteur'tab$'fichier'tab$'age'tab$'sexe'tab$'niveau_etude'tab$'profession'tab$'categorie_professionnelle'tab$'dizaine'tab$'phoneme'tab$'duree'tab$'cog'tab$'skew'newline$'

path_table$ = path$ + "\" + "metadonnees_ESLO2_ENT_ENTJEUN.txt"
table_md = Read Table from tab-separated file: path_table$
fichier_manquant = 0

folders_list = Create Strings as folder list: "folderList", path$

nb_folders = Get number of strings

for a from 1 to nb_folders
	printline 'a'/'nb_folders'
	select 'folders_list'
	folder$ = Get string: a

	select 'table_md'


	ligne_md = Extract rows where column (text): "directory", "is equal to", folder$
	age = Get value: 1, "age"
	dizaine = floor(age/10)*10

	sexe$ = Get value: 1, "sexe"
	niveau_etude$ = Get value: 1, "niveau_etude"
	profession$ = Get value: 1, "profession"
	categorie_professionnelle$ = Get value: 1, "categorie_professionnelle"

	
	path_file$ = path$ + "\" + folder$ + "\" + "*.wav"
	file_list = Create Strings as file list: "fileList", path_file$
	nb_files = Get number of strings


	for b from 1 to nb_files
		select 'file_list'
		file$ = Get string: b

		@ouverture_fichier

		if analyse = 1
			@analyse
		endif

	endfor


endfor



########################################################################
procedure ouverture_fichier

		full_path_wav$ = path$ + "\" + folder$ + "\" + file$
		full_path_grille$ = path$ + "\" + folder$ + "\"  + folder$ + "_aligned\" + file$ - ".wav" + ".TextGrid"

		if fileReadable(full_path_grille$)
			grille = Read from file: full_path_grille$
			son = Read from file: full_path_wav$
			select 'grille'
			
			analyse = 1

		else
			fichier_manquant = fichier_manquant + 1
			analyse = 0
		
		endif

endproc


########################################################################
procedure analyse

			nb_intervals = Get number of intervals: 2

			for c from 1 to nb_intervals
				select 'grille'
				label$ = Get label of interval: 2, c
				index_regex(label$,"")
			#	if index_regex("'label$'","[a-zA-Zçàùëêûüéè]")>0
			#	if label$ = "a"
				if label$ = ""
					label$ = "_"
				endif

				start = Get start time of interval: 2, c
				end = Get end time of interval: 2, c
				milieu = (end+start)/2
				duree = round((end-start)*1000)
				
				select 'son'
				extrait = Extract part: milieu-0.015, milieu+0.015, "Kaiser2", 1, "yes"
				spectre = To Spectrum: "yes"
				cog = Get centre of gravity: 2
				skew = Get skewness: 2


				fileappend 'file_save$' 'folder$''tab$''file$''tab$''age''tab$''sexe$''tab$''niveau_etude$''tab$''profession$''tab$''categorie_professionnelle$''tab$''dizaine''tab$''label$''tab$''duree''tab$''cog:2''tab$''skew:5''newline$'

				select 'extrait'
				plus 'spectre'
				Remove

			endfor	


select 'son'
plus 'grille'
#plus 'ligne_md'
Remove
#pause


endproc

##########################################################################





printline FINI !!! 'fichier_manquant'



