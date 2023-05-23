# Python Basic Utilities

A collection of basic Python utilities for use in any Python project, in the form of
subclasses and files, and not as a third-party dependency that needs installation.
Completely cross-platform, functioning on anything supporting Python 3. (No support for
Python 2 is planned.)

### Features:

- Dependency installation
- Logging utility
- Easy-to-use configuration system via PyYAML
- Support for both terminal and graphical apps
- Completely cross-platform
- Graphical error/dialogue windows via Tkinter
- Commenting throughout for readable, understandable code

### Installation/Usage:

Simply clone this repository and start creating your project inside the Main
class.

#### Setting up your app:
Change the values in `data/app.json` to your liking. Default values are:
```json
{
  "name": "My App",
  "version": 0.1,
  "author": "A Person",
  "app-type": "terminal"
}
```
`app-type` can be either "terminal" or "graphical". Terminal will output everything
in the terminal, obviously, while Graphical will create and manage windows via Python's
stock Tkinter GUI system. Version currently doesn't do much outside of cosmetic value,
but it will have more importance when I finish the update system.

#### Dependencies:
To specify a dependency that requires installation, I would recommend copying the one
existing dependency already in `dependencies.json`, and changing what is needed. Example:
```json
{
  "dependencies": [
    {
      "name": "PyYAML",
      "import": "import yaml",
      "install": "python3 -m pip install pyyaml -q -q -q"
    },
    {
      "name": "MyDependency",
      "import": "from mydependency import MyDependency",
      "install": "python3 -m pip install mydependency -q -q -q"
    }
  ]
}
```
(Note that the `-q` args in the command are to prevent any output from Pip.
And it's good practice to use `python3 -m pip` instead of `pip` directly, due to some
individuals not having pip added to PATH. Specify `python3` to avoid interference with
Python 2, if it's installed.)

#### Logging:
Import `from functions.logger import Log` in any file or function that you wish to
log from, and pass through the current file object from Main into the function. Log
takes three arguments: "`logFile`(the file to log to, obviously)," "`infoType`(the
type of output, be it info, warning, error, or debug)," and "`message`(the message to
log)." Note that Log does not output anything to the terminal or current screen. It
only outputs to the current log file. Any output to the terminal must be done with
print statements.

#### Config:
To load config, import `from functions.loadConfig import loadConfig`. Then simply create
a config var with `loadConfig` as its value. Example:

```python
from functions.loadData import loadConfig

config = loadConfig()
```
`config` will return a dictionary with all config values in it. If there is no config
file present, the function will return `False`. The best way to create a system for
using the config is as follows:
```python
if config:
    myValue = config['myValue']
else:
    myValue = 'some default value'
```
If you add any values to the config file, be sure to add them to the
`createDefaultConfig` function as well.

#### Graphical Errors/Dialogues
To use a Graphical Error(GError), simply import `from functions.graphicalError import
GError`. While it is named error, it can be used for dialogues as well.

GError takes multiple arguments:
- `message`: A string to show as a message in the window(required)
- `messageToLog`: The message to log to file, if different from message. Pass `None`
if the message is the same.
- `windowTitle`: The title for the window. Also pass `None` if you want to use the
default of "(AppName) - Error"),
- `custom_buttons`: custom buttons you can create along with the default "OK" button.
Pass a dictionary in this format for your buttons:`{"button":"code to execute"}`.
A simple example would be "`{"Print":"print('hi')"}`".
- `logFile`: The file to log to. (required)

### To-do:

- Add an option to handle dependency installation in a window, instead of a terminal.
- Add more graphical elements overall.
- Find a way to not have to pass the current log file to every subclass and function.
- Add more error handling for the program.
- Create an automatic update system.

### Credit:

Don't remove the comments stating me as author.
