#!/usr/bin/env python

import unittest
from llmuri import uri_to_litellm


class TestUriToLitellm(unittest.TestCase):
    def zztest_basic_uri_with_prefix(self) -> None:
        uri = "llm:modelname"
        expected_output = {"model": "modelname"}
        self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_no_uri_prefix(self) -> None:
        test_cases = [
            (
                "aaa/bbb",
                {"model": "bbb"},
            ),
            (
                "llm:aaa/bbb",
                {"model": "bbb"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_query_parms(self) -> None:
        test_cases = [
            (
                "aaa/bbb",
                {"model": "bbb"},
            ),
            (
                "llm:aaa/bbb?",
                {"model": "bbb"},
            ),
            ("llm:aaa/bbb?a=1", {"a": "1", "model": "bbb"}),
            ("llm:aaa/bbb?a=1&b=2", {"a": "1", "b": "2", "model": "bbb"}),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_fragments(self) -> None:
        test_cases = [
            (
                "aaa/bbb",
                {"model": "bbb"},
            ),
            (
                "aaa/bbb#",
                {"model": "bbb#"},
            ),
            (
                "aaa/bbb#foo",
                {"model": "bbb#foo"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_abbreviations(self) -> None:
        test_cases = [
            (
                "mistralai/mistral-medium",
                {"api_base": "https://api.mistral.ai/v1", "model": "mistral-medium"},
            ),
            (
                "openai/gpt-4",
                {"api_base": "https://api.openai.com/v1", "model": "gpt-4"},
            ),
            (
                "ollama/llama2",
                {"api_base": "http://localhost:11434", "model": "ollama/llama2"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_ssl(self) -> None:
        test_cases = [
            (
                "ollama/llama2",
                {"api_base": "http://localhost:11434", "model": "ollama/llama2"},
            ),
            (
                "llm:ollama/llama2",
                {"api_base": "http://localhost:11434", "model": "ollama/llama2"},
            ),
            (
                "llms:ollama/llama2",
                {"api_base": "http://localhost:11434", "model": "ollama/llama2"},
            ),
            (
                "ollama@127.0.0.1:11434/llama2",
                {"api_base": "http://127.0.0.1:11434", "model": "ollama/llama2"},
            ),
            (
                "llm:ollama@127.0.0.1:11434/llama2",
                {"api_base": "http://127.0.0.1:11434", "model": "ollama/llama2"},
            ),
            (
                "llms:ollama@127.0.0.1:11434/llama2",
                {"api_base": "https://127.0.0.1:11434", "model": "ollama/llama2"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)

    def test_mem(self) -> None:
        test_cases = [
            ("transformers@:mem/gpt2", {"api_base": ":mem", "model": "gpt2"}),
            ("transformers@FOO:mem/gpt2", {"api_base": "FOO:mem", "model": "gpt2"}),
            ("llm:transformers@FOO:mem/gpt2", {"api_base": "FOO:mem", "model": "gpt2"}),
            (
                "llms:transformers@FOO:mem/gpt2",
                {"api_base": "FOO:mem", "model": "gpt2"},
            ),
            (
                "llms:transformers@:mem/gpt2?a=b&c=d",
                {"api_base": ":mem", "model": "gpt2", "a": "b", "c": "d"},
            ),
            (
                "llms:transformers@FOO:mem/gpt2?a=b&c=d",
                {"api_base": "FOO:mem", "model": "gpt2", "a": "b", "c": "d"},
            ),
            ("openapi@:mem/", {"api_base": ":mem", "model": ""}),
            ("openapi@:mem", {"api_base": ":mem", "model": ""}),
            (
                "llms:openapi@:mem/?a=b&c=d",
                {"api_base": ":mem", "model": "", "a": "b", "c": "d"},
            ),
        ]
        for uri, expected_output in test_cases:
            with self.subTest(uri=uri, expected_output=expected_output):
                self.assertEqual(uri_to_litellm(uri), expected_output)


if __name__ == "__main__":
    unittest.main()
