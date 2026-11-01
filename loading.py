"""Load a directory of documents into a LlamaIndex vector index.

The previous version imported a non-existent ``llama`` package and called
methods that don't exist; this uses the real LlamaIndex API.
"""

import os
from pathlib import Path

from llama_index.core import Document, VectorStoreIndex


def load_files_to_index(directory: str, ignore_file: str = ".granignore") -> VectorStoreIndex:
    """Build a VectorStoreIndex from the text files under ``directory``.

    File names (one per line) listed in ``ignore_file`` are skipped.
    """
    root = Path(directory)
    ignore_path = root / ignore_file
    ignored = set(ignore_path.read_text().splitlines()) if ignore_path.exists() else set()

    documents = []
    for current, _dirs, files in os.walk(root):
        for name in files:
            if name in ignored or name == ignore_file:
                continue
            path = Path(current) / name
            try:
                text = path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue  # skip binary or unreadable files
            documents.append(Document(text=text, metadata={"file_path": str(path)}))

    return VectorStoreIndex.from_documents(documents)


if __name__ == "__main__":
    import sys

    directory = sys.argv[1] if len(sys.argv) > 1 else "data"
    index = load_files_to_index(directory)
    print(index.as_query_engine().query("Summarise these documents."))
