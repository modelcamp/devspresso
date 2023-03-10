from inference_models.inference_model import InferenceModel, ChatInferencePrompt
from typing import Dict

class CodeGenerator(InferenceModel):

    def __init__(self):
        super().__init__()
        self.name = "code_generator"
        self.display_name = "Code Generator"
        self.openai_model_name = "gpt-3.5-turbo"
        self.max_tokens = 2000
        self.default_prompt_seed = "You're a software engineer helping me write code. Respond with just the code changes requested and no other output. Avoid describing the code and prefer leaving comments in the code instead or using descriptive variable names. If the code requested is unclear, ask me for more information."

    def inference_prompt(self, inference_input: str, previous_messages: [Dict[str, str]] = None) -> ChatInferencePrompt:
        if not previous_messages:
            seed_message = {'role': 'system', 'content': self.default_prompt_seed}
            messages = [seed_message]
        else:
            messages = previous_messages
        messages.append({'role': 'user', 'content': inference_input})
        return ChatInferencePrompt(messages)
