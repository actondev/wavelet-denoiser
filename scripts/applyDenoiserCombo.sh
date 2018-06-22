#!/bin/bash

# example  call
# to denoise all the noizeus files of speaker 1 (sp01) that is noisified at 5db snr
# ./applyDenoiserCombo.sh --noise=../dataset/noizeus44100/sp01*sn5.wav --out=../dataset/noizeus-denoised

DENOISER_COMMAND="python ../src/denoiser-argument.py"

# set the parameters that will be passed to the denoiser below
# space seperated values will mean that both will be applied
# note: if A has value of "2 4" and B of "1 2" then the denoiser will be applied for
# a=2,b=1 and a=2,b=2 and a=4,b=1 and a=4,b=2 ;)

ARG_A="2"; # default 2
ARG_B="1"; # default 1
ARG_C="1"; # default 1
ARG_D="0.1"; # default 0.1
ARG_AKG="2 4"; # ak filter grad: default 4
ARG_AKO="2"; # ak filter offset: default 2
ARG_AKS="asc desc"; # ak filter slope: default asc
ARG_TYPE="1 2"; # default 1 ?? or 2??

while [ $# -gt 0 ]; do
  case "$1" in
    --noise=*)
      noise="${1#*=}"
      ;;
    --out=*)
      out="${1#*=}"
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

VERBOSE=1
DELIMITER="----------------------------"


# creating the output folder for our noisified files
outDir=$out
mkdir $outDir

# clear the folder (if there were files there before)
rm $outDir/*.wav

sourceFiles=$(ls $noise)

echo "source files: $sourceFiles"

# exit

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

  denoisedFile="$outDir/${baseNameWithoutExtension}(a=${a},b=${b},c=${c},d=${d},akg=${akg},ako=${ako},aks=${aks},type=${type}).wav"
  denoisedFile=`realpath $denoisedFile`

  CMD="${DENOISER_COMMAND} -i=\"$file\" -a=$a -b=$b -c=$c -d=$d -akg=$akg -ako=$ako -aks=$aks -type=$type -o=$denoisedFile"
  out=$($CMD)
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