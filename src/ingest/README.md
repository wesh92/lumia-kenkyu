# Ingestion Procedures

## Secrets file for Ingesting Data

You will need to create/place a file named `.secrets.toml` in the `./models` directory. Below is the shape you will need for specific things to function!

```toml
[deepl]
api_key = "******:fx"

[supabase]
url = "https://****.supabase.co"
key = "****"

[er]
api_key = "****"
```

The tables here should be fairly self-explanatory and any additional tables should be self-descriptive as well.

## Using the CLI

Once you have made the toml I recommend reviewing the `er_api_cli` python file.

Sample usage:

```shell
python er_api_cli.py fetch-and-push --no-push --models weapon -d --output data.json
```

The above will run the CLI, not push anything to Supabase, for the weapon endpoint specifically, display a table of the counts, and output the data into a JSON file named `data.json`

```shell
python er_api_tui.py fetch-and-push -d
```

The above will run ALL of the available endpoints, pushing them to Supabase, and displaying a table at the end with counts of each process result. There will be no output file.

> [!IMPORTANT]
> As it is right now these processes will ALWAYS attempt to go to Deepl to translate. There will be an option to NOT do this in the future but you should be aware of it until that time!
