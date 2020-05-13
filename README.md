# Mass Rename Series Folders of a Sonarr library

I have not found an easy option to change the folder naming scheme of a tv library from within sonarr.
Since i don't want to have to do this by hand, i wrote this small tool to do this for me.

The configuration is done in a yaml file. This program assumes config.yml as the default configuration path.  
The configuration path can also be specified manually. An example can be seen in config-example.yml

Most options are configurable, but the new naming scheme has to be put in by hand. 
Unfortunately i did not see an api endpoint to get the currently configured folder naming scheme from sonarr.
Doing it by had is somewhat clunky, but i did not want to spend more time on it than i already did.

The naming scheme is specified in the variable `new_name_components`.  
This variable is a list of tuples. Each tuple has a string and a boolean.  
If the boolean is True then the the string is used to look up the corresponding value for the series.  
You can look up possible values in the sonarr api description.  
If the boolean is False then the string is used as is.  
All the name elements will be concatenated in the order of the list.

The script also supports the replacement of the space character with any other character(s).  
Space replacement is done on the series folder name only. It doesn't affect the rest of the library path.

The example configuration in this naming scheme: `Series_Name_(year)`

This program also supports moving the shows to a new library folder. 
This option does not check or change the permissions in the new library.

There is also an option to add the language to the library folder.  
I needed this option, because the emby developers don't seem to be interested in 
providing filtering based on audio language.  
This option needs sonarr v3 and reads the language profiles.  
The name of the language profile is added as a sub folder under the library root.

The new library root folder and any needed language profile sub folders have to exist before running the script.

This program has a gui and a command line interface. 
I have not done a lot of compatibility testing for the GUI or Windows, but it should work.
My library move was done on linux with the CLI.

Use `rename_shows.py --help` to get an overview of the available command line options.
Run rename_shows.py without any arguments to get the GUI version.
