form: "process files"
    text: "directoryPath", "D:\\Memoire\\corpus_1_tier\\ESLO2_ENT_1001\\"
endform
printline 'directoryPath$'
Create Strings as file list: "files$", directoryPath$ + "*.wav"

nstrings = Get number of strings

avg = 0

for i from 1 to nstrings
    soundFile$ = Get string: i
    dotPosition = rindex(soundFile$, ".")
    baseName$ = left$(soundFile$, dotPosition - 1)
    printline "basename:" / 'baseName$'
    textGridFile$ = directoryPath$ + baseName$ + ".TextGrid"


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
       avg = avg + duration



	
    endfor
	avg = avg / numberOfIntervals
	appendInfoLine: avg
endfor