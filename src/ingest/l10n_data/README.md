# Create Split Texts and JSONs for Programmatic Use of l10n Data

## Goal

- Split the l10n large text file into manageable chunks for programmatic use.
- Create JSON files programmatically for more standardized and structured use.

## Steps

1. Get the l10n text file.
```bash
wget https://d1wkxvul68bth9.cloudfront.net/l10n/l10n-English-20240705012716.txt
```
2. Split the text file using the l10n_data_splitter.py script.
```bash
poetry run python l10n_data_splitter.py l10n-English-20240705012716.txt
```
- This script will create a directory `texts` if it does not exist. It takes the first two positional items from the first line it encounters something new in the text and populates the text files with the text until the next two positional items are encountered.
> [!NOTE]
> There is an additional argument `--filter-prefix <first-positional-name>` which allows a user to only parse, for instance, `Trait` types out of the text file.
3. Create JSON files from the split text files using the convert.py script.
```bash
poetry run python convert.py
```
- The `convert.py` script will create a directory `jsons` if it does not exist. It will create a JSON file for each text file in the `texts` directory. The JSON file will have the same name as the text file with the `.json` extension.
> [!NOTE]
> Additonal parameter `-f area_name -f trait` is avialable if you only need to convert certain text files to JSONs. This must match the FILENAME completely (exclude the extension). So, unlike the above script where you could pass `item` and get all subtypes of `item`, here you must pass the exact name of the file you want to convert.
> EXCEPT when you pass an additional argument `--glob` which will allow the script to glob match. You will need to quote the text as well. Example of this below:
```bash
poetry run python convert.py -f "weapontype_*" --glob
```
