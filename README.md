# Idem-Prompt

## Abstract

GPT-4o and other large language models have significant use in large-scale customer-facing applications. However, to ensure their performance and evaluation are reliable and trustworthy, it is necessary to study their ability to generate consistent results for perfectly identical inputs. By introducing Idem-Prompt, a modular query framework, we explore how GPT-4o, a widely used model in LLM-powered applications, can achieve improved idempotence, i.e., better repeatability in responses. Through the framework, we incorporate specific constraints within the input, known as idempotence-driven constraints, and demonstrate how these simple restrictions can enhance character-level and content-level consistency across various natural language processing and generation tasks.

<p align="center" width="100%">
<img src="https://github.com/user-attachments/assets/7e31b721-f764-45a3-9950-24b796e08343">
<em>Figure 1: Example of character-level idempotent responses by an LLM </em>

<img src="https://github.com/user-attachments/assets/93ede282-5a52-46ca-ab6f-d8d46cad284a">
<em>Figure 2: Example of character-level non-idempotent responses by an LLM </em>
</p>

## Installation

1. Clone the repository
2. Optional: Create a Python virtual environment
3. Run:
   
```
pip install -r requirements.txt
```

## Usage

Set the test parameter in main.py. Refer to utils/prompt_data.py for prompt names.
```
prompt_name = <default-prompt-name>
```

## Contributing

We appreciate any additional requests and/or contributions to Idem-Prompt. The issues tracker is used to keep a list of features and bugs to be worked on. Please contact the authors for contributions.
