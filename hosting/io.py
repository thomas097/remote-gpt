import sys
import rich.prompt
import rich.console

def pprint(
        text: str, 
        style: str = None,
        rule: bool = False, 
        wrap: bool = False, 
        replace: bool = False,
        *args, **kwargs
        ) -> None:
    """
        Convenience function to print formatted text.

    Args:
        text (str):               Text to be displayed
        style (str, optional):    Style of text, e.g. "bold red"
        rule (bool, optional):    Whether to print as header
        wrap (bool, optional):    Whether to apply word wrap
        replace (bool, optional): Whether to overwrite previously printed line
    """
    if rule:
        _print_rule(text, style, *args, **kwargs)
    elif wrap:
        _print_wrap(text, style, *args, **kwargs)
    elif replace:
        _print_replace(text, style, *args, **kwargs)
    else:
        print(text)


def _print_rule(text: str, style: str = None, width: int = 80, newline: bool = True) -> None:
    """
        Prints text surrounded by "─" up to the width of the console.

    Args:
        text (str):            Text to be displayed
        style (str, optional): Style of text, e.g. "bold red"
        width (int, optional): Width of console
    """
    rule = "─" * ((width - len(text) - 2) // 2)
    prefix = "\n" if newline else ""
    rich.console.Console().print(f"{prefix}{rule} {text} {rule}", style=style)


def _print_wrap(text: str, style: str = "", width: int = 80) -> None:
    """
        Prints text, wrapping lines to a maximum length of 'width'.

    Args:
        text (str):            Text to be displayed
        style (str, optional): Style of text, e.g. "bold red"
        width (int, optional): Width of console
    """
    # Split on each newline
    for newline in text.split('\n'):

        lines = [[]]
        total = [0]

        for token in newline.split():

            # Restart line if total chars exceeds width
            if total[-1] + len(token) + 1 <= width:
                lines[-1].append(token)
                total[-1] += len(token) + 1
            else:
                lines.append([token])
                total.append(len(token))

        # Print lines one-by-one
        for line in lines:
            rich.console.Console().print(" ".join(line), style=style)


def _print_replace(text: str, style: str = "") -> None:
    """
        Prints text, overwriting previously printed line.

    Args:
        text (str):            Text to be displayed
        style (str, optional): Style of text, e.g. "bold red"
    """
    # Cursor up one line
    sys.stdout.write("\033[F")
    rich.console.Console().print(text, style=style)


def ask_user_input(prompt: str, style: str = "", hide: bool = True) -> str:
    """
        Asks for user input.

    Args:
        prompt (str):          Prefix text prompt
        style (str, optional): Style of text, e.g. "bold red"
        hide (bool, optional): Whether to hide user input.

    Returns:
        str: User input
    """
    style_fmt = f"[{style}]" if style else ""
    return rich.prompt.Prompt.ask(prompt=style_fmt + prompt, password=hide)


def ask_confirm(prompt: str, style: str = "") -> str:
    """
        Ask user to confirm text in prompt.

    Args:
        prompt (str):          Prefix text prompt
        style (str, optional): Style of text, e.g. "bold red"

    Returns:
        str: True if input was 'Y'; False otherwise
    """
    style_fmt = f"[{style}]" if style else ""
    return rich.prompt.Confirm.ask(prompt=style_fmt + prompt)