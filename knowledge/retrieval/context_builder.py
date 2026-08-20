from langchain_core.documents import Document


def build_context(
    documents: list[Document],
) -> str:
    """
    Convert retrieved Documents into textual context
    suitable for the future Generator LLM.
    """

    context_parts = []

    for index, document in enumerate(
        documents,
        start=1,
    ):
        metadata = document.metadata

        source = metadata.get(
            "source",
            "unknown",
        )

        location_parts = []

        if "page" in metadata:
            location_parts.append(
                f"page={metadata['page']}"
            )

        if "slide" in metadata:
            location_parts.append(
                f"slide={metadata['slide']}"
            )

        location = ""

        if location_parts:
            location = (
                ", "
                + ", ".join(location_parts)
            )

        context_parts.append(
            f"[Source {index}: {source}{location}]\n"
            f"{document.page_content}"
        )

    return "\n\n".join(context_parts)