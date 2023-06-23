# SMAPI Profile Manager Changelog

## Update [v1.2.6] (???)
This update adds a whole new help menu along with other features and fixes.

### Additions
 - Added a new help menu to better assist users with the program (#43)

### Fixes
 - Fixed an issue where tooltips wouldn't render properly when the computer is running slow

## Update [v1.2.5] (March 7, 2023)
An update to make the install process simpler and fix some bugs.

### Additions
 - Added a file scanner to find the SMAPI executable automatically (#38)

### Changes
 - Added hover effects to the profile list

### Fixes
 - Fixed pinned profiles not sticking to the top of the list if the profile was next to another pinned profile in the sort (#35)
 - The tooltip for profile names now gets updated when the profile name is changed (#37)
 - Fixed profile name tooltips appearing away from the profile name in some situations

## Update [v1.2.4] (Feb 9, 2023)
A slightly more feature heavy update than recently, possibly the last big update until 1.3.0.

### Additions
 - Added a button to revert the last change to profiles, in case you accidentally deleted one, for example (#33)
 - Added an update check that informs you when a new update is available (#32)
 - Profiles can now be pinned to the top of the list (#34)

### Changes
 - Massively reorganized the code to make it easier to work with
 - Colour improvements to the profile editor
 - Updated the preview in the README

### Fixes
 - Fixed alignment issues in the profile editor

## QOL Update [v1.2.3] (Jan 26, 2022)
An update with a lot of small quality of life changes and fixes. The goal is to make the program work as you'd think it would.

### Changes
 - The profiles list can now be scrolled with the mouse wheel while hovering the profiles, instead of just the scrollbar
 - Tooltips can now be hovered over without disappearing
 - The textbox to input the name when creating a profile is now selected by default
 - The profile name input popup and profile editor can now be applied by pressing enter

### Fixes
 - Scrolling down the profiles list will no longer cover the top of the window
 - The Last Played property of a profile now says "Never" instead of being blank if the profile has never been played
 - Tooltips should no longer show up in the taskbar as a sub-window
 - Closing the window to name a new profile no longer creates a new profile
 - Closing the profile path explorer no longer creates a new profile with no mods path

## Profile Editor Improvements [v1.2.2] (Jan 16, 2022)
A slightly larger update than usual, this update brings a few new features to the profile editor, as well as a few bug fixes.

### Additions
 - Added a properties dropdown to the profile editor to view properties that can't be edited (#26)
 - Added tooltips to the profile editor (#26)

### Changes
 - All popup windows now appear on top of the main window, rather than top left of screen

### Fixes
 - Fixed a bug where the program would not load if the unmodded profile was edited (#26)
 - Fixed an issue with image files not getting updated when updating the software (#29)
 - Program window should now actually start in the middle of your screen
 - Fixed some elements in the profile editor being aligned to the center rather than left and right (#26)

## Update [v1.2.1] (Jan 9, 2022)

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