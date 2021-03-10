# coding=utf-8
# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------


def sample_batch_translation():
    import os
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.documenttranslation import (
        DocumentTranslationClient,
        BatchDocumentInput,
        StorageTarget,
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

    job_result = client.wait_until_done(job.id)  # type: JobStatusDetail

    print("Job status: {}".format(job_result.status))
    print("Job created on: {}".format(job_result.created_on))
    print("Job last updated on: {}".format(job_result.last_updated_on))
    print("Total number of translations on documents: {}".format(job_result.documents_total_count))

    print("Of total documents...")
    print("{} failed".format(job_result.documents_failed_count))
    print("{} succeeded".format(job_result.documents_succeeded_count))
    print("{} in progress".format(job_result.documents_in_progress_count))
    print("{} not yet started".format(job_result.documents_not_yet_started_count))
    print("{} cancelled".format(job_result.documents_cancelled_count))

    doc_statuses = client.list_documents_statuses(job_result.id)  # type: ItemPaged[DocumentStatusDetail]
    for document in doc_statuses:
        print("Document with ID: {} has status: {}".format(document.id, document.status))
        if document.status == "Succeeded":
            print("Document location: {}".format(document.url))
            print("Translated to langauge: {}".format(document.translate_to))
        else:
            print("Error Code: {}, Message: {}".format(document.error.code, document.error.message))


if __name__ == "__main__":
    sample_batch_translation()
