# PyFuck

PyFuck is a minimalist esoteric programming language interpreter inspired by Brainfuck. It provides a simple interpreter for executing PyFuck scripts and includes an updater.

## Features

- Interpret and execute `.pyf` PyFuck files
- Debugging options for easier troubleshooting
- Automatic updates via GitHub API
- Command-line interface with multiple options

## Installation

If the executable in releases doesn't work you can still use the runtime as a normal python script.

### Remember to add pyfuck.exe to PATH before trying to run it.

Ensure you have Python installed and added to PATH. Then, clone the repository:

```sh
git clone https://github.com/Trenclik/PyFuck.git
cd PyFuck
```

Then run it with:

```sh
python main.py
# main.py replaces pyfuck
```

## Usage

All commands have a shortenned version
e.g.

```sh
pyfuck run -> pyfuck r
```

### Running a PyFuck Script

To execute a `.pyf` script open it with pyfuck.exe or run:

```sh
pyfuck run <path_to_file>
```

Use `--debug` to enable debugging output (useless outside of developement):

```sh
pyfuck run --debug <path_to_file>
```

Use `--silent` to suppress output:

```sh
pyfuck run --silent <path_to_file>
```

### Display Help

To see available commands and options:

```sh
pyfuck help
```

For detailed help on a specific command:

```sh
pyfuck help run
```

### Check Version

To check the current installed version:

```sh
pyfuck version
```

### Update

To update pyfuck interpreter:

```sh
pyfuck update
```

## PyFuck Language

PyFuck consists of three main commands:

- `>` : Move to the next character in the character set
- `<` : Move to the previous character in the character set
- `!` : Print the selected character

Example PyFuck script that executes `print("Hello World!")`:

```pyf
>>>>>>>>>>>>>>>>>>>>>>>>>!
>>!
<<<<<<<<<!
>>>>>!
>>>>>>!
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
<<<<<<!
<<<<<<<<<<<<<<<<<<<<!
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
>>>>>>>!
!
>>>!
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<!
<<<<<<<<!
>>>!
<<<<<<!
<<<<<<<<!
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>!
>!
>>>>>>>!
```

## Automatic Updater

The interpreter includes an updater that checks the latest version from GitHub releases.

## Contributing

Feel free to fork the repository, create a branch, and submit a pull request. Contributions are welcome!

## License

This project is licensed under the MIT License.

## Disclaimer

This is an experimental project and may contain bugs. Use at your own risk.
