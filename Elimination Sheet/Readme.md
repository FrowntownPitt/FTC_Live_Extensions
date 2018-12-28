##Elimination Sheet

This extension will generate an elimination "bracket" webpage that can be printed directly.  It uses the [FTC Live Scoring API ](https://github.com/FIRST-Tech-Challenge/scorekeeper)
to fetch the elimination alliances.

### How to use
You will need to update `Configuration.ini` to your use-case.  The config names self-explanatory.

All you have to do is run `elimination_alliances_sheet.py` after alliance selection is finished and it'll open the result in 
your default browser.  It'll print in portrait in the default scaling (shrink to fit).

The `*.austl` file is a template ("**Aus**tin's **t**emplate **l**anguage") that has `#{}` markers to be replaced.  These will be replaced
by the `elimination_alliances_sheet.py` program before it saves the result.

#### Features
There are sections for each semifinal and the final lineup.  Both semifinals will be prepopulated with data from the FTC Live 
scoring software.  The Final section allows you to write in the teams that advanced.

Under each alliance there are checkboxes to mark which teams participated in which round.

There is a box between the alliances to mark the results of each match.

#### For the Future
Currently if an event has only 2-team elimination alliances then the Second pick number slot will be blank.  I'd like to 
some day remove that slot entirely so the Captain and First pick take up the entire section.