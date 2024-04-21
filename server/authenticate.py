from pyngrok import conf
from source.formatting import pprint, ask_user_input


def authenticate(auth_token: str = "") -> None:
    """
    Authenticates ngrok to enable forwarding of webapps on localhost to a public URL.

    Args:
        auth_token (str, optional): ngrok authentication token. If a token is not 
            provided, the user will be prompted to provide an auth-token manually.
    """
    if auth_token == "":
        # Prompt user to provide ngrok authentication token
        pprint("ngrok authentication", rule=True)
        pprint("\nNo ngrok authentication token set! To obtain a token, please visit the \
               ngrok website (https://dashboard.ngrok.com) and copy your auth-token. New \
               users may need to sign up to create an ngrok account.", wrap=True)
        pprint("\nTip: Set your authentication token in the `config.toml` to authentication automatically.", wrap=True)
        pprint("\nWarning: Keep your authentication token private; never publish your token online!\n", style='bold red', wrap=True)
        
        auth_token = ask_user_input("Enter your ngrok authentication token", style='bold blue')
        pprint("Enter your ngrok authentication token: " + "*" * len(auth_token), style='bold blue',replace=True)

    conf.get_default().auth_token = auth_token
