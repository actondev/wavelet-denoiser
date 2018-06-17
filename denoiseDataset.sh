#!/bin/bash

NOISIFIED_DIR="./dataset/noisified";
OUTPUT_DIR="./dataset/denoised";
VERBOSE=1
DELIMITER="----------------------------"

ARG_A="2"; # default 2
ARG_B="1"; # default 1
ARG_C="1"; # default 1
ARG_D="0.1"; # default 0.1
ARG_AKG="2 4"; #ak filter grad: default 4
ARG_AKO="1 2"; #ak filter offset: default 2
ARG_AKS="asc"; #ak filter slope: default asc
ARG_TYPE="1 2"; # default 1 ?? or 2??


# creating the output folder for our noisified files
mkdir $OUTPUT_DIR

# clear the folder (if there were files there before)
rm $OUTPUT_DIR/*.wav

sourceFiles=$(ls $NOISIFIED_DIR/*.wav)

if [ -z "$sourceFiles" ]; then
  echo "please create the noisified dataset first!";
  exit
fi

SECONDS=0

counter=0

function denoiseFile()
{
  a=$1
  b=$2
  c=$3
  d=$4
  akg=$5
  ako=$6
  aks=$7
  type=$8

  counter=$(($counter+1))

  denoisedFile="$OUTPUT_DIR/${baseNameWithoutExtension}(a=${a},b=${b},c=${c},d=${d},akg=${akg},ako=${ako},aks=${aks},type=${type}).wav"
  denoisedFile=`realpath $denoisedFile`

  CMD="python python/denoiser-argument.py --file=\"$file\" -a=$a -b=$b -c=$c -d=$d -akg=$akg -ako=$ako -aks=$aks -type=$type -o=$denoisedFile"
  out=$($CMD)&
  if [ $VERBOSE -gt 0 ]; then
    echo "$DELIMITER"
    echo "a:$a b:$b c:$c d:$d akg:$akg ako:$ako aks:$aks type:$type"
    echo " >> running $CMD .."
    if [ $VERBOSE -eq 2 ]; then
      echo "$out"
    fi
    echo "$DELIMITER"
  fi
}

COMMAND_DENOISE="python denoiser-argument -f "

for file in $sourceFiles; do
  echo "$DELIMITER"
  baseNameWithoutExtension=$(basename "$file" .wav)
  echo "denoising $baseNameWithoutExtension"
  for a in $ARG_A; do
    for b in $ARG_B; do
      for c in $ARG_C; do
        for d in $ARG_D; do
          for akg in $ARG_AKG; do
            for ako in $ARG_AKO; do
              for aks in $ARG_AKS; do
                for type in $ARG_TYPE; do
                  denoiseFile $a $b $c $d $akg $ako $aks $type
                done
              done
            done
          done
        done
      done
    done
  done
done

wait

echo "done, created $counter files in $SECONDS seconds"