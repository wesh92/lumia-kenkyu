# Lumia Kenkyu 【研究】

<!--toc:start-->
- [Lumia Kenkyu 【研究】](#lumia-kenkyu-研究)
  - [Project Overview](#project-overview)
  - [Project Structure](#project-structure)
  - [Match Retrieval and Processing](#match-retrieval-and-processing)
    - [Match Processing Components](#match-processing-components)
    - [Match Processing CLI Usage](#match-processing-cli-usage)
  - [Localization (l10n) Data Processing](#localization-l10n-data-processing)
    - [Localization (l10n) Files](#localization-l10n-files)
    - [Localization (l10n) Usage](#localization-l10n-usage)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Error Handling](#error-handling)
  - [Contributing](#contributing)
  - [License](#license)
  - [Authors](#authors)
<!--toc:end-->

Research and data-related information for the MOBA Eternal Return by Nimble Neuron

## Project Overview

This project contains utilities for retrieving, processing, and storing match data for Eternal Return, as well as tools for managing localization (l10n) data. The project is divided into two main components:

1. Match Retrieval and Processing
2. Localization (l10n) Data Processing

## Project Structure

```
lumia-kenkyu/ <-- You are here
├── pyproject.toml
├── README.md
└── src/
    ├── matches/
    │   ├── CONSTS.py
    │   ├── game_data_cli.py
    │   ├── models/
    │   │   ├── game.py
    │   │   └── user.py
    │   ├── data_access/
    │   │   └── supabase.py
    │   ├── processors/
    │   │   ├── prepare_processors.py
    │   │   └── insertion_processors.py
    │   └── getter.py
    └── l10n_data/
        ├── l10n_data_splitter.py
        ├── convert.py
        ├── texts/
        │   └── (generated text files)
        └── jsons/
            └── (generated JSON files)
```

## Match Retrieval and Processing

Located in `src/matches/`, these utilities include a unified CLI tool for fetching game data, grouping it by teams, inserting it into a Supabase database, and performing various other data processing tasks.

### Match Processing Components

- `CONSTS.py`: Contains constants and configuration settings.
- `game_data_cli.py`: Main CLI tool for all game data processing operations.
- `models/`: Defines data models for game and user information.
- `data_access/`: Contains database access layer (Supabase DAO).
- `processors/`: Includes data preparation and insertion strategy processors.
- `getter.py`: Functions for fetching game data from the API.

### Match Processing CLI Usage

The project now uses a unified CLI tool for all match processing operations:

```
poetry run python src/matches/game_data_cli.py [COMMAND] [OPTIONS]
```

Available commands:

1. Insert Users:
   ```
   poetry run python src/matches/game_data_cli.py insert-users [USERNAMES]... [--force]
   ```

2. Fetch User Games:
   ```
   poetry run python src/matches/game_data_cli.py fetch-user-games-command [USERNAME] [--limit LIMIT]
   ```

3. Process JSON Files:
   ```
   poetry run python src/matches/game_data_cli.py process-json-files [--directory DIR] [--archive-dir DIR] [--error-dir DIR]
   ```

4. Process Single File:
   ```
   poetry run python src/matches/game_data_cli.py process-single-file [FILE_PATH] [--archive-dir DIR] [--error-dir DIR]
   ```

5. Process Games (Grouper functionality):
   ```
   poetry run python src/matches/game_data_cli.py process-games [--count COUNT] [--output-dir DIR] [--delay DELAY]
   ```

For more information on each command and its options, use the `--help` flag:

```
poetry run python src/matches/game_data_cli.py [COMMAND] --help
```

## Localization (l10n) Data Processing

Located in `src/l10n_data/`, these utilities help manage and process localization data for Eternal Return.

### Localization (l10n) Files

- `l10n_data_splitter.py`: Splits a large l10n text file into smaller, categorized files.
- `convert.py`: Converts the split text files into JSON format for easier programmatic use.

### Localization (l10n) Usage

1. Download the l10n text file:
   ```
   wget https://d1wkxvul68bth9.cloudfront.net/l10n/l10n-English-20240705012716.txt
   ```

2. Split the text file:
   ```
   poetry run python src/l10n_data/l10n_data_splitter.py l10n-English-20240705012716.txt
   ```
   Optional: Use `--filter-prefix <first-positional-name>` to process only specific types (e.g., `Trait`).

3. Convert split files to JSON:
   ```
   poetry run python src/l10n_data/convert.py
   ```
   Optional: Use `-f <filename>` to convert specific files, or `-f "<pattern>" --glob` for pattern matching.

## Setup

1. Clone this repository.
2. Ensure you have Poetry installed. If not, install it following the instructions at [Python Poetry Docs](https://python-poetry.org/docs/#installation).
3. Navigate to the project root and install dependencies using Poetry:
   ```
   poetry install
   ```
4. Create a `.secrets.toml` file in the `src/matches/` directory (see below for details).

## Configuration

Create a `.secrets.toml` file in the `src/matches/` directory with the following structure:

```toml
[er_api]
key = "your_api_key_here"

[supabase]
url = "your_supabase_project_url"
key = "your_supabase_api_key"
```

Replace `your_api_key_here`, `your_supabase_project_url`, and `your_supabase_api_key` with your actual API key for the Eternal Return API and your Supabase project credentials.

**Note:** Do not commit the `.secrets.toml` file to version control. Add it to your `.gitignore` file to prevent accidental commits.

## Error Handling

If any errors occur during processing, affected files or data will be logged, and in the case of file processing, problematic files will be moved to an error directory for further investigation.

## Contributing

Please read [CONTRIBUTING.md](https://github.com/wesh92/lumia-kenkyu/blob/main/CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GNU AGPLv3 License - see the `LICENSE.md` file for details.

## Authors

- Wes Hahn <wes@cloudskipper.work>
