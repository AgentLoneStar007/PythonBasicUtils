# Python Basic Utilities

A collection of basic Python utilities for use in any Python project, in the form of
subclasses and files, and not as a third-party dependency that needs installation.

### Features:

- Dependency installation
- Logging utility
- Configuration system via PyYAML
- Commenting throughout for readable, understandable code

### Installation/Usage:

Simply clone this repository, and either start coding your project inside the Main
class, or take what's currently inside the Main class and implement it into your
main.py file/program.

#### Dependencies:
To specify a dependency that requires installation, simply copy the one existing
dependency already in `dependencies.json`, and change what is needed. Example:
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
(Note that the `-q` args in the command are to prevent any output from the command.
And it's good practice to use `python -m pip` instead of `pip` directly, due to some
individuals not having pip added to PATH.)

#### Logging:
Import `from functions.logger import Log` in any file or function that you wish to
log from, and pass through the current file object from Main into the function. Log
takes three arguments: "`logFile`(the file to log to, obviously)," "`infoType`(the
type of output, be it info, warning, error, or debug)," and "`message`(the message to
log)." Note that Log does not output anything to the terminal or current screen. It
only outputs to the current log file. Any output to the terminal must be done with
print statements.

#### Config:
To load config, import `from functions.loadConfig import LoadConfig`. You must create
an object of the `loadConfig` class to load the config. Example:
```python
from functions.loadConfig import LoadConfig
loadConfig = LoadConfig()
config = loadConfig.isConfigLoaded()
```
`config` will return a dictionary with all config values in it. If you add any values
to the config file, be sure to add them to the `createDefaultConfig` function as well.

### Credit:

Don't remove the comments stating me as author.
