# Lumia Kenkyu

<!--toc:start-->
- [Lumia Kenkyu](#lumia-kenkyu)
  - [Game Data Processing Utilities](#game-data-processing-utilities)
  - [Project Structure](#project-structure)
  - [Components](#components)
  - [Setup](#setup)
  - [Configuration](#configuration)
  - [Usage](#usage)
    - [CLI Commands](#cli-commands)
  - [Error Handling](#error-handling)
  - [License](#license)
  - [Authors](#authors)
<!--toc:end-->

## Game Data Processing Utilities

This project contains utilities for retrieving, processing, and storing game data for Eternal Return. The utilities include a CLI tool for fetching game data, grouping it by teams, inserting it into a Supabase database, and various other data processing tasks.

## Project Structure

```
lumia-kenkyu/
├── pyproject.toml
├── README.md
└── src/
    └── matches/
        ├── CONSTS.py
        ├── game_data_cli.py
        ├── models/
        │   ├── game.py
        │   └── user.py
        ├── data_access/
        │   └── supabase.py
        ├── processors/
        │   ├── prepare_processors.py
        │   └── insertion_processors.py
        └── getter.py
```

## Components

- `CONSTS.py`: Contains constants and configuration settings.
- `game_data_cli.py`: Main CLI tool for all game data processing operations.
- `models/`: Defines data models for game and user information.
- `data_access/`: Contains database access layer (Supabase DAO).
- `processors/`: Includes data preparation and insertion strategy processors.
- `getter.py`: Functions for fetching game data from the API.

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

## Usage

The project now uses a unified CLI tool for all operations. To run the CLI tool, use Poetry to ensure you're in the correct virtual environment:

```
poetry run python src/matches/game_data_cli.py [COMMAND] [OPTIONS]
```

### CLI Commands

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

## Error Handling

If any errors occur during processing, the affected files or data will be logged, and in the case of file processing, problematic files will be moved to an error directory for further investigation.

## License

This project is licensed under the GNU AGPLv3 License - see the `LICENSE.md` file for details.

## Authors

- Wes Hahn <wes@cloudskipper.work>
