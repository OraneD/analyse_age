form: "process files"
    text: "directoryPath", "D:\\Memoire\\module_entretiens\\ESLO2_ENT_1082\\"
    sentence: "idLoc", "MX953"
endform
printline 'directoryPath$'
Create Strings as file list: "files$", directoryPath$ + "*.wav"

nstrings = Get number of strings

for i from 1 to nstrings
    soundFile$ = Get string: i
    dotPosition = rindex(soundFile$, ".")
    baseName$ = left$(soundFile$, dotPosition - 1)
    printline "basename:" / 'baseName$'
    textGridFile$ = directoryPath$ + baseName$ + "_C.TextGrid"
    outputWavFile$ = "D:\\Memoire\\corpus_1_tier\\" + baseName$ + "\\" + baseName$ + "_T1.wav"
    outputTextGridFile$ = "D:\\Memoire\\corpus_1_tier\\" + baseName$ + "\\" + baseName$ + "_T1.TextGrid"

####################################################
    Read from file: directoryPath$ + soundFile$
    Read from file: textGridFile$
    new_grid = Create TextGrid: 0, 0.01, "Tier1", ""


#### Loop through tiers to extract them
   selectObject: "TextGrid " + baseName$ + "_C"
   numberOfTiers = Get number of tiers
   for tier to numberOfTiers
	selectObject: "TextGrid " + baseName$ + "_C"
	tierName$ = Get tier name:  tier
	printline : 'tierName$'
	if tierName$ ==  idLoc$
	     tierNum = tier
	     Extract one tier: tier
	     tierLoc= selected()
	     nbintervals = Get number of intervals: 1
	endif
	if tierName$ == "Turns"
		Extract one tier: tier
		tierTurns= selected()
	endif
    endfor
############ Sound 
    selectObject: "Sound " + baseName$
    plusObject: "TextGrid " + baseName$ + "_C"
    Extract non-empty intervals: tierNum, "no" 
#PAS OUBLIER DE CHANGER LINTERVALLE POUR CHAQUE FICHIER ICI
    Concatenate
    Save as WAV file: outputWavFile$
    Remove



################
	    for interval from 1 to nbintervals
			selectObject: tierLoc
			intervalLabel$ = Get label of interval: 1,interval
			selectObject: tierTurns
			
			if intervalLabel$ <> "" 
				selectObject: tierLoc
				startTime = Get starting point: 1,interval
				endTime = Get end point: 1,interval
				selectObject: tierTurns
				turnInterval= Get interval at time: 1, startTime
				turnLabel$ = Get label of interval: 1, turnInterval
				if turnLabel$ == idLoc$
					selectObject: tierLoc
					extract_Text = Extract part: startTime, endTime, "no"
					select 'new_grid'
				
					plus 'extract_Text'
				
					new_grid = Concatenate
					removeObject: extract_Text

					appendInfoLine: startTime, intervalLabel$, endTime

				endif
				if turnLabel$ <> idLoc$

					selectObject: tierTurns
					extract_Text = Extract part: startTime, endTime, "no"
					select 'new_grid'
				
					plus 'extract_Text'
				
					new_grid = Concatenate
					removeObject: extract_Text

					appendInfoLine: startTime, intervalLabel$, endTime
			        endif
			 endif

		endfor

    selectObject: "TextGrid chain"
    Save as text file: outputTextGridFile$
    Remove
endfor 

########Clear the object window
select all
Remove
#############

#######View the 2 files created (doesn't work if script launched via command line)
Read from file: outputWavFile$
Read from file: outputTextGridFile$
selectObject: "Sound " + baseName$ + "_T1"
plusObject: "TextGrid " + baseName$ + "_T1"
View & Edit

#######Command line (windows prompt)
#C:\\Progam Files\\Praat.exe path\to\script.praat path\to\directory IDlocuteur
#Praat.exe D:\\Memoire\\scripts\\tiers_without_overlaps.praat D:\\Memoire\\module_entretiens\\ESLO2_ENT_1006\\ OS6
