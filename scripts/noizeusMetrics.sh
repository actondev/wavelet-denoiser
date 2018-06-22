#!/bin/bash

# Script to calculate the denoiser performance over a collection of denoised files from the noizeus dataset
# Note: it will output the results in a format ready to be used in org-mode of emacs (putting the results in a table)
# 
# example  usage
# ./metrics.sh --denoised=../dataset/noizeus-denoised/sp01_airport_sn5*.wav --source=../dataset/noizeus44100/
# the above command will calcute the metric for all the denoised files.
# It will try to find the clean file in the given source directory eg the sp01_airport_sn5(..denoiser params..).wav
#   will assume sp01_airport.wav as the source file

PYTHON_METRIC_CMD="python ../src/metric-cci.py"

while [ $# -gt 0 ]; do
  case "$1" in
    --denoised=*)
      denoised="${1#*=}"
      ;;
    --source=*)
      source="${1#*=}"
      ;;
    *)
      printf "***************************\n"
      printf "* Error: Invalid argument.*\n"
      printf "***************************\n"
      exit 1
  esac
  shift
done

# changing the pwd to the script's location, for the ls to work
cd "$(dirname "$0")"


function getNoisedNameFromDenoisedFile()
{
    fileName=$1
    baseName=$(basename $fileName)
    # getting the original noise from noizeus file: sp[number]_airport_sn[number]
    regex='(sp[0-9]+_[a-z]+_sn[0-9]+).+'
    # echo "$fileName"
    [[ $fileName =~ $regex ]]
    match="${BASH_REMATCH[1]}"
    # echo noise file
    echo "${match}"
}

function getParamsFromDenoisedFileName()
{
    regex='.+\((.+)\)'
    # regex='.+(a_[0-9].+).wav'    
    fileName=$1
    [[ $fileName =~ $regex ]]
    echo "${BASH_REMATCH[1]}"
}

function getCleanFilePathFromDenoisedFile()
{
    fileName=$1
    # getting the clean file from noizeus file: sp[number]_airport
    regex='(sp[0-9]+)'
    [[ $fileName =~ $regex ]]
    match="${BASH_REMATCH[1]}"
    echo "${source}/${match}.wav"
}

function echoInfoBeforeTable()
{
    echo "Clean file: =$1= \\\\"
    echo "Noised file: =$2= \\\\"
    echo "Noised file metric: =$3="
    echo ""
}

function echoTableHeader()
{
    echo "|parameters|metric|"
    echo "|----------|------|"
}

function echoTableParamsWithMetric()
{
    echo "|$1|$2|"
}


denoisedFiles=$(ls $denoised)

noisedName=$(getNoisedNameFromDenoisedFile $denoised)
noisedFile="${source}/${noisedName}.wav"
# echo "noisedFile $noisedFile"
cleanFile=$(getCleanFilePathFromDenoisedFile $denoised)
# echo "cleanFile $cleanFile"
CMD_METRIC_NOISED="${PYTHON_METRIC_CMD} --a=\"$noisedFile\" -b=\"$cleanFile\""
metricNoised=$($CMD_METRIC_NOISED)

# echoing for emacs output :)

echoInfoBeforeTable $(basename $cleanFile) $(basename $noisedFile) $metricNoised
echoTableHeader

for denoisedFile in $denoisedFiles; do
    params=`getParamsFromDenoisedFileName $denoisedFile`
    # echo "params: $params"
    noisedName=$(getNoisedNameFromDenoisedFile $denoisedFile)
    cleanFile=$(getCleanFilePathFromDenoisedFile $denoisedFile)
    CMD_METRIC_DENOISED="${PYTHON_METRIC_CMD} --a=\"$denoisedFile\" -b=\"$cleanFile\""
    # echo running $CMD
    metricDenoised=$($CMD_METRIC_DENOISED)
    # echo "$params: $metric"
    echoTableParamsWithMetric $params $metricDenoised
done
