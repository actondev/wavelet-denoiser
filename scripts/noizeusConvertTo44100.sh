#!/bin/bash

# known issue: the denoiser works better with 44100 files
# that's why we go through that :)

NOIZEUS_DIR="../dataset/noizeus";
outputDir="../dataset/noizeus44100";

mkdir $outputDir

subdirs=$(ls $NOIZEUS_DIR/*/ -d)

possibleSubDirs="clean 0dB 5dB 10dB 15dB"

function convertFilesToWav44100()
{
  dir=$1
  files=$(ls $dir/*.wav)

  for file in $files; do
    dirName=$(dirname $file)
    baseName=$(basename $file)
    targetName="${baseName}.wav";
    targetPath="${outputDir}/${baseName}"
    if [  -e $targetPath ]; then
        continue;
    fi

    echo "converting $file"
    echo "target path $targetPath"
    ffmpeg -i $file -vn -acodec pcm_s16le -ac 1 -ar 44100 -f wav $targetPath -n &> /dev/null
  done
}

for possibleSubDir in  $possibleSubDirs; do
    dir="$NOIZEUS_DIR/$possibleSubDir";
    if [ -e "$dir" ]; then
        convertFilesToWav44100 $dir
    fi
done
