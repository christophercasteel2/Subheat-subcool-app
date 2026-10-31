# Calculator file templates

These two files give `tools/build_calc_files.py` the parts of an HP Prime file that do not depend on the program. Both were taken from an app file written by the HP Connectivity Kit that loads on firmware 2.4. Nothing program-specific is left in them.

- `container.bin` is an empty program file in the format current firmware uses: the 12-byte header, the three flag records, an empty function list, an empty source block named `Main`, and the 1004-byte trailer the Connectivity Kit writes. `tools/hpfile.py` fills in the function list and the source.
- `template.hpapp` is the 124-byte app-settings file that goes in an `.hpappdir` folder.

The layout of these files is described in the [Xprime](https://github.com/Insoft-UK/Xprime) project's notes (`hpprgmG2.md`). This project first used the older plain format (a 20-byte header followed by the source); those files did not show up on a G1 running firmware 2.4.2.
