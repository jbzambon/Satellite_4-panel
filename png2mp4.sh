#!/bin/sh
#

# utility script to combine ordered pngs into a mp4 animation
#
# 21 June 2011
# Updated: 27 August 2015

#desired framerate of movie (frames/sec)
r=30

#backup files for safekeeping
#mkdir backup
#cp $1"_*.png" backup/
#echo "Done Backing up"

iter=1
for f in *.png;
do
  echo "Processing $f file.."
  if [ $iter -eq 1 ]; then
    #desired image width, sanity check for even numbers
      w=`identify -format "%w" $f`
        if [ `expr $w % 2` -eq 1 ]; then
           w=`expr $w - 1`
        fi
    #desired image height, sanity check for even numbers
      h=`identify -format "%h" $f`
        if [ `expr $h % 2` -eq 1 ]; then
           h=`expr $h - 1`
        fi
  fi
  conf_file=`printf %04d $iter`
  echo $conf_file
  convert -background white -flatten -resize "$w"x"$h"\! -quality 100 $f `printf %04d $iter`.jpg
  convert `printf %04d $iter`.jpg \( ncsu_logo.jpg -resize 125x60^ \) -gravity northwest -geometry +5+5 -composite -quality 100 `printf %04d $iter`.jpg
  convert `printf %04d $iter`.jpg \( oomg_logo.jpg -resize 199x59^ \) -gravity northeast -geometry +5+5 -composite -quality 100 `printf %04d $iter`.jpg
  iter=`expr $iter + 1`
done

ffmpeg -r 30 -i %04d.jpg -c:v libx264 -crf 23 -profile:v baseline -level 3.0 -pix_fmt yuv420p -c:a aac -ac 2 -b:a 128k -movflags faststart -s $w"x"$h $1.mp4
