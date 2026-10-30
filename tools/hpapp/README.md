# App container template

`template.hpapp` is the 124-byte app-settings file used for HP PPL applications. It is copied unchanged from the [Xprime](https://github.com/Insoft-UK/Xprime) project's "PPL Application" template, commit `d79081d`, and Xprime's own example apps (for example *Shuttle*) ship the same file. Xprime is MIT licensed; its license is in `LICENSE-xprime.md`.

`tools/build_calc_files.py` writes this file, unchanged, into `SUPERSUB.hpappdir`. The program goes alongside it as `SUPERSUB.hpappprgm`, and the build also writes the note and the icon.
