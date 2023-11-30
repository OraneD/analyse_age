#!/urs/bin/bash
#set -o xtrace
entretiens="."
trs_files=$(find $entretiens -name '*.trs')  
trs_files_no_ext=$(echo $trs_files | sed 's/\.trs//g')
echo $trs_files_no_ext
for file in $trs_files_no_ext; do                                                   
   perl trs_to_tg.pl "${file}.trs">"${file}.TextGrid"
	echo $file transcrit                                                  
done
#find -name "*.trs" -exec perl trans2praat.pl {} done/{}.TextGrid \;   

