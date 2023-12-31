form: "process files"
    text: "directoryPath", "D:\\Memoire\\module_diachronie\\diachronie_1_tier\\ESLO2_DIA_1222\\"
endform
printline 'directoryPath$'
Create Strings as file list: "files$", directoryPath$ + "*.wav"

nstrings = Get number of strings

for i from 1 to nstrings
    soundFile$ = Get string: i
    dotPosition = rindex(soundFile$, ".")
    baseName$ = left$(soundFile$, dotPosition - 1)
    folderbaseName$ = left$(soundFile$, dotPosition - 4)
    printline "basename:" / 'baseName$'
    textGridFile$ = directoryPath$ + baseName$ + ".TextGrid"
    outputWavFile$ = directoryPath$ + baseName$ + "_T1.wav"
    outputTextGridFile$ = directoryPath$ + baseName$ + "_T1.TextGrid"

    Read from file: directoryPath$ + soundFile$
    Read from file: textGridFile$

    selectObject: "TextGrid " + baseName$
    tierNumber = 1
    numberOfIntervals = Get number of intervals: tierNumber
    for intervalNumber to numberOfIntervals
       selectObject: "TextGrid " + baseName$
       label$ = Get label of interval: tierNumber, intervalNumber
       if index(label$, "+") <> 0
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'overlap'	
           appendInfoLine: duration, label$
       elif label$ == ""
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'empty string'	
           appendInfoLine: duration, label$
       elif label$ == " [rire] "
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'rire'	
           appendInfoLine: duration, label$
       elif label$ == " [bb] "
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'BB'	
           appendInfoLine: duration, label$
	elif label$ == " [pf] "
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'PF'	
           appendInfoLine: duration, label$
        elif label$ == " [i] "
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'i'	
           appendInfoLine: duration, label$
        elif label$ == " [b] "
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'b'	
           appendInfoLine: duration, label$
	elif label$ == " [tx] "
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
	   printline 'tx'	
           appendInfoLine: duration, label$
	
       else
           startTime = Get starting point: tierNumber, intervalNumber
           endTime = Get end point: tierNumber, intervalNumber
           duration = endTime - startTime
           appendInfoLine: duration, label$

           Create TextGrid: 0, duration, "tier", ""
           Set interval text: 1, 1, label$
	   Save as text file: "D:\\Memoire\\modules_ESLO\\module_diachronie\\diachronie_mfa_1channel\\" + folderbaseName$ + "\\" + baseName$ + "_" + string$(intervalNumber) + ".TextGrid"
	   Remove

	   selectObject: "Sound " +  baseName$
	   Extract part: startTime, endTime, "rectangular", 1, "no"
	   Save as WAV file: "D:\\Memoire\\modules_ESLO\\module_diachronie\\diachronie_mfa_1channel\\" + folderbaseName$ + "\\" + baseName$ + "_" + string$(intervalNumber) + ".wav"
           Remove
 
	endif
    endfor
endfor