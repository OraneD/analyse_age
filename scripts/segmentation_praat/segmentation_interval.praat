form: "process files"
    text: "directoryPath", "D:\\Memoire\\corpus_mfa\\ESLO2_ENT_1002\\"
endform
printline 'directoryPath$'
Create Strings as file list: "files$", directoryPath$ + "*.wav"

nstrings = Get number of strings

for i from 1 to nstrings
    soundFile$ = Get string: i
    dotPosition = rindex(soundFile$, ".")
    baseName$ = left$(soundFile$, dotPosition - 1)
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
       startTime = Get starting point: tierNumber, intervalNumber
       endTime = Get end point: tierNumber, intervalNumber
       duration = endTime - startTime
       appendInfoLine: duration, label$

        Create TextGrid: 0, duration, "tier", ""
        Set interval text: 1, 1, label$
	Save as text file: directoryPath$ + baseName$ + "_" + string$(intervalNumber) + ".TextGrid"

	selectObject: "Sound " +  baseName$
	Extract part: startTime, endTime, "rectangular", 1, "no"
	Save as WAV file: directoryPath$ + baseName$ + "_" + string$(intervalNumber) + ".wav"



	
    endfor
endfor