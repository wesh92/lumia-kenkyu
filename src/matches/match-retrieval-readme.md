# Lumia Kenkyu

<!--toc:start-->
- [Lumia Kenkyu](#lumia-kenkyu)
  - [Match Retrieval Utilities](#match-retrieval-utilities)
  - [Project Structure](#project-structure)
  - [Files](#files)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [Fetching and Grouping Game Data](#fetching-and-grouping-game-data)
    - [Inserting Data into Supabase](#inserting-data-into-supabase)
  - [Error Handling](#error-handling)
  - [License](#license)
  - [Authors](#authors)
<!--toc:end-->

## Match Retrieval Utilities

This directory contains utilities for retrieving, processing, and storing match data for Eternal Return. The utilities include scripts for fetching game data, grouping it by teams, and inserting it into a Supabase database.

## Project Structure

```
lumia-kenkyu/
├── pyproject.toml
├── README.md
└── src/
    └── matches/ <-- You are here
        ├── CONSTS.py
        ├── game.py
        ├── getter.py
        ├── grouper.py
        └── inserter.py
```

## Files

- `CONSTS.py`: Contains constants and configuration settings.
- `game.py`: Defines data models for game and player information.
- `getter.py`: Functions for fetching game data from an API.
- `grouper.py`: Groups game data by teams and writes it to JSON files.
- `inserter.py`: Inserts processed game data into a Supabase database.

## Setup

1. Clone this repository.
2. Ensure you have Poetry installed. If not, install it following the instructions at [Python Poetry Docs.](https://python-poetry.org/docs/#installation).
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

## Usage

To run the scripts, use Poetry to ensure you're in the correct virtual environment:

### Fetching and Grouping Game Data

To fetch game data and group it by teams, run:

```
poetry run python src/matches/grouper.py --count <number_of_games> --output_dir <output_directory> --delay <delay_between_requests>
```

Options:
- `--count`: Number of game IDs to generate and process (default: 100)
- `--output_dir`: Directory to write output JSON files (default: "output_examples")
- `--delay`: Delay in seconds between processing each game (default: 1.33)

### Inserting Data into Supabase

To process the JSON files and insert the data into Supabase, run:

```
poetry run python src/matches/inserter.py
```

This script will process all JSON files in the `output_examples` directory (or the directory specified in `CONSTS.py`), insert the data into Supabase, and move processed files to an archive directory.

## Error Handling

If any errors occur during processing, the affected game folders will be moved to an error directory for further investigation.

## License

This project is licensed under the GNU AGPLv3 License - see the `LICENSE.md` file for details.

## Authors

- Wes Hahn <westly.hahn@gmail.com>
