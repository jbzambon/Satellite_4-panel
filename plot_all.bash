#!/bin/bash
# 
# Program to get NOAA-16 data from AWS
# Joseph B. Zambon
# 4 April 2019

src='publicAWS:noaa-goes16/ABI-L2-MCMIPC/'
dest=`pwd`

count=0

png_count=0
for yyyy in 2018; do
    for ddd in 326; do
        for hh in 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 ; do
            echo $yyyy$ddd$hh
            for file in `rclone ls $src$yyyy"/"$ddd"/"$hh"/"`; do
              count=$((count+1))
              modulo=$(( $count  % 2 ))
              if [ "$modulo" -eq "0" ]; then
                echo $file
                `rclone copy $src$yyyy"/"$ddd"/"$hh"/"$file $dest`
                python -W ignore GOES_all_regional.py $dest'/'$file
                `rm -rf $dest"/"$file`
                `mv ${file%".nc"}".png" $(printf "%04d" $png_count)".png"`
                png_count=$((png_count+1))
              fi
            done
        done
    done
    for ddd in 327; do
        for hh in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 ; do
            echo $yyyy$ddd$hh
            for file in `rclone ls $src$yyyy"/"$ddd"/"$hh"/"`; do
              count=$((count+1))
              modulo=$(( $count  % 2 ))
              if [ "$modulo" -eq "0" ]; then
                echo $file
                `rclone copy $src$yyyy"/"$ddd"/"$hh"/"$file $dest`
                python -W ignore GOES_all_regional.py $dest'/'$file
                `rm -rf $dest"/"$file`
                `mv ${file%".nc"}".png" $(printf "%04d" $png_count)".png"`
                png_count=$((png_count+1))
              fi
            done
        done
    done
    for ddd in 328; do
        for hh in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 ; do
            echo $yyyy$ddd$hh
            for file in `rclone ls $src$yyyy"/"$ddd"/"$hh"/"`; do
              count=$((count+1))
              modulo=$(( $count  % 2 ))
              if [ "$modulo" -eq "0" ]; then
                echo $file
                `rclone copy $src$yyyy"/"$ddd"/"$hh"/"$file $dest`
                python -W ignore GOES_all_regional.py $dest'/'$file
                `rm -rf $dest"/"$file`
                `mv ${file%".nc"}".png" $(printf "%04d" $png_count)".png"`
                png_count=$((png_count+1))
              fi
            done
        done
    done
    for ddd in 329; do
        for hh in 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 ; do
            echo $yyyy$ddd$hh
            for file in `rclone ls $src$yyyy"/"$ddd"/"$hh"/"`; do
              count=$((count+1))
              modulo=$(( $count  % 2 ))
              if [ "$modulo" -eq "0" ]; then
                echo $file
                `rclone copy $src$yyyy"/"$ddd"/"$hh"/"$file $dest`
                python -W ignore GOES_all_regional.py $dest'/'$file
                `rm -rf $dest"/"$file`
                `mv ${file%".nc"}".png" $(printf "%04d" $png_count)".png"`
                png_count=$((png_count+1))
              fi
            done
        done
    done
    for ddd in 330; do
        for hh in 00 01 02 03 04 05 ; do
            echo $yyyy$ddd$hh
            for file in `rclone ls $src$yyyy"/"$ddd"/"$hh"/"`; do
              count=$((count+1))
              modulo=$(( $count  % 2 ))
              if [ "$modulo" -eq "0" ]; then
                echo $file
                `rclone copy $src$yyyy"/"$ddd"/"$hh"/"$file $dest`
                python -W ignore GOES_all_regional.py $dest'/'$file
                `rm -rf $dest"/"$file`
                `mv ${file%".nc"}".png" $(printf "%04d" $png_count)".png"`
                png_count=$((png_count+1))
              fi
            done
        done
    done

done
foo=${foo%"$suffix"}
