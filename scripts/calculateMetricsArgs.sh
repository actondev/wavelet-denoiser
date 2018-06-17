#!/bin/bash

# Script to calculate the denoiser performance over one particualr noised file from the noizeus dataset
# 
# example  usage
# ./calculateMetricsArgs.sh --denoised=./noizeus-denoised/sp01_airport_sn5*.wav --source=./noizeus44100/

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
CMD_METRIC_NOISED="python3 python/metric-cci.py --a=\"$noisedFile\" -b=\"$cleanFile\""
metricNoised=$($CMD_METRIC_NOISED)

# echoing for emacs output :)

echoInfoBeforeTable $(basename $cleanFile) $(basename $noisedFile) $metricNoised
echoTableHeader

for denoisedFile in $denoisedFiles; do
    params=`getParamsFromDenoisedFileName $denoisedFile`
    # echo "params: $params"
    noisedName=$(getNoisedNameFromDenoisedFile $denoisedFile)
    cleanFile=$(getCleanFilePathFromDenoisedFile $denoisedFile)
    CMD_METRIC_DENOISED="python3 python/metric-cci.py --a=\"$denoisedFile\" -b=\"$cleanFile\""
    # echo running $CMD
    metricDenoised=$($CMD_METRIC_DENOISED)
    # echo "$params: $metric"
    echoTableParamsWithMetric $params $metricDenoised
done
