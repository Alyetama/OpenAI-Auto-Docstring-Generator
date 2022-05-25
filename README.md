# OpenAI Auto-Docstring

Use OpenAI API to automatically generate elaborate, high quality docstrings for your Python files\*.

[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) 

\*Not meant to be used in production.

## Getting Started

1. [Sign up](https://beta.openai.com/signup) or [login](https://beta.openai.com/login/) to OpenAI.
2. Go to your [API keys page](https://beta.openai.com/account/api-keys).
3. Create a new secret key and copy it.
4. In a terminal shell, run:

```sh
export OPENAI_TOKEN='xxxxxxxxxxx'
```

5. Now you can use the program to automatically generate elaborate docstrings for your Python files by running:

```sh
python auto_docstring.py -f some_script.py -t "$OPENAI_TOKEN"
```
