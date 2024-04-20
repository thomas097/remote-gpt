import threading
from config import Config
from pyngrok import ngrok, conf
from rich.console import Console
from flask import Flask, request, jsonify


def authenticate_ngrok(auth_token: str = None) -> None:
    """
        Authentication for ngrok to allow forwarding of a webapp
        to a public URL.

    Args:
        auth_token (str, optional): ngrok authentication token. To obtain an
            auth-token, create an account at https://dashboard.ngrok.com/ and 
            copy the authentication string under `Connect > Installation`.
            If auth_token is None, the user is asked to input a the auth-token 
            upon calling authenticate_ngrok().
    """
    if auth_token is None:
        auth_token = Console().input("[green]Enter your ngrok auth-token: ", password=True)
    
    conf.get_default().auth_token = auth_token


def main(config: Config):
    app = Flask(__name__)
    authenticate_ngrok()

    # Open a ngrok tunnel to the HTTP server
    public_url = ngrok.connect(config.port).public_url
    print(f"Exposing http://127.0.0.1:{config.port} via {public_url}")

    # Update Flask URL with public URL
    app.config["BASE_URL"] = public_url

    @app.route('/text', methods=['POST'])
    def POST_request_handler():
        text = request.get_json()['text']

        # Do stuff here

        response = {
            "success": True,
            "response": "this is my response!"
        }
        return jsonify(response)

    # Start the Flask server in a new thread
    threading.Thread(target=app.run, kwargs={"use_reloader": False}).start()

    Console().print('Press [bold]Enter[\] to kill...')
    input()
    ngrok.disconnect(public_url)


if __name__ == '__main__':
    main(config=Config("config.toml"))