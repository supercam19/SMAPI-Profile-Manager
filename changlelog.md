# SMAPI Profile Manager Changelog

## Update [v1.2.1] (???)

### Changes 
 - If the program tries to download files without an internet connection, an error popup will appear
 - Small program optimizations that should make the program load faster (#24)

### Fixes
 - Fixed the Last Played value not getting updated when launching a profile
 - Fixed the unmodded profile not launching when the Force SMAPI option was checked
 - Fixed the white gear icon having a blank gap in it

## Core Update [v1.2.0] (Jan 8, 2023)
A major update that focuses on core backend features of the program to improve user experience and make the program more reliable.

### Additions
 - Profiles can now be edited, and an editor has been added to the UI (#20)
 - The profiles list can now be sorted by name, date created, and date last played (#22)
 - Added a default profile that launches the game unmodded (#21)
 - Implemented a new way of loading and saving profiles, leading to fewer errors and less file clutter (#18)

### Changes
 - Mod profiles can now be imported from anywhere on your computer (#18)
 - The program will now start in the center of your screen
 - Mod profile information is now stored in a JSON file (#19)
 - Mod profile creation date and date last played are now tracked (#19)
 - Updated the preview image in the README

### Fixes
 - Fixed tooltips with small amounts of text being much wider than the text

## Round Tooltip Edges [v1.1.4] (Dec 27, 2022)
Fixed critical issue where the app window would not display properly if your display scaling was not set to 150%, aswell as finally added rounded edges to tooltips.

### Changes
 - Tooltips now have rounded edges (#16)
 - Made the colour of tooltips brighter so it won't blend in with the background

### Fixes
 - Fixed issue where the app window would not display properly if your display scaling was not set to 150% (#17)

## Update [v1.1.3] (Dec 24, 2022)
Very small update fixing issues with profile names and how they display in the program.

### Changes
 - Profile names are now limited to 100 characters
 - Profile names now have a tooltip incase their name is too long to fit in the window

### Fixes
 - Fixed long profiles names hiding the launch and delete buttons
 - Fixed profile names > ~20 characters not being aligned with shorter ones

## UI Update pt2 [v1.1.2] (Dec 21, 2022)
This update unintentionally ended up pretty much being a continuation of the UI Update

### Additions
 - Added an icon-sheet loader which will improve the UI in the future (#9)
 - Added the capability for widget animations (#9)
 - Added a help button to the UI

### Changes
 - New delete profile button icon, along with a hover animation (#9)
 - Several changes to the README

## UI Update [v1.1.1] (Dec 16, 2022) 
A smaller update focused mostly on the user interface of the app

### Additions
 - Added mouse hover tooltips to all buttons on the UI (#4)
 - Updated the look and feel of the profile buttons (#6)

### Fixes
 - Fix false error message appearing when reloading the window (#7)
 - Fix white rectangle from appearing in the UI
 - Fix setup instructions in the README

## Update 1.1.0 (Dec 4, 2022)

### Additions
 - Can now launch the game if it is not in the default install location
 - Implemented a check for critical files
 - Version tag in the UI

### Changes
 - Made the install process more simple
 - Updated the README.md file

### Fixes
 - Fixed a bug where game would not launch in most cases
 - Properly centered the add profile button
 - Fixed the preview image not showing up in the README

## Update 1.0.1 (Nov 27, 2022)

### Additions
 - Added a changelog
 - Added a new icon for the taskbar/exe file

### Fixes
 - Fixed the window icon not displaying