# Exported Songstatus by Synthriders

When a new game session with a song is started, the game automatically outputs the song status to a file. This file is then used by the Discord Rich Presence to show the current song status.

When the session is over, the game will empty the `SongStatusOutput.txt` file, which means the RPC tool will watch for changes in the file and update the Discord status accordingly.

## Song Status  Config file

Path: "C:\Program Files (x86)\Steam\steamapps\common\SynthRiders\SynthRidersUC\SongStatus.txt"

Possible values for the config file are:

- {{SongName}} - Name of the current song
- {{SongAuthor}} - Artist of the current song
- {{Difficulty}} - Current difficulty being played
- {{Beatmapper}} - Mapper of the current song
- {{CoverImage}} - Tells song status to generate a cover image if available

Example config File

````
{{SongName}} by {{SongAuthor}}
{{Difficulty}} (mapped by {{Beatmapper}})
{{CoverImage}
````

## Example Output

C:\Program Files (x86)\Steam\steamapps\common\SynthRiders\SynthRidersUC\SongStatusOutput.txt

````

Official song:

````

Automatic Call by NINA
Master (mapped by OST)

````

Custom song:

````

E.T. by QUATTROTEQUE & Rayyea
Master (mapped by Sodapie & SpaceTrace)

`````

Cover file path: "C:\Program Files (x86)\Steam\steamapps\common\SynthRiders\SynthRidersUC\SongStatusImage.png"