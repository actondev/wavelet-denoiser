import subprocess
import os

activeItem = None
activeTake = None


def getActiveItem():
    global activeItem
    if activeItem == None:
        activeItem = RPR_GetSelectedMediaItem(0, 0)
    return activeItem


def getActiveTake():
    global activeTake
    if activeTake == None:
        activeTake = RPR_GetMediaItemTake(getActiveItem(), 0)
    return activeTake


def msg(m):
    RPR_ShowConsoleMsg(m + "\n")


def getActiveFileName():
    item = getActiveItem()
    take = getActiveTake()
    source = RPR_GetMediaItemTake_Source(take)
    (source, fileName, filenamebuf_sz) = RPR_GetMediaSourceFileName(source, "", 1024)
    return fileName


def getNoisePeriod():
    (_isSet, _isLoop, startTime, endTime,
     _allowautoseek) = RPR_GetSet_LoopTimeRange(False, False, 0, 0, False)
    if(endTime == 0.0):
        return (0, 0)
    itemPosition = RPR_GetMediaItemInfo_Value(getActiveItem(), "D_POSITION")
    noiseStart = startTime - itemPosition
    noiseEnd = endTime - itemPosition
    return (noiseStart, noiseEnd)


# since addSourceAsTakeToItem from fileName is not working, hack:
def nameTakeAs(fileName):
    item = getActiveItem()
    activeTake = getActiveTake()
    takeName = RPR_GetTakeName(activeTake)
    (_retval, _take, _paramName, _stringNeedBig, _setnewvalue) = RPR_GetSetMediaItemTakeInfo_String(
        activeTake, "P_NAME", fileName, True)


def addSourceAsTakeToItem(fileName):
    item = getActiveItem()
    activeTake = getActiveTake()
    source = RPR_PCM_Source_CreateFromFile(fileName)
    take = RPR_AddTakeToMediaItem(item)
    RPR_SetMediaItemTake_Source(take, source)


''' Returns the fileName of the denoised item, or false '''


def executeDenoiser(args):
    result = False
    runProcessArguments = list()
    runProcessArguments.append("python")
    runProcessArguments.append("D:/Auth/git-diplo/python/denoiser-argument.py")
    for key, value in args.items():
        runProcessArguments.append(key)
        runProcessArguments.append(value)
    # msg(" ".join(runProcessArguments))
    proc = subprocess.Popen(runProcessArguments, stdout=subprocess.PIPE)
    lines = list()
    for line in proc.stdout:
        lineParsed = line.decode("utf-8").replace("\r\n", "")
        # msg(lineParsed)
        lines.append(lineParsed)
    numLines = len(lines)
    if numLines >= 2:
        # second to last should be OK, and last should have the denoised
        # filename
        if lines[numLines - 2] == "OK":
            result = lines[numLines - 1]
    return result


''' 
	Gets input from the user about the denoiser parameters
	API syntax:
	(Boolean retval, String title, Int num_inputs, String captions_csv, String retvals_csv, Int retvals_csv_sz)
		= RPR_GetUserInputs(title, num_inputs, captions_csv, retvals_csv, retvals_csv_sz) '''


def getUserInputs():
    # (_retval, _title, _num_inputs, _captions_csv, retvals_csv, retvals_csv_sz) = RPR_GetUserInputs("Denoiser parameters", 6, "a,b,c,d,ak grad,ak offset", "", 0)
    (_retval, _title, _num_inputs, _captions_csv, retvals_csv, retvals_csv_sz) = RPR_GetUserInputs(
        "Denoiser parameters", 7, "a,b,c,d,ak grad,ak offset, ak slope (asc or desc)", "2,1,1,0.1,4,2,asc", 64)
    # retvals_csv+= ","
    valuesSplitted = retvals_csv.split(",")
    argumentsArray = {}
    argumentsArray['-a'] = valuesSplitted[0]
    argumentsArray['-b'] = valuesSplitted[1]
    argumentsArray['-c'] = valuesSplitted[2]
    argumentsArray['-d'] = valuesSplitted[3]
    argumentsArray['-akg'] = valuesSplitted[4]
    argumentsArray['-ako'] = valuesSplitted[5]
    argumentsArray['-aks'] = valuesSplitted[6]
    return argumentsArray


def main():
    (noiseStart, noiseEnd) = getNoisePeriod()
    if noiseEnd == 0:
        msg("Please make a time selection stating the noise period")
        return
    fileName = getActiveFileName()
    args = getUserInputs()
    args['-f'] = "'" + fileName + "'"
    args['-t'] = "'" + str(noiseStart) + "-" + str(noiseEnd) + "'"
    denoisedFileName = executeDenoiser(args)
    # addSourceAsTakeToItem(denoisedFileName)
    nameTakeAs(denoisedFileName)

main()
