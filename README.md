# OpenAI Auto-Docstring Generator

Use OpenAI API to automatically generate elaborate, high quality docstring for your Python files\*.

[![Supported Python versions](https://img.shields.io/badge/Python-%3E=3.6-blue.svg)](https://www.python.org/downloads/) [![PEP8](https://img.shields.io/badge/Code%20style-PEP%208-orange.svg)](https://www.python.org/dev/peps/pep-0008/) 

\*Not meant to be used in production.

## Getting Started

1. Clone this repository

```sh
git clone https://github.com/Alyetama/OpenAI-Auto-Docstring-Generator.git
cd OpenAI-Auto-Docstring-Generator
```

2. [Sign up](https://beta.openai.com/signup) or [login](https://beta.openai.com/login/) to OpenAI.
3. Go to your [API keys page](https://beta.openai.com/account/api-keys).
4. Create a new secret key and copy it.
5. In a terminal shell, run:

```sh
export OPENAI_TOKEN='xxxxxxxxxxx'
```

## Usage

```
python generate_docstring.py --help

usage: generate_docstring.py [-h] -f FILE [-t OPENAI_TOKEN]
                             [-F FREQUENCY_PENALTY] [-T TOP_P]
                             [-p PRESENCE_PENALTY] [-e TEMPERATURE]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to the input file
  -t OPENAI_TOKEN, --openai-token OPENAI_TOKEN
                        OpenAI token
  -F FREQUENCY_PENALTY, --frequency-penalty FREQUENCY_PENALTY
                        How much to penalize new tokens based on their
                        existing frequency in the text so far. Decreases the
                        model's likelihood to repeat the same line verbatim
  -T TOP_P, --top-p TOP_P
                        Controls diversity via nucleus sampling: (e.g., 0.5
                        means half of all likelihood weighted options are
                        considered
  -p PRESENCE_PENALTY, --presence-penalty PRESENCE_PENALTY
                        How much to penalize new tokens based on whether they
                        appear in the text so far. Increases the model's
                        likelihood to talk about new topics
  -e TEMPERATURE, --temperature TEMPERATURE
                        Controls randomness (i.e., lowering results in less
                        random completions. As the temperature approaches
                        zero, the model will become deterministic and
                        repetitive
```


### Example

```sh
python generate_docstring.py -f some_script.py -t "$OPENAI_TOKEN"
```

<details>
  <summary>Input file</summary>
  
```python

# Source: https://github.com/Alyetama/Gotipy

import json
import os
import sys
import traceback

import requests
from requests.auth import HTTPBasicAuth
from requests.structures import CaseInsensitiveDict

from gotipy_exceptions import _MissingRequiredParameter


class Gotify:

    def __init__(self,
                 host_address=None,
                 fixed_token=None,
                 fixed_priority=None):
        self.host_address = host_address
        self.fixed_token = fixed_token
        self.fixed_priority = fixed_priority

    @staticmethod
    def _headers():
        headers = CaseInsensitiveDict()
        headers['Content-type'] = 'application/json'
        return headers

    def _get_host_address(self):
        host_address = self.host_address
        if not host_address and not os.getenv('GOTIFY_HOST_ADDRESS'):
            raise _MissingRequiredParameter('host_address',
                                            'GOTIFY_HOST_ADDRESS',
                                            'class instance')
        else:
            if not host_address:
                host_address = os.getenv('GOTIFY_HOST_ADDRESS')
        if 'http' not in host_address:
            raise TypeError(
                'Missing a valid scheme in the host address (e.g., `http://`)!'
            )
        return host_address

    def create_app(self, admin_username, admin_password, app_name, desc=None):
        host_address = self._get_host_address()
        url = f'{host_address}/application'
        data = json.dumps({'name': app_name, 'description': desc})
        auth = HTTPBasicAuth(admin_username, admin_password)
        resp = requests.post(url,
                             headers=self._headers(),
                             data=data,
                             auth=auth)
        return resp.json()

    def push(self, title, message, token=None, priority=2):

        if not token:
            token = self.fixed_token
            if not token:
                token = os.getenv('GOTIFY_APP_TOKEN')
        host_address = self.host_address

        if self.fixed_priority:
            priority = self.fixed_priority

        data = {'title': title, 'message': message, 'priority': priority}

        if not token and not os.getenv('GOTIFY_APP_TOKEN'):
            raise _MissingRequiredParameter('token', 'GOTIFY_APP_TOKEN',
                                            'method')

        host_address = self._get_host_address()

        url = f'{host_address}/message?token={token}'
        resp = requests.post(url,
                             headers=self._headers(),
                             data=json.dumps(data))

        try:
            return resp.json()
        except json.decoder.JSONDecodeError:
            traceback.print_exception(*sys.exc_info())
        except requests.exceptions.ConnectionError:
            traceback.print_exception(*sys.exc_info())
```

</details>


<details>
  <summary>Output</summary>

```
# >>>>>>>>>>>>>>> METHOD/FUNCTION: __init__ (1/5)

    """
    Args:
        host_address (str): The host address of the server.
        fixed_token (str): The fixed token to be used for authentication.
        fixed_priority (int): The fixed priority to be used for authentication.
    """

--------------------------------------------------------------------------------

# >>>>>>>>>>>>>>> METHOD/FUNCTION: _headers (2/5)

    """
    Returns:
        headers (CaseInsensitiveDict): A dictionary of headers to be used in the request.
    """

--------------------------------------------------------------------------------

# >>>>>>>>>>>>>>> METHOD/FUNCTION: _get_host_address (3/5)

    """Gets the host address of the Gotify server.

    Returns:
        str: The host address of the Gotify server.

    Raises:
        _MissingRequiredParameter: If the host address is not provided.
        TypeError: If the host address is not a valid URL.
    """

--------------------------------------------------------------------------------

# >>>>>>>>>>>>>>> METHOD/FUNCTION: create_app (4/5)

    """Creates a new application.

    Args:
        admin_username (str): The username of the admin user.
        admin_password (str): The password of the admin user.
        app_name (str): The name of the application to be created.
        desc (str): The description of the application to be created.

    Returns:
        dict: A dictionary containing the response from the server.
    """

--------------------------------------------------------------------------------

# >>>>>>>>>>>>>>> METHOD/FUNCTION: push (5/5)

    """Sends a push notification to the Gotify server.

    Args:
        title (str): The title of the notification.
        message (str): The message of the notification.
        token (str): The token of the application.
        priority (int): The priority of the notification.

    Returns:
        dict: A dictionary containing the response from the server.

    Raises:
        MissingRequiredParameter: If the token is not provided.
        ConnectionError: If the connection to the server fails.
    """

--------------------------------------------------------------------------------

```

</details>
