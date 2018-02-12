# Bibtex-Duplication-Remover
This simple Python script is used for two purposes:

1) Checking the duplicated entries of a Bibtex file.
2) Merging two Bibtex files without duplicated entries.

### How to Use
- Single mode (check the duplication only)

`python bibtex_dup_remover.py ref.bib`

- Merging mode (generate the merged version called out.bib)

`python bibtex_dup_remover.py ref.bib --another-bib new.bib`

### Requirements
- pybtex
