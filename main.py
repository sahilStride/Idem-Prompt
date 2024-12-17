from core.prompt_runner import PromptRunner
from core.response_analyser import ResponseAnalyzer
from utils.prompt_data import prompt_data

if __name__ == "__main__":
    prompt_name = '' # refer prompt examples in utils/prompt_data.py
    model = '' # select from ['gpt-4o','gemini-1.5-flash','claude-3-5-sonnet-latest','llama3.3-70b','grok-2-1212']
    num_runs = 30 # number of runs for each prompt
    constraint_types = list(prompt_data[prompt_name]['idempotence_constraints'].keys()) + ['repeat','none']
    for constraint_type in constraint_types:
        if constraint_type=='none':
            constraints = ['none']
        elif constraint_type!='repeat':
            constraints = prompt_data[prompt_name]['idempotence_constraints'][constraint_type].keys()
        else:
            constraints = ['two_times','four_times','six_times']
        for constraint in constraints:
            response_analyser = ResponseAnalyzer()
            for i in range(num_runs):
                prompt_runner = PromptRunner(model,prompt_name,constraint_type,constraint)
                prompt_runner.get_response()
                response_analyser.responses.append(prompt_runner.response)
                print(f"Prompt {i+1} done")
            response_analyser.group_responses()
            response_analyser.calculate_metrics()
            with open(f'outputs/{model}_output_{prompt_name}_{constraint_type}_{constraint}.txt', 'a') as file:
                file.write("\nRIPPLE: " + str(response_analyser.ripple))
                file.write("\nCONSIM: " + str(response_analyser.consim))