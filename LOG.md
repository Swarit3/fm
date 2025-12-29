
Log:

Fixed of popup menu items not showing up.

Fixed flickering: move the fucking renderer to only execute when key input detected.
Changed color scheme. Previous one looked like high contrast vomit.
Added a forced refresh system.
Fixed bottomtxt.
Improved bottomtxt update logic.
Added exception if file size/dir item count is unobtainable.
Fixed error message implementation. Any text persists until key input is recieved.

Added exception if directory is inaccessible.
Improved forced refresh system to allow specifying number of frames to force run. (temporary patch until main() gets reordered)
Centered output and bottomtxt instead of '\t' spam.
Improved header and footer color.
Added message if Current Directory is empty.
Fixed navigation exception to only handle specified errors.
Added exception when trying to enter a folder in an empty directory.
Added truncation in header when path is too long.
Added filename truncation to keep it inline.

Added special keys support.
Added modular reusable line-by-line input function.
Added basic bash functionality wirhout output.
Added exception handling when current directory and/or one or more parent diretories are inaccessible or deleted.

Removed redundant/commented code.

First session on Windows.
Removed navinp function - Seperate input function appears an idea farfetched, with how much work (Enter) and (Exit) bottons take for directory navigation that becomes a liability when dealing with popups and text boxes.
Reordered main()..
Implemented Exit confirmation.
Redesigned perline scrnSIZE logic to be dynamic.
Added exception if user tries to navigate up and parent directory does not contain root directory.
Added clear screen for NT systems.

Transparent BG support.
