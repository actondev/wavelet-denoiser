function addTakeFromFileName (fileName)
    item = reaper.GetSelectedMediaItem(0, 0)
    source = reaper.PCM_Source_CreateFromFile(fileName)
    -- filenamebuf = reaper.GetMediaSourceFileName(source, "")
    -- reaper.ShowConsoleMsg("here: " .. filenamebuf)
    take = reaper.AddTakeToMediaItem(item)
    reaper.SetMediaItemTake_Source(take, source)
    reaper.SetActiveTake(take)
end

item = reaper.GetSelectedMediaItem(0, 0)
take = reaper.GetMediaItemTake(item, 0)
source = reaper.GetMediaItemTake_Source(take)
takeName = reaper.GetTakeName(take)
addTakeFromFileName(takeName)
reaper.UpdateItemInProject(item)
-- rebuild peaks for selected items
reaper.Main_OnCommand(40441, 0)