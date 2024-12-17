from core.llm_interface import create_and_send_prompt, Prompt
from utils.prompt_data import prompt_data

class PromptRunner:
    def __init__(self, model, prompt_name, constraint_type, constraint):
        self.prompt_name = prompt_name.lower()
        self.model = model.lower()
        self.constraint_type = constraint_type.lower()
        self.constraint = constraint.lower()
        self.system: str = prompt_data[prompt_name]['instruction']
        if constraint_type.lower() =='input_length':
            self.user_prompt: str = prompt_data[prompt_name]['idempotence_constraints']['input_length'][constraint]
            self.idempotence_constraint: str = ""
        elif constraint_type.lower() =='repeat' or constraint_type.lower() =='none':
            self.user_prompt: str = prompt_data[prompt_name]['generic_input']
            self.idempotence_constraint: str = ""
        else:
            self.user_prompt: str = prompt_data[prompt_name]['generic_input']
            self.idempotence_constraint: str = prompt_data[prompt_name]['idempotence_constraints'][constraint_type][constraint]
        self.response:str = ""

    @create_and_send_prompt
    def _send_prompt(self):
        self.user_prompt = "USER INPUT: " + self.user_prompt
        if self.constraint_type=='examples':
            self.idempotence_constraint = "\nHere are examples for reference:\n" + self.idempotence_constraint + "\nUse the format provided in the examples!"
            self.user_prompt = self.user_prompt + self.idempotence_constraint
        elif self.constraint_type=='repeat':
            if self.constraint=='two_times':
                self.idempotence_constraint = self.system
            elif self.constraint=='four_times':
                self.idempotence_constraint = self.system + "\nPlease make sure to " + self.system.lower()
                self.system = self.system + "\nPlease make sure to " + self.system.lower()
            elif self.constraint=='six_times':
                self.idempotence_constraint = self.system + "\nPlease make sure to " + self.system.lower() + "\nIMPORTANT: " + self.system.lower()
                self.system = self.system + "\nPlease make sure to " + self.system.lower() + "\nIMPORTANT: " + self.system.lower()
            self.user_prompt = self.user_prompt + "\nIMPORTANT: " + self.idempotence_constraint
        elif self.constraint_type=='none':
            pass
        else:
            self.user_prompt = self.user_prompt + "\nIMPORTANT: " + self.idempotence_constraint
        return Prompt(system=self.system, user_prompt=self.user_prompt, model=self.model)

    def get_response(self):
        self.response = self._send_prompt()