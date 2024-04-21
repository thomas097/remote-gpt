import os
import toml
import urllib.request
from llama_cpp import Llama


class ModelRegistry:
    def __init__(self, toml_registry_file: str) -> None:
        self._registry = toml.load(toml_registry_file)

    def _list_model_names(self) -> list[str]:
        return list(self._registry.keys())
    
    def get_path(self, model_name: str) -> str:
        """Returns the filepath to the model checkpoint on disk. If model is not found 
        on disk, the model is downloaded from the internet (see `models/registry.toml`)

        Args:
            model_name (str): Name of model as listed in registry, e.g. 'mistral-7b'.

        Returns:
            str: full path to model checkpoint
        """
        if model_name not in self._registry:
            raise Exception(f"model_name '{model_name}' does not exist. Choose from {self._list_model_names()}")
        
        dir_path = os.path.dirname(os.path.realpath(__file__))
        model_path = os.path.join(dir_path, f"{model_name}.gguf")

        # Download model if not found in folder
        if not os.path.isdir(dir_path):
            os.mkdirs(dir_path)

        if not os.path.isfile(model_path):
            download_url = self.get_info(model_name, key='download_url')
            print(f'Downloading "{model_name}" from "{download_url}"')
            urllib.request.urlretrieve(download_url, model_path)
            print("  - completed!")

        return model_path

    def get_info(self, model_name: str, key: str) -> str:
        """Retrieves some model_name-specific info under `key` from model registry.

        Args:
            model_name (str): Name of model as listed in registry, e.g. 'mistral-7b'.
            key (str):        Key under which info is stored, e.g. 'chat_format'.

        Raises:
            Exception: `model_name` is not a valid model name.
            Exception: `key` is not a valid key under the specified `model_name`.

        Returns:
            str: String stored under `key` for specified `model_name`.
        """
        model_info = self._registry.get(model_name, None)
        if model_info is None:
            raise Exception(f"model_name '{model_name}' does not exist. Choose from {self._list_model_names()}")
        
        info = model_info.get(key, None)
        if info is None:
            raise Exception(f"key '{key}' does not exist. Choose from {list(model_info.keys())}")
        
        return info


class LLM:
    def __init__(
            self, 
            registry: ModelRegistry,
            model_name: str, 
            system_prompt: str = "You are a helpful chat assistant.", 
            device: str = 'cuda', 
            n_ctx: int = 4096
            ) -> None:

        self._model = Llama(
            model_path=registry.get_path(model_name),
            chat_format=registry.get_info(model_name, key='chat_format'),
            n_gpu_layers=(-1 if device == 'cuda' else 0),
            verbose=False,
            n_ctx=n_ctx
            )
        print(f"LLM.__init__(): Running {model_name} on {device.upper()}")
        
        self._messages = [{"role": "system", "content": system_prompt}]
        
    def chat_completion(self, prompt: str, **kwargs) -> str:
        """Generate LLM assistant's response to user prompt, continuing from chat.

        Args:
            prompt (str): User prompt to respond to.

        Returns:
            str: Response vy LLM assistant.
        """
        # Add user prompt to message queue
        self._messages.append({"role": "user", "content": prompt})

        # Generate response
        response = self._model.create_chat_completion(messages=self._messages, **kwargs)
        message = response['choices'][0]['message']

        # Add assistant's response to message queue
        self._messages.append(message)

        return message['content'].strip()


if __name__ == '__main__':
    llm = LLM(
        registry=ModelRegistry("models/registry.toml"),
        model_name='mistral-7b-openorca-q5'
        )
    response = llm.chat_completion("What is 3 + 3?")
    print(response)

        