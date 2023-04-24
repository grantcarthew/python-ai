# ai

A command line interface to ChatGPT and prepared prompts.

## Prepared Prompts

Inside the [prompts](prompts) directory you will find prepared prompts you can use to help you focus your chat sessions.

If you create a great prompt, please create a pull request and I'll add it in.

## ai Command Line

You can use the `ai` command line tool located in this repository to interact with ChatGPT from the terminal.

Features:

- Uses an [OPENAI_API_KEY](https://platform.openai.com/account/api-keys), which is far cheaper than a subscription
- Prepared [prompts](prompts). eg: `ai -p python "read a csv file"`
- Start interactive sessions or one-time requests
- Asynchronous or synchronous interface


Here is the help from the terminal:

```text
usage: ai [-h] [-i] [-lp] [-lm] [-e] [-v] [-s] [-p PROMPT] [request_or_path]

Sends requests to ChatGPT using the OpenAI API.
The result is shown in the terminal and copied onto the clipboard.

An OpenAI API key is required:
export OPENAI_API_KEY=<your-private-key>

Prepared Prompts
----------------
You can preload prepared prompts to focus the AI:
- 'ai -p <prompt-name>: Load a prompt for the request.
- 'ai -lp': List the existing prompts
- 'ai -e': Create, edit, or delete the prepared prompts.
- 'ai -v': View the prompts and messages during a request.

There is a footer.md file that is appended to the end of
every prepared prompt. Review its contents.

File Review
-----------
The 'request_or_path' can be a path to a file such as a Python script.
To ask the AI to do something when you use a path, place a
comment at the top of the file such as:

# ChatGPT: Review this file and make suggestions for improvements.

Synchronous
-----------
By default the 'ai' script responds with content asynchronously
displaying the response in the terminal as it comes in.

If you wish you can change this behaviour by using 'ai -s'.

Note: If you use '-v' for verbose output, synchronous
calls will be forced.

Interactive
-----------
If you start an interactive session with 'ai -i', you can have
longer conversations about a topic. The input prompt supports
history over multiple runs and CTRL-R for searching history.

The history file is located at: '$HOME/.config/aihistory'

Hint: if you point to a file with the 'request_or_path' argument,
you can then discuss the file.

positional arguments:
  request_or_path       your question or a file path

options:
  -h, --help            show this help message and exit
  -i, --interactive     does not exit after the first response
  -lp, --list-prompts   lists the prepared prompts
  -lm, --list-models    lists the available OpenAI models
  -e, --edit            opens the prompts in VSCode
  -v, --verbose         shows metadata (synchronous forced)
  -s, --synchronous     use synchronous calls to OpenAI
  -p PROMPT, --prompt PROMPT
                        prompt name or part there of

Example
---------------------------------------------------------
Ask a basic question:
$ ai "Define Chockers"

List prepared prompts:
$ ai -lp

Get prompted for a basic question:
$ ai

Review a Python script:
$ ai -p python /path/to/doc

Edit the prompts in VSCode:
$ ai -e

Show the full request details:
$ ai -v "What is the meaning of life?"


```
