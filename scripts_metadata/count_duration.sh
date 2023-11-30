#!/bin/bash

parent_dir="$1"
csv_file="$2"

temp_csv=$(mktemp)
echo "name_of_directory,age,time,time_loc" > "$temp_csv"

while IFS= read -r line || [[ -n "$line" ]]; do
    dir_name=$(echo "$line" | cut -d',' -f1)

    if [[ -d "$parent_dir/$dir_name" ]]; then
        cd "$parent_dir/$dir_name"
        
        total_duration=0
        for file in *.wav; do
            if [[ -f "$file" ]]; then
                duration=$(soxi -D "$file" | cut -d'.' -f1)  
                total_duration=$((total_duration + duration))
            fi
        done

        minutes=$((total_duration / 60))
        seconds=$((total_duration % 60))

        echo "Total duration for $dir_name: $(printf "%02d:%02d" $minutes $seconds)"
        echo "${line%?},$(printf "%02d:%02d" $minutes $seconds)" >> "$temp_csv"
        cd - > /dev/null
    else
        echo "${line%?}," >> "$temp_csv"
    fi
done < "$csv_file"

mv "$temp_csv" "$csv_file"



