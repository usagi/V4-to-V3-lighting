# Optimized version Notes

This is an optimized version of the original code (https://github.com/benzhenwen/V4-to-V3-lighting) with some improvements and bug fixes mainly...

- fixup the input file JSON parsing
- auto set the = output file path if not provided (<input>.v3.dat)
- optimize for overall performance

---

## you should probably just use this ngl
https://converter.stormpacer.xyz/
# BeatSaber lightshow converter from v4.0.0 to v3.3.0
written in python 311, 3.9 or above required
## How to use
- get python v3.9 or later (duh): https://www.python.org/
- download converter.py and move it into your beatmap folder
- backup your map because I have no idea if this works lol
- run converter.py
- when prompted, provide the input file path. ex: lightshow.dat
- when prompted, provide the output file path. ex: ExpertPlusStandard.dat

the input file should be a v4.0.0 lightshow and the output file should be a v3.3.0 beatmap

the lightshow will be merged into the beatmap (but not deleted). if a non-existent file for output is selected, a new file will be created.

the output file will not contain optional properties (the file is quest compatable)
## Issues
me: ngl this is my first actual attempt at a proper repo. if you have any feedback about the script or my general lack of knowledge message me on discord @ ben208
(im sure there are issues, no way i wrote something that just works first try)
### Thanks
officialMECH for writing the documentation on the v4 lighting format and answering my endless questions about it
