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
YBM61EIomRK6oLtTIPdC5xMVQUV9cDxp

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

## Installation

The ai command is simply a Python script. To install the ai command, follow these steps.

### Step 1 - Install Python

If you don't have Python installed you will need to install Python v3. The script has been tested on Python v3.10.

https://www.python.org/downloads/

Once installed, test it by opening a terminal or command prompt and typing:

```bash
python --version
pip --version
```

### Step 2 - Install Modules

Python supports many different modules. This command line tool uses the following installable modules:

- [argparse v1.4.0](https://pypi.org/project/argparse/)
- [openai v0.27.4](https://pypi.org/project/openai/)
- [pick v2.2.0](https://pypi.org/project/pick/)
- [prompt_toolkit v3.0.38](https://pypi.org/project/prompt-toolkit/)
- [rich v13.3.4](https://pypi.org/project/rich/)

To install these modules, use the following command in the terminal:

```bash
python -m pip install argparse openai pick prompt_toolkit rich
```

If you would prefer, there is a [pyproject.toml](pyproject.toml) file for a [Poetry](https://python-poetry.org/) installation.

### Step 3 - Clone Repository

You will need [git](https://git-scm.com/) installed to carry out this step.

For Linux:

```bash
bin_path="${HOME}/bin"
mkdir -p "${bin_path}"
cd "${bin_path}"
git clone https://github.com/grantcarthew/python-ai ai
```

### Step 4 - Add PATH

To be able to run the command without changing into the cloned directory, you will need to edit your `PATH` environment variable.

For Linux:

```bash
echo 'export PATH="${PATH}:${HOME}/bin/ai"' >> "${HOME}/.bashrc"
```

### Step 5 - Restart Terminal

To pickup the new PATH environment variable, restart your terminal.

At this point, you should have access to the `ai` command.

Try this:

```bash
ai -i "Hi"
```

The above example is calling the `ai` command, enabling "interactive mode" with `-i`, and then saying "Hi" to ChatGPT.