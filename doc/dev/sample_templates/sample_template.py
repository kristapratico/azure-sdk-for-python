# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
FILE: sample_template.py

DESCRIPTION:
    This sample demonstrates how to do champion scenario ABC.

    More information on what the sample does or additional details necessary to set up
    the sample to run.

USAGE:
    python sample_template.py

    Set the environment variables with your own values before running the sample:
    1) AZURE_SERVICE_NAME_ENDPOINT - the endpoint to your resource
    2) AZURE_SERVICE_NAME_CREDENTIAL - the credential to authenticate with the service
"""


def sample_template():
    # Sample code goes here

    # Use START/END sphinx directives to capture code for a sample snippet.
    # Use literalinclude in docstrings to embed the sample snippet in ref docs:
    # https://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html#directive-literalinclude

    # [START sample_example]
    import os

    endpoint = os.environ["AZURE_SERVICE_NAME_ENDPOINT"]
    key = os.environ["AZURE_SERVICE_NAME_CREDENTIAL"]

    # [END sample_example]

    # Guideline on samples: https://azure.github.io/azure-sdk/python_documentation.html#code-snippets


if __name__ == "__main__":
    sample_template()
