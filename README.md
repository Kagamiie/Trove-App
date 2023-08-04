# Trove-App
### Features

- Class Selection: Choose between different character classes by clicking on the respective class buttons. Currently supported classes are Solarion, Ice Sage, Bard, Shadow Hunter, Dracolyte, and Boomeranger (you can select them just by clicking on the classes button).
- Hide Player: Toggle visibility of your character in the game.
- No AFK: Prevent the game from marking you as AFK (Away From Keyboard) automatically.
- Auto-Hit: Automatically keep attacking in the game.

## Requirement

- [Python](https://www.python.org/)
- [PyQt](https://pypi.org/project/PyQt5/)
- [win32api, win32gui, win32con](https://pypi.org/project/pywin32/) 
- [keyboard libraries](https://pypi.org/project/keyboard/)
 
## Installation

Ensure you have Python 3.x installed on your system.
Install the required libraries using the following command:
```sh
pip install PyQt5 pywin32 keyboard
```

Download the Trove application files.
Run the application using the following command, or just by doubleclick on it.:
```sh
python main.pyw
```


## Notes
Before using the application, make sure the game "Trove" is running and visible on your screen.
The application's window is draggable, allowing you to move it to a convenient position on your screen.
To close the application, click the "Close" button.

## Known Issues
The application may not work correctly with screen resolutions other than 1920x1080.
If you encounter any bugs or issues, please report them in the Issues section of the GitHub repository.
If you encounter some 'unicode error 'unicodeescape' can't decode bytes' it may be due to the string 'App/Interface/ui/main.ui', just add another slash/backslash like that 'App//Interface//ui//main.ui', 'App\\Interface\\ui\\main.ui' (depend on what can work for you)
# License
This tool is released under the MIT License. See [LICENSE](https://github.com/Kagamiie/Python-Mini-Projects/blob/afe6d60762ad3e834578d1998c144c06be8ce26d/LICENSE) file for details.

# Contributing
Contributions are welcome! If you find any issues or have any suggestions for improvements, please submit a pull request or open an issue.

<br>
