form: "process files"
    text: "directoryPath", "D:\\Memoire\\module_entretiens\\ESLO2_ENT_1002\\"
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
    outputWavFile$ = directoryPath$ + baseName$ + "_T1.wav"
    outputTextGridFile$ = directoryPath$ + baseName$ + "_T1.TextGrid"

    Read from file: directoryPath$ + soundFile$
    Read from file: textGridFile$
    selectObject: "Sound " + baseName$
    plusObject: "TextGrid " + baseName$ + "_C"
    Extract non-empty intervals: 3, "no"
    Concatenate

    Save as WAV file: outputWavFile$


new_grid = Create TextGrid: 0, 0.01, "Tier1", ""

selectObject: "TextGrid " + baseName$ + "_C"

numberOfTiers = Get number of tiers

for tier to numberOfTiers
	selectObject: "TextGrid " + baseName$ + "_C"
	tierName$ = Get tier name:  tier
	printline : 'tierName$'
	if tierName$ ==  "RL2"
	     Extract one tier: tier
	     tierLoc= selected()
	     nbintervals = Get number of intervals: 1


	    for interval from 1 to nbintervals
			selectObject: tierLoc
			intervalLabel$ = Get label of interval: 1,interval
			if intervalLabel$ <> ""
				startTime = Get starting point: 1,interval
				endTime = Get end point: 1,interval
				extract_Text = Extract part: startTime, endTime, "no"
				select 'new_grid'
				
				plus 'extract_Text'
				
				new_grid = Concatenate

				
				
				appendInfoLine: startTime, intervalLabel$, endTime

			endif
		endfor
	endif
endfor

    selectObject: "TextGrid chain"
    Save as text file: outputTextGridFile$
endfor



