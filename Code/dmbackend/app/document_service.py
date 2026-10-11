import os
import uuid

import fitz


# Project root:
# B:\SASTRA_Bhuvaneshwari_227003030_CSE
PROJECT_ROOT = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "..",
        "..",
    )
)

# Shared input-data directory at the project root
DATA_DIR = os.path.join(
    PROJECT_ROOT,
    "Input_Data",
)

UPLOAD_DIR = os.path.join(
    DATA_DIR,
    "uploads",
)

EXTRACTED_DIR = os.path.join(
    DATA_DIR,
    "extracted",
)


def ensure_storage_directories():
    os.makedirs(
        UPLOAD_DIR,
        exist_ok=True
    )

    os.makedirs(
        EXTRACTED_DIR,
        exist_ok=True
    )


def save_pdf(file):
    ensure_storage_directories()

    unique_id = uuid.uuid4().hex

    stored_filename = (
        f"{unique_id}.pdf"
    )

    pdf_path = os.path.join(
        UPLOAD_DIR,
        stored_filename
    )

    file.save(pdf_path)

    return (
        stored_filename,
        pdf_path
    )


def extract_pdf_text(
    pdf_path,
    stored_filename
):
    ensure_storage_directories()

    document = None

    try:
        document = fitz.open(
            pdf_path
        )

        page_count = len(
            document
        )

        text_parts = []

        for page_number in range(
            page_count
        ):
            page = document[
                page_number
            ]

            page_text = page.get_text(
                "text"
            )

            if page_text:
                text_parts.append(
                    page_text
                )

        extracted_text = "\n".join(
            text_parts
        ).strip()

        extracted_filename = (
            os.path.splitext(
                stored_filename
            )[0]
            + ".txt"
        )

        extracted_path = os.path.join(
            EXTRACTED_DIR,
            extracted_filename
        )

        with open(
            extracted_path,
            "w",
            encoding="utf-8"
        ) as text_file:
            text_file.write(
                extracted_text
            )

        return {
            "page_count": page_count,
            "extracted_text": extracted_text,
            "extracted_text_path": extracted_path,
            "extracted_text_length": len(
                extracted_text
            )
        }

    finally:
        if document is not None:
            document.close()


def delete_document_files(
    storage_path,
    extracted_text_path
):
    if (
        storage_path
        and os.path.exists(storage_path)
    ):
        os.remove(
            storage_path
        )

    if (
        extracted_text_path
        and os.path.exists(
            extracted_text_path
        )
    ):
        os.remove(
            extracted_text_path
        )