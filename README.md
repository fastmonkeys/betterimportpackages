![Better Import Packages](http://i.imgur.com/a9qAFGw.png)

Sublime Text 3 plugin that helps with Python imports. It scans the open folders for imports that were used previously and uses them to write the correct import. Please note that the plugin is just a prototype at this stage.


## How to use it
1. Select the class or function you wish to import (e.g. *UserPhoto*) and either right-click "Add import" or use the keybinding Cmd+Shift+I.
![Screenshot](http://i.imgur.com/UKkmgCW.png)

2. The import is then added to top of the file.
![Screenshot](http://i.imgur.com/D4vqajY.png)

## How to install
1. Open your terminal. At first you'll have to install `ack`.

  - For Mac users:
  ````$ brew install ack````
  - For Debian/Ubuntu users:
  ````$ sudo apt-get install ack````

2. Clone the repository to the Sublime Text Packages folder.

  ````
$ cd ~/Library/Application\ Support/Sublime\ Text\ 3/Packages/
$ git clone https://github.com/fastmonkeys/betterimportpackages BetterImportPackages
  ````
