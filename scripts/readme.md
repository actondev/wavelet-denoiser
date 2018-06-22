## Running the tests
Just run `python3 -m unittest discover -v -s ./test -p '*test*.py'`

### Windows fix
If you are on windows, and your executable to run `python` is.. `python` (even though it's version 3) then using `git bash`:
- `which python`
  will tell you the path of the executable for the python
- make sure `python -V` shows version 3
- `ln -s /path/of/python/from/which/python/command ~/bin`
- edit the environment variables for your current user, and add the `C:\users\USERNAME\bin` there

For example, I had to run `ln -s /c/Python36/python.exe ~/bin/python3.exe`

## Scripts provided

 - noizesDataset.sh \
    downloads the noizeus dataset available at http://ecs.utdallas.edu/loizou/speech/noizeus/

- noizeusConvertTo44100.sh \
    Uses ffmpeg to convert the noizeus dataset wav files to 44100 samplerate (to fix the know issue - so far - of getting better results with our current python code when samplerate is 4100)

    Note: to use it on windows
    - download ffmpeg from https://ffmpeg.zeranoe.com/builds/
    - use `git bash` or `cygwin` and run `ln -s /path/that/ffmpeg.exe/resides ~/path/that/is/in/your/PATH`. The second path should be a directory that on your path.
        > You can see your path by running `echo $PATH`
    

- applyDenoiserCombo.sh \
    Self explained :) Applies the denoiser to a set of files. For each file it will apply the denoiser with a combination of parametsrs.

    Edit the script file to change the arguments that will be passed to the denoiser

    > example call `./applyDenoiserCombo.sh --noise=../dataset/noizeus44100/sp01*sn5.wav --out=../dataset/noizeus-denoised`

- noizeusMetrics.sh \
    Calculates the denoiser performance over a collection of denoised files from the noizeus dataset. To be used (ideally) after running the `applyDenoiserCombo.sh`
