#!/bin/bash

dir_path="$1"

if [[ ! -d "$dir_path" ]]; then
    echo "Directory does not exist."
    exit 1
fi

cd "$dir_path"

total_duration=0
for file in *.wav; do
    if [[ -f "$file" ]]; then
        duration=$(soxi -D "$file" | cut -d'.' -f1)  
        total_duration=$((total_duration + duration))
    fi
done

minutes=$((total_duration / 60))
seconds=$((total_duration % 60))

echo "Total duration for $dir_path: $(printf "%02d:%02d" $minutes $seconds)"

