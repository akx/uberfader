# Uberfader

Concatenate and crossfade audio to form a very long sequence.

## Usage

* Create virtualenv
* Install requirements
* Point `uberfader` at a directory of WAV files and tell it the desired output length, e.g. 600 seconds:  
  `python3 uberfader.py -i ./bits/ -o ./long.wav -l 600`

## Caveats

* The underlying Pydub library exhibits quadratic behavior with long sequences. Instead of generating a very
  long sequence in a single run, you may have better luck generating a number of shorter ones first, then
  re-uberfading them. Use the `-n` parameter to have Uberfader generate N files (suffixed e.g. `long_0001.wav`)
  and then do `python3 uberfader.py -i ./long_sequences -o ./really-long.wav -l 3600` to generate the final sequence.
  Your audience probably won't realize what's happening.