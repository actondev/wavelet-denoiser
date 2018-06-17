## Installing the necessary modules

- pip3 install -r requirements.txt
  didn't work, pywavelets fails cause it need numpy..?
  `pip3 install numpy` and afterwards `pip3 install pywavelets` is ok

but then `import soundfile` causes an error `ImportError: No module named '_cffi_backend'`

trying
- `sudo apt-get install libffi-dev`
- `pi3 install cffi`

then, another error

`OSError: sndfile library not found`

trying `apt-get install libsndfile1`

for `matplotlib`
`apt-get install libpng12-dev libfreetype6-dev libxft-dev` (the libxft-dev is required for a server)
(maybe `pkg-config` is the needed package, which libxft-dev installs)