#!/bin/bash


parent_dir="$1"
total_percentage=0
count=0
if [ -z "$parent_dir" ]; then
    echo "Please provide a parent directory."
    exit 1
fi


cd "$parent_dir" || { echo "Failed to change to directory $parent_dir"; exit 1; }

for dir in */; do

    cd "$dir" || continue

    cmd1_output=$(egrep -e "[Aa-Zz]+- " *.TextGrid 2>/dev/null | wc -l)

    cmd2_output=$(ls *.TextGrid 2>/dev/null | wc -l)

    if [ "$cmd2_output" -eq 0 ]; then
        echo "In directory $dir: Division by zero (No TextGrid files found)"
    else

		result=$(echo "scale=2; ($cmd1_output/$cmd2_output)*100" | bc)
        echo "In directory $dir: Result = $result%"
		echo "$cmd1_output - / $cmd2_output TextGrid"

        total_percentage=$(echo "$total_percentage + $result" | bc)
        count=$((count+1))
    fi

    cd ..
done

if [ $count -ne 0 ]; then
    average=$(echo "scale=2; $total_percentage / $count" | bc)
    echo "Average Percentage: $average%"
else
    echo "No TextGrid files processed."
fi
