# Dictionary Patches for Plover
[![PyPI](https://img.shields.io/pypi/v/plover-dictionary-patch)](https://pypi.org/project/plover-dictionary-patch/)
![GitHub](https://img.shields.io/github/license/Kaoffie/plover_dictionary_patch)

**Dictionary Patches** are patch files that allow you to patch JSON dictionaries without editing the original files. This is useful if the base dictionary file is from an external source, such as the default `main.json` dictionary from Plover.

## Usage

```json
{
  "source": "main.json",
  "add": {
    "SKWR": "just",
    "TKEURBGS": "dictionary"
  },
  "delete": [
    "SHRAOEP/HRES",
    "TOED/AS"
  ]
}
```

Dictionary patches have the extension `dicp`. They are written in the JSON format, with three sections:

- `source`: Base JSON file; must be in the same directory
- `add`: Additions or overwrites
- `delete`: Deleted entries. Note that only outlines are recorded, and they are surrounded in square brackets `[]`

When using dictionary patches, you are recommended to disable the base dictionary, since the patch itself will act as a normal dictionary. You can delete and edit entries in Plover's dictionary editor on the patch itself, and the patch file will update accordingly based on the difference between the edited dictionary and the base file.

To update the base file, simply replace the original base file with the updated version with the same file name, and the patch will work as usual.
