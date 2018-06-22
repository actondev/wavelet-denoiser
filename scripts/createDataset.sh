#!/bin/bash

SOURCE_FILES_DIR="./dataset/source/*.wav";
NOISE_FILES_DIR="./dataset/noise/*.wav";
OUTPUT_FOLDER="./dataset/noisified/";
SNRS="0 6 12";

# creating the output folder for our noisified files
mkdir $OUTPUT_FOLDER

# clear the folder (if there were files there before)
rm $OUTPUT_FOLDER/*

pwd=$(pwd)
echo "pwd $pwd"
sourceFiles=$(ls $SOURCE_FILES_DIR)
noiseFiles=$(ls $NOISE_FILES_DIR)

for sourceFile in $sourceFiles; do
  echo "source $sourceFile"
	for noiseFile in $noiseFiles; do
    echo "noise $noiseFile"
		for snr in $SNRS; do
			python src/noisify.py --source "$sourceFile" --noise "$noiseFile" --snr "$snr" --output "$OUTPUT_FOLDER"
		done
	done
done
