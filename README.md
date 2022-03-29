# Dictionary Patches for Plover
[![PyPI](https://img.shields.io/pypi/v/plover-dictionary-patch)](https://pypi.org/project/plover-dictionary-patch/)
![GitHub](https://img.shields.io/github/license/Kaoffie/plover_dictionary_patch)

**Dictionary Patches** allow you to maintain edits of dictionaries without making any actual changes to the original file, allowing you to swap or update the original file when necessary.

## Format

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

## Usage

When using dictionary patches, you are recommended to disable the base dictionary, since the patch itself will act as a normal dictionary. You can delete and edit entries in Plover's dictionary editor on the patch itself, and the patch file will update accordingly based on the difference between the edited dictionary and the base file.

To update the base file, simply replace the original base file with the updated version with the same file name, and the patch will work as usual.

## Converting dictionaries to Patches

If you already have a regular JSON dictionary that contains edits from an original dictionary file, you can create a patch file like this, with a `target` parameter containing the name of the edited dictionary file.

```json
{
  "source": "main.json",
  "target": "edited_main.json"
}
```

The next time you edit the patch, the file will be expanded into its regular additions/deletions format in the example above. You are recommended to keep a backup of the original edited dictionary.

## Converting Patches to Dictionaries

If you would like to create a copy of the edited dictionary in JSON format, simply add a `generate` parameter containing the name of the output file:

```json
{
  "generate": "edited_dict.json",
  ...
}
```

The edited dictionary will be generated as a JSON dictionary every time you update the patch from within Plover.