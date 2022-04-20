# String_Spy - A MacOS/Linux Defensive Tool 
Author: AsaurusRex

## Purpose
String Spy is a project aimed at improving MacOS defenses.  It allows users to constantly monitor all running processes for user-defined strings, and if it detects a process with such a string it will log the PID, process path, and user running the process.  It will also (optionally) kill the process.  For certain default C2s and other malicious software, this tool can quickly log and stop malicious behavior that normal AV does not recognize, and allows for customization.  Right now, String_Spy is set to look for default Mythic payloads, but any IOC string can be used and searched in running processes.  This tool is very similar to Yara, but easier to run for end users.

## Requirements:
Python2 (only tested with Python2.7+), and some associated Python libraries.  In addition, the ability to compile C code to run on your native OS - gcc worked just fine for me. NOTE: Linux OS's do not need to worry about this part as much, and can link any dummy file to run as PID_resolver - this is a TODO for me to clean up.
This is only designed to run on MacOS, not Linux, so some modifications would be needed to port this code to Linux - especially to the C code.

## Usage

usage: String_Spy.py [-h] [-path PATH_TO_COMPILED_BINARY] [-o OUTPUT]
                     [-string_file STRING_FILE]

String Spy searches all running processes on MacOS and kills/logs any process
which contains a string of your choice.

optional arguments:

  -h, --help            show this help message and exit

  -path PATH_TO_COMPILED_BINARY
                        Provide the full path to the compiled PID_resolver
                        code. See PID_resolver.c for source code. Sometimes
                        errors if you do not provide full path


  -o OUTPUT             Provide the full path where you want your log file to
                        be placed.


  -string_file STRING_FILE
                        Provide the path to a file which contains which
                        strings you want to monitor for, and whether you want
                        to kill a process with that string. E.g. "my_string
                        kill" or if you wish to only log the process, then
                        just "my_string log". Each new string should be a on
                        new line.


## Example
Right now, String_Spy is hardcoded to hunt default Mythic payloads.

To run it, after compiling PID_resolver.c, we can use commands such as: 

```
sudo python2 string_scanner.py -path /Users/securitytester/string_scanner/PID_resolver -string_list example_strings.txt
```

NOTE: it is recommended to run this with sudo, so that you can enumerate/kill all processes if necessary.
