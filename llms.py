import os
import urllib.request
from llama_cpp import Llama
from hosting.io import pprint
from rich.console import Console


MODEL_INFO = {
    'mistral-7b-openorca-q5': {
        "url": "https://huggingface.co/TheBloke/Mistral-7B-OpenOrca-GGUF/resolve/main/mistral-7b-openorca.Q5_K_M.gguf",
        "chat_format": 'chatml'
    }
}


class LLM:
    def __init__(
            self, 
            model_name: str, 
            sys_prompt: str = "You are a helpful chat assistant.", 
            device: str = 'cuda', 
            n_ctx: int = 4096
            ) -> None:
        # Filepath to model weights
        model_path = os.path.realpath(os.path.join("models", f"{model_name}.gguf"))

        # Download model from the web if it has not yet exist
        if not os.path.isfile(model_path):
            self._download(model_name, outfile=model_path)

        self._model = Llama(
            model_path=model_path,
            chat_format=MODEL_INFO[model_name]['chat_format'],
            n_gpu_layers=(-1 if device == 'cuda' else 0),
            n_ctx=n_ctx,
            verbose=False
            )
        
        self._messages = [{"role": "system", "content": sys_prompt}]
        
        pprint(f"Running {model_name} on {device.upper()}!", rule=True)
            
    def _download(self, model_name: str, outfile: str) -> None:
        # Test whether model_name refers to a model in MODEL_URLS
        model_info = MODEL_INFO.get(model_name, None)
        if model_info is None:
            pprint(f"ERROR: Unknown model_name '{model_name}'. Please choose from:", style="bold red")
            for model in MODEL_INFO.keys():
                pprint(f"  - {model}", style="bold red")
            quit()
        else:
            url = model_info['url']

        # Create one.
        outdir = os.path.dirname(outfile)
        if not os.path.isdir(outdir):
            os.makedirs(outdir)

        progress_text = f"Downloading '{model_name}' from '{url}'"
        with Console().status(progress_text, spinner="bouncingBar"):
            urllib.request.urlretrieve(url, outfile) 

        pprint("Download completed!", style="bold blue")

    def chat_completion(self, prompt: str, **kwargs) -> None:
        # Update chat history
        self._messages.append({"role": "user", "content": prompt})

        # Get response from LLM
        response = self._model.create_chat_completion(messages=self._messages, **kwargs)
        message = response['choices'][0]['message']

        # Update chat history with LLM's message
        self._messages.append(message)

        return message['content']


if __name__ == '__main__':
    llm = LLM('mistral-7b-openorca-q5')
    response = llm.chat_completion("What is 3 + 3?")
    print(response)

        