# Set the paths to the audio and TextGrid files
audioFile$ = "../module_entretiens/ESLO2_ENT_1001/ESLO2_ENT_1001.wav"
textGridFile$ = "../module_entretiens/ESLO2_ENT_1001/ESLO2_ENT_1001_C.TextGrid"
#################################

#Opening files

Read from file: audioFile$
sound = selected("Sound")
Read from file: textGridFile$
textgrid = selected("TextGrid")

#################################

# Get interval names to create new textgrid

numberOfTiers = Get number of tiers
namesTiers$ = ""
for tier to numberOfTiers
	selectObject: textgrid
	tierName$ = Get tier name:  tier
	namesTiers$ = namesTiers$ + " " + tierName$
endfor


##################################
new_grid = Create TextGrid: 0, 0.01, namesTiers$, ""
new_sound = Create Sound from formula: "vLoc", 2, 0, 0.01, 44100, "0"
##################################

# Extrcat times from the tier we are interested in

for tier to numberOfTiers
	selectObject: textgrid
	tierName$ = Get tier name:  tier
	printline : 'tierName$'
	if tierName$ ==  "BV1"
	      nbintervals = Get number of intervals: tier


	    for interval from 1 to nbintervals
			selectObject: textgrid
			intervalLabel$ = Get label of interval: tier,interval
			if intervalLabel$ <> ""
				startTime = Get starting point: tier,interval
				endTime = Get end point: tier,interval
				appendInfoLine: startTime, intervalLabel$, endTime

###################################################

#Concatenate the TextGrid and audio extracts into one file
	
				preserve_time$ = "yes"
				extract_Text = Extract part: startTime, endTime, "no"
				select 'new_grid'
				plus 'extract_Text'
				new_grid = Concatenate

				selectObject: sound
				extract_Sound = Extract part: startTime, endTime, "rectangular", 1.0, "no"
				select 'new_sound'
				plus extract_Sound
				new_sound = Concatenate


			endif
	    endfor
	endif
endfor


