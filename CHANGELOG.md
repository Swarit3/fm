
Log:


Fixed flickering: move the fucking renderer to only execute when key input detected.
Changed color scheme. Previous one looked like high contrast vomit.
Added a forced refresh system.
Fixed bottomtxt.
Improved bottomtxt update logic.
Added exception if file size/dir item count is unobtainable.
Fixed error message implementation. Any text persists until key input is recieved.

Added exception if directory is inaccessible.
Improved forced refresh system to allow specifying number of frames to force run. (temporary patch until main() gets reordered)
Imprtoved output and bottomtxt by centering it instead of '\t' spam.
Improved header and footer color.
Added message if Current Directory is empty.
Improved navigation exception to only handle specified errors.
Added exception when trying to enter a folder in an empty directory.
Added truncation in header when path is too long.
Added filename truncation to keep it inline.

Added special keys support.
Added modular reusable line-by-line input function.
Added basic bash functionality without output.
Added exception handling when current directory and/or one or more parent diretories are inaccessible or deleted.

Removed redundant/commented code.

First session on Windows.
Removed navinp function - Seperate input function appears an idea farfetched, with how much work (Enter) and (Exit) bottons take for directory navigation that becomes a liability when dealing with popups and text boxes.
Reordered main()..
Added Exit confirmation.
Redesigned perline scrnSIZE logic to be dynamic.
Added exception if user tries to navigate up and parent directory does not contain root directory.
Added clear screen for NT systems.

Transparent BG support.

Fixed popup menu items not showing up.
Added remove function.
Improved exception handling for current directory being deleted.
Removed clear before and after running program.
Added Delete operation.
Removed forced refresh implementation.
Added forcing refresh state via hidded bottomtxt.
Added debug logger for when the function is running.
Improved popup logic to limit subwindow size to scrnX and scrnY.
Added '~' to jump to home directory.
Added HOME and END keys to navigate to beginning and end of item list.
Improved scroll position calculation logic on moving up directories.
Improved code layout and factoring.
Improved PopUp appearance by adding borders.
Added parameter type specification when calling functions.
Fixed popup key input and update logic.
Improved comments; Removed unneeded profanity, old comments.
Added helper script testkeys.py to test keycodes.
Added helper script strip.py to compress file by removing comments and empty lines.
Moved LOG.md to CHANGELOG.md.

Improved input logic to be non blocking, significantly reducing CPU usage
