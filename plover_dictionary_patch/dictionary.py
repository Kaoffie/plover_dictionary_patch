import json
import os

from plover.steno_dictionary import StenoDictionary
from plover.dictionary.json_dict import JsonDictionary
from plover.steno import normalize_steno, steno_to_sort_key


PATCH_EXT = "dicp"
SOURCE = "source"
TARGET = "target"
GENERATE = "generate"
ADD = "add"
DELETE = "delete"


class DictionaryPatch(StenoDictionary):

    readonly = False

    def __init__(self):
        super().__init__()
        self._source_name = None
        self._source_path = None
        self._generate_name = None
        self._generate_path = None

    def _load(self, filename: str) -> None:
        with open(filename, "r", encoding="utf-8") as fp:
            json_data = json.load(fp)

            self._source_name = json_data[SOURCE]
            self._source_path = os.path.join(
                os.path.dirname(filename), 
                self._source_name
            )

            if GENERATE in json_data:
                self._generate_name = json_data[GENERATE]
                self._generate_path = os.path.join(
                    os.path.dirname(filename),
                    self._generate_name
                )

                print("Generated", self._generate_path, self._generate_name)

            if TARGET in json_data:
                target_path = os.path.join(
                    os.path.dirname(filename),
                    json_data[TARGET]
                )
                target_dict = JsonDictionary.load(target_path)
                self.update(target_dict)
            
            else:
                source_dict = JsonDictionary.load(self._source_path)
                self.update(source_dict)
            
                additions = json_data[ADD]
                self.update(
                    (normalize_steno(outline), translation)
                    for outline, translation
                    in additions.items()
                )

                deletions = json_data[DELETE]
                for del_key in deletions:
                    self._dict.pop(normalize_steno(del_key), None)

    def _save(self, filename: str) -> None:
        source_dict = JsonDictionary.load(self._source_path)

        source_keys = set(kv[0] for kv in source_dict.items())
        deletions = sorted(
            ("/".join(tup) for tup in source_keys - set(self._dict.keys())),
            key=lambda outline: steno_to_sort_key(outline)
        )

        additions = dict()
        for outline, translation in self.items():
            if (
                outline not in source_keys 
                or translation != source_dict.get(outline)
            ):
                additions["/".join(outline)] = translation
        
        add_mappings = dict(sorted(
            additions.items(),
            key=lambda kv: steno_to_sort_key(kv[0])
        ))

        save_data = {
            SOURCE: self._source_name,
            ADD: add_mappings,
            DELETE: deletions
        }

        if self._generate_path and self._generate_name:
            print("Generating")
            save_data = {GENERATE: self._generate_name, **save_data}
            gen_dict = JsonDictionary()
            gen_dict.path = self._generate_path
            gen_dict.update(self)
            gen_dict.save()

        with open(filename, "w", encoding="utf-8") as fp:
            json.dump(
                save_data, 
                fp, 
                ensure_ascii=False, 
                indent=2,
                separators=(",", ": ")
            )
            fp.write("\n")

    @classmethod
    def create(cls, _) -> None:
        raise ValueError("Dictionary Patches do not support creation")
