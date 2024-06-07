# llmuri -- URI support for LLMs
Standard naming support for LLMs:  llm:myhost/mymodel?params...

This project defines a standard URI for specifying LLMs and provides functionality to
convert LLM strings for use with popular LLM packages.

# Example

```
from llmuri import uri_to_litellm
from litellm import completion

for uri in [
    "llm:openai/gpt-4",
    "openai/gpt-4",
    "llm:ollama/llama2",
    "llm:mistralai/mistral-medium?temperature=0.2&max_tokens=4",
    "llm:ollama@example.com:11434/llama2",
]:
    kwargs = uri_to_litellm(uri)
    response = completion(
        messages=[{"content": "respond in 20 words. who are you?", "role": "user"}],
        **kwargs,
    )
    print(response)
```

## Installation

```
pip install llmuri
```

## URI Specification

[*scheme*:]*provider*[@*host*[:*port*]]/*model-name*[?*parameter1*=*value1*[&*parameter2*=*value2*]...

examples:

```
ollama/llama2
llm:ollama/llama2?temperature=0.2
llms:ollama@example.com:11434/llama2
```

- *scheme* can be "llm" or "llms" to specify that the LLM is hosted behind
  an https web service.  If the scheme is ommitted, "llm" is assumed.

- *provider* is the name of the LLM API or service.

- *host* is an optional hostname where the LLM service is located.

- *port* is the service's port number.

- *model-name* is the name of the model to be executed.

- *parameter-list* is a list of model-specific parameters.

## Canonical Abbreviations

The canonical set of well-known services (e.g. "openai", "mistralai")
is in `canonical-abbreviations.csv`.

## In-process References

If the `port` portion of the URI is "mem", then the LLM is not accessed
externally, but refers to an LLM instantiated in the current process.

The semantics of in-process references is a WIP and subject to change.

- *provider* and *host* are available for llm specification.

```
llm:A@B:mem/mymodel  #  A,B are available
llmp:A@B:C/mymodel   #  A,B,C are available if we introduce a new scheme. bad idea?
```

Examples:

```
llm:MyTransformer@:mem        # Instantiate an instance of MyTransformer
llm:openai@:mem/gpt-3.5-turbo # Instantiate an instance of OpenAI() using gpt-3.5-turbo
llm:completions@mistralai:mem/mistral-medium  # completions interface?
```
