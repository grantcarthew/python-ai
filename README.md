# ai

A command line interface to ChatGPT and prepared prompts.

**STATUS: Extremely unstable**

Reference Documentation:

- [Prompt Engineering](docs/prompt-engineering.md)
- [Markdown Pseudo Language](docs/markdown-pseudo-lang.md)
- [Reference Projects](docs/reference-projects.md)

## Prepared Prompts

Inside the [prompts](prompts) directory you will find prepared prompts you can use to help you focus your chat sessions.

If you create a great prompt, please create a pull request and I'll add it in.

## ai Command Line

You can use the `ai` command line tool located in this repository to interact with ChatGPT from the terminal.

Features:

- Uses an [OPENAI_API_KEY](https://platform.openai.com/account/api-keys), which is far cheaper than a subscription
- Prepared [prompts](prompts). eg: `ai python "read a csv file"`
- Start interactive sessions or one-time requests
- Asynchronous or synchronous interface

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

You'll also need to make sure you have 'tk' installed:

```bash
sudo pacman -S tk
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
