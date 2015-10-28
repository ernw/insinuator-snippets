# Installation

1. Download Firefox x86 as an __archive__ and unzip it, e.g. in your home folder
1. Download JRE x86 as an __archive__ and unzip it, e.g. in your home folder
1. Download webex.sh or clone this repository
1. Modify the paths in webex.sh to point to the folders of Firefox x86 and JRE x86.
1. Source webex.sh
  * E.g. put `source <path/to/webex.sh>` in your .bashrc. This will load it automatically.

__Please note:__ There is no need to uninstall Firefox or JRE if you have any version of it installed. Also Firefox and JRE won't be auto-updated by your package manager, so you should check both for updates on a regular base.

# Usage
To start your WebEx session first close Firefox (the script tries to detect if Firefox is running and will ask you to close it). Then just open a terminal and run `webex` (Be sure to source webex.sh first! See installation above)

# What this script will do
At the time the post was created, WebEx was able to run 'smoothly' on Linux with 32bit versions of both Firefox and JRE. Essentially this script will just do that: It will put a symlink to the x86 plugin into Firefox' plugin folder and launch x86 Firefox. After Firefox is closed again, it will remove the symlink and you can work with your favorite version of your favorite browser again. :wink:
