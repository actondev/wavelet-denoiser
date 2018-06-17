#!/bin/bash

# http://ecs.utdallas.edu/loizou/speech/noizeus/train_0dB.zip

# Available sounds:
# airport babble car exhibition restaurant street airport station
# sounds="airport babble car exhibition restaurant street airport station"
sounds="airport babble car exhibition restaurant"
# 0 5 10 and 15 available
# dbs="0 5 10"
dbs="0 5 10"

outputDir="./noizeus"

if [ ! -e "${outputDir}/clean.zip" ]; then
	echo "downloading clean.zip"
	wget "http://ecs.utdallas.edu/loizou/speech/noizeus/clean.zip" -P "$outputDir" -q
	echo "  ..extracting"
	unzip -d "$outputDir" -o "${outputDir}/clean.zip" > /dev/null
fi

for sound in $sounds; do
	for db in $dbs; do
		zipName="${sound}_${db}dB.zip"
		if [ ! -e "${outputDir}/${zipName}" ]; then
			echo "downloading $zipName"
			wget "http://ecs.utdallas.edu/loizou/speech/noizeus/${zipName}" -P "$outputDir" -q
			echo "  ..extracting"
			unzip  -d "$outputDir" -o "${outputDir}/${zipName}" > /dev/null
		fi
	done
done
