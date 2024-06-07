#!/usr/bin/env python
"""
llmuri -- URI parsing for LLMs
"""

from llmuri import uri_to_litellm
from litellm import completion  # type: ignore[import-not-found]
from devtools import debug  # type: ignore[import-not-found]

sample_uris = [
    # abbreviations for common providers
    "mistralai/mistral-medium",
    "openai/gpt-4",
    "ollama/llama2",
    # no leading uri is same as leading uri of "llm://"
    "mistralai/mistral-medium",
    "llm://mistralai/mistral-medium",
    # query parameters
    "mistralai/mistral-medium?temperature=0.2&max_tokens=4",
]

sample_uris = [
    "ollama@localhost:11434/llama2",
    "ollama@127.0.0.1:11434/llama2",
    "ollama/llama2",
    "ollama@example.com:11434/llama2",
]

sample_uris = [
    "ollama/llama2",
    "ollama@example.com:11434/llama2",
    "llm://ollama@example.com:11434/llama2",
    "llms://ollama@example.com:11434/llama2",
]


def do_one_uri(uri: str, dry_run: bool=False) -> None:
    print("-" * 80)

    print("uri:", uri)
    kwargs = uri_to_litellm(uri)
    debug(kwargs)
    if dry_run:
        return
    try:
        response = completion(
            messages=[{"content": "respond in 20 words. who are you?", "role": "user"}],
            **kwargs,
        )
        rid = response["id"]
        rid = response.choices[0].message.content
    except Exception as e:
        print("ERROR:", e)
        response = None
        rid = "******************************** ERROR ********************************"

    print(rid)


def main() -> None:
    for uri in sample_uris:
        do_one_uri(uri, dry_run=False)


if __name__ == "__main__":
    main()
