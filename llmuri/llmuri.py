#!/usr/bin/env python
"""
llmuri -- URI parsing for LLMs
"""

from urllib.parse import urlparse, parse_qs
from typing import Dict, List, Tuple

api_abbreviations = {
    # TODO figure out how to specify e.g. openai protocol on localhost
    "mistralai": ("mistral", "https://api.mistral.ai/v1"),
    "openai": ("openai", "https://api.openai.com/v1"),
    "claude": ("claude", "https://api.anthropic.com/v1"),
    "ollama": ("ollama", "http://localhost:11434"),
}

# For litellm, These are special cases where the model name should be prefixed
# with the api_spec.
litellm_special_model_prefix = {
    "ollama",
}


def uri_to_litellm(uri: str, verbose: bool = False) -> Dict[str, str]:
    """
    Converts a URI to a dict suitable for passing to litellm.
    """

    rv = {}

    if not (uri.startswith("llm:") or uri.startswith("llms:")):
        uri = "llm:" + uri

    # Patch in a // so it can be parsed by urlparse.
    uri = uri.replace(":", "://", 1)

    # We skip these parsed elements: fragments, params, username, password
    p = urlparse(uri, allow_fragments=False)

    # netloc look like: api_spec@api_base
    # If there is no @, then api_spec is the whole netloc

    netloc_parts = p.netloc.split("@")
    if len(netloc_parts) == 2:
        api_spec, api_base = netloc_parts
    else:
        api_spec = p.netloc
        api_base = None

    if api_base and not api_base.endswith(":mem"):
        if not (api_base.startswith("http://") or api_base.startswith("https://")):
            if p.scheme == "llms":
                api_base = "https://" + api_base
            if p.scheme == "llm":
                api_base = "http://" + api_base
    else:
        if api_spec in api_abbreviations:
            api_spec, api_base = api_abbreviations[api_spec]

    if api_base:
        rv["api_base"] = api_base

    model = p.path
    # get rid of leading / in path
    if model.startswith("/"):
        model = model[1:]

    if api_spec in litellm_special_model_prefix:
        model = f"{api_spec}/{model}"

    rv["model"] = model
    query_dict = {
        k: v[0] if len(v) == 1 else str(v) for k, v in parse_qs(p.query).items()
    }
    rv.update(query_dict)
    return rv
