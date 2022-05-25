#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import signal
import sys
import time

import openai


def alarm_handler(signum, _):
    print('Signal handler called with signal', signum)
    raise TimeoutError('Request is taking too long. Skipping...')


def keyboard_interrupt_handler(sig: int, _) -> None:
    print(f'KeyboardInterrupt (id: {sig}) has been caught...')
    print('Terminating the session gracefully...')
    sys.exit(1)


def generate_docstring(file, openai_token, temperature, top_p,
                       frequency_penalty, presence_penalty):
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    signal.signal(signal.SIGALRM, alarm_handler)

    for p in [temperature, top_p]:
        assert 0 <= p <= 1, 'Allowed range for temperature/top_p is [0.0, 1.0]'
    for _p in [frequency_penalty, presence_penalty]:
        assert 0 <= _p <= 2, \
        'Allowed range for frequency_penalty/presence_penalty is [0.0, 2.0]'

    openai.api_key = openai_token

    with open(file) as f:
        lines = f.read()

    functions = lines.split('def ')[1:]
    functions[-1] = functions[-1].split('if __name__')[0]

    n = 1

    for func in functions:

        signal.alarm(60)

        func_tokens = 'def ' + func.replace('        ', '    ').strip()
        if '"""' in func_tokens:
            func_tokens = ''.join(
                func_tokens.split('"""')[0::2]).strip().replace('\n\n', '\n')

        func_name = func_tokens.split('(')[0].split('def ')[1]
        prog = f'({n}/{len(functions)})'
        print(f'# >>>>>>>>>>>>>>> METHOD/FUNCTION: {func_name} {prog}\n')

        prompt_tokens = len(func_tokens) / 2
        max_tokens = int(4000 - prompt_tokens)

        config = {
            'engine':
            'code-davinci-002',
            'prompt':
            f'# Python 3.7\n \n{func_tokens}\n    \n# An elaborate, '
            'high quality docstring for the above function in google '
            'format:\n\"\"\"',
            'temperature':
            temperature,
            'max_tokens':
            max_tokens,
            'top_p':
            top_p,
            'frequency_penalty':
            frequency_penalty,
            'presence_penalty':
            presence_penalty,
            'stop': ["#", "\"\"\""]
        }

        try:
            response = openai.Completion.create(**config)
        except TimeoutError:
            continue

        try:
            resp = response['choices'][0]['text'].strip()
        except KeyError as e:
            print(f'ERROR!: {e}')

        if resp.startswith('    '):
            resp = ''.join(resp[5:])

        if resp.lstrip().startswith('def'):
            resp = ''.join(resp.split(':')[1:])

        if resp.startswith(func_name + '('):
            resp = ''.join(resp.split(')')[1:])

        print('    """' + resp.strip())
        print('    """')
        print(f'\n{"-" * 80}\n')

        if n != len(functions):
            time.sleep(20)
            n += 1

        signal.alarm(0)


def opts() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('-f',
                        '--file',
                        help='Path to the input file',
                        type=str,
                        required=True)
    parser.add_argument('-t',
                        '--openai-token',
                        help='OpenAI token',
                        type=str,
                        default=os.getenv('OPENAI_API_KEY'))
    parser.add_argument('-F',
                        '--frequency-penalty',
                        help='How much to penalize new tokens based on their '
                        'existing frequency in the text so far. Decreases the '
                        'model\'s likelihood to repeat the same line verbatim',
                        type=float,
                        default=0)
    parser.add_argument(
        '-T',
        '--top-p',
        help='Controls diversity via nucleus sampling: (e.g., '
        '0.5 means half of all likelihood weighted options are '
        'considered',
        type=float,
        default=1)
    parser.add_argument(
        '-p',
        '--presence-penalty',
        help='How much to penalize new tokens based on whether '
        'they appear in the text so far. Increases the model\'s '
        'likelihood to talk about new topics',
        type=float,
        default=0.2)
    parser.add_argument(
        '-e',
        '--temperature',
        help='Controls randomness (i.e., lowering results in '
        'less random completions. As the temperature approaches '
        'zero, the model will become deterministic and '
        'repetitive',
        type=float,
        default=0)
    return parser.parse_args()


if __name__ == '__main__':
    args = opts()
    generate_docstring(**vars(args))
