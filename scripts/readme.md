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
