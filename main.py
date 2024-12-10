from core.prompt_runner import PromptRunner
from core.response_analyser import ResponseAnalyzer
from utils.prompt_data import prompt_data

if __name__ == "__main__":
    prompt_name = 'default-story' # refer prompt examples in utils/prompt_data.py
    constraint_types = list(prompt_data[prompt_name]['idempotence_constraints'].keys()) + ['repeat']
    for constraint_type in constraint_types:
        if constraint_type!='repeat':
            constraints = prompt_data[prompt_name]['idempotence_constraints'][constraint_type].keys()
        else:
            constraints = ['two_times','four_times','six_times']
        for constraint in constraints:
            prompt_runner = PromptRunner(prompt_name,constraint_type,constraint)
            response_analyser = ResponseAnalyzer()
            for i in range(30):
                prompt_runner.get_response()
                response_analyser.responses.append(prompt_runner.response)
                print(f"Prompt {i+1} done")
            with open(f'outputs/output_{prompt_name}_{constraint_type}_{constraint}.txt', 'w') as file:
                file.write("\n*****************\n".join(response_analyser.responses))
            response_analyser.group_responses()
            response_analyser.calculate_metrics()
            print("\nRIPPLE: ",response_analyser.ripple)
            print("\nCONSIM: ",response_analyser.consim)
            with open(f'outputs/output_{prompt_name}_{constraint_type}_{constraint}.txt', 'a') as file:
                file.write("\nRIPPLE: " + str(response_analyser.ripple))
                file.write("\nCONSIM: " + str(response_analyser.consim))