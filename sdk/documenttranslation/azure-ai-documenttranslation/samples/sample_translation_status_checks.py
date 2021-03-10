# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------


def sample_translation_status_checks():
    import os
    import time
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documenttranslation import (
        DocumentTranslationClient,
        BatchDocumentInput,
        StorageTarget
    )

    endpoint = os.environ["AZURE_DOCUMENT_TRANSLATION_ENDPOINT"]
    key = os.environ["AZURE_DOCUMENT_TRANSLATION_KEY"]
    source_container_url_en = os.environ["AZURE_SOURCE_CONTAINER_URL_EN"]
    target_container_url_es = os.environ["AZURE_TARGET_CONTAINER_URL_ES"]
    target_container_url_fr = os.environ["AZURE_TARGET_CONTAINER_URL_FR"]

    client = DocumentTranslationClient(endpoint, AzureKeyCredential(key))

    job = client.create_translation_job(
        [
            BatchDocumentInput(
                source_url=source_container_url_en,
                targets=[
                    StorageTarget(target_url=target_container_url_es, language="es"),
                    StorageTarget(target_url=target_container_url_fr, language="fr"),
                ],
            )
        ]
    )  # type: JobStatusDetail


    doc_statuses = client.list_documents_statuses(job.id)  # type: ItemPaged[DocumentStatusDetail]

    pending = []
    for doc in doc_statuses:
        if doc.status in ["NotStarted", "Running"]:
            pending.append(doc.id)
        else:
            print("Document at {} completed with status: {}".format(doc.url, doc.status))

    while pending:
        time.sleep(30)
        for idx, doc_id in reversed(list(enumerate(pending))):
            doc_status = client.get_document_status(job.id, doc_id)
            if doc_status not in ["NotStarted", "Running"]:
                print("Document at {} completed with status: {}".format(doc_status.url, doc_status.status))
                del pending[idx]


if __name__ == '__main__':
    sample_translation_status_checks()
