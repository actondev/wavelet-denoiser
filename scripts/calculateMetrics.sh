#!/bin/bash

# example call
# ./calculateMetrics.sh speech1 speech1_noised_white_snr0*

# changing the pwd to the script's location, for the ls line to work
cd "$(dirname "$0")"

SOURCE_FILE="./dataset/source/$1.wav";
DENOISIDED_FILES_DIR="./dataset/denoised/$2";

denoisedFiles=$(ls $DENOISIDED_FILES_DIR)

function getParamsFromDenoisedFileName()
{
    regex='.+\((.+)\)'    
    fileName=$1
    [[ $fileName =~ $regex ]]
    echo "${BASH_REMATCH[1]}"
}

function echoInfoBeforeTable()
{
    echo "Source file: =$SOURCE_FILE= \\\\"
    echo "Denoised files: =$DENOISIDED_FILES_DIR="
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

echoInfoBeforeTable
echoTableHeader
for denoisedFile in $denoisedFiles; do
    # [[ $denoisedFile =~ $regex ]]
    # echo "params are ${BASH_REMATCH[1]}"
    params=`getParamsFromDenoisedFileName $denoisedFile`
    CMD="python3 python/metric-cci.py --a=\"$SOURCE_FILE\" -b=\"$denoisedFile\""
    metric=$($CMD)
    # echo "$params: $metric"
    echoTableParamsWithMetric $params $metric
done
