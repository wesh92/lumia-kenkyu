# Lumia Kenkyu

<!--toc:start-->
- [Lumia Kenkyu](#lumia-kenkyu)
  - [Project Overview](#project-overview)
  - [Project Structure](#project-structure)
  - [Match Retrieval Utilities](#match-retrieval-utilities)
    - [Files](#files)
    - [Usage](#usage)
  - [Localization (l10n) Data Processing](#localization-l10n-data-processing)
    - [Files](#files)
    - [Usage](#usage)
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

1. Match Retrieval Utilities
2. Localization (l10n) Data Processing

## Project Structure

```
lumia-kenkyu/
├── pyproject.toml
├── README.md
└── src/
    ├── matches/
    │   ├── CONSTS.py
    │   ├── game.py
    │   ├── getter.py
    │   ├── grouper.py
    │   └── inserter.py
    └── l10n_data/
        ├── l10n_data_splitter.py
        ├── convert.py
        ├── texts/
        │   └── (generated text files)
        └── jsons/
            └── (generated JSON files)
```

## Match Retrieval Utilities

Located in `src/matches/`, these utilities include scripts for fetching game data, grouping it by teams, and inserting it into a Supabase database.

### Files

- `CONSTS.py`: Contains constants and configuration settings.
- `game.py`: Defines data models for game and player information.
- `getter.py`: Functions for fetching game data from an API.
- `grouper.py`: Groups game data by teams and writes it to JSON files.
- `inserter.py`: Inserts processed game data into a Supabase database.

### Usage

To fetch and group game data:

```
poetry run python src/matches/grouper.py --count <number_of_games> --output_dir <output_directory> --delay <delay_between_requests>
```

To insert data into Supabase:

```
poetry run python src/matches/inserter.py
```

## Localization (l10n) Data Processing

Located in `src/l10n_data/`, these utilities help manage and process localization data for Eternal Return.

### Files

- `l10n_data_splitter.py`: Splits a large l10n text file into smaller, categorized files.
- `convert.py`: Converts the split text files into JSON format for easier programmatic use.

### Usage

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
2. Ensure you have Poetry installed. If not, install it following the instructions at [https://python-poetry.org/docs/#installation](https://python-poetry.org/docs/#installation).
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

If any errors occur during processing, affected files or folders will be moved to an error directory for further investigation.

## Contributing

Please read `CONTRIBUTING.md` for details on our code of conduct and the process for submitting pull requests.

## License

This project is licensed under the GNU AGPLv3 License - see the `LICENSE.md` file for details.

## Authors

- Wes Hahn <westly.hahn@gmail.com>
