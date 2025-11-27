# Puzzle dailies uploader

Example of creating posts in Puzzle via GraphQL

## Description

The application shows how to create posts with attached files (videos, images, PDF documents) using the API without user authorisation.

To run the example, execute the following command

```bash
uv run --script ./dailies-upload.py --username ‘user_login’ --project ‘MyAwesomeProject’ --path ‘episode01/shot010’ --description ‘final version 34’ --tags “comp” ‘for_review’ --files ‘path/to/file1’ ‘path/to/file2’
```

#### Parameters:

- `--username` - username/login
- `--project` - project name
- `--path` - path to the product within the project (must be created in advance)
- `--description` - post text
- `--tags` - tags that will be added to the post
- `--files` - files that will be uploaded to Puzzle
- `--src_files` - files whose paths will be added to the post text as links ( path to exr sequence, etc )

## Python venv setup
Before running script create a python venv by running
```bash
uv sync
```

Then execute following command to generate a `puzzle` module from GraphQL schema
```bash
uv run ariadne-codegen
```

## Changing the generated client

The GraphQL client for Puzzle is generated into the `puzzle` module by `ariadne-codegen`. Do not edit the generated client code by hand.

To update the client after schema or query changes:

1. Make sure `schema.graphql` contains an up-to-date schema.
2. Update `queries.graphql` with the required queries/mutations.
3. Regenerate the client:

   ```bash
   uv run ariadne-codegen
   ```

**Note:** Running `ariadne-codegen` is required before the first run and after any changes to schema or query files.

## Updating the schema

To update the schema you need the `cynic-cli` tool (requires [Rust](https://www.rust-lang.org/tools/install) to be installed):

```shell
cargo install --git https://github.com/obmarg/cynic.git cynic-cli
```

After installing `cynic-cli`, run `./get-schema.sh > schema.graphql` in the repository root to authenticate against the Puzzle server and download the current GraphQL schema.

The script expects the following environment variables to be set in `.env`:

- `PUZZLE_API` — GraphQL endpoint URL of the Puzzle server.
- `PUZZLE_USER_DOMAIN` — studio domain (leave blank if not used).
- `PUZZLE_USERNAME` — username to authenticate with.
- `PUZZLE_PASSWORD` — password for the user.

Optionally, set `LOG_LEVEL` (e.g., `LOG_LEVEL=INFO`) to control logging verbosity.

See `example.env` for an example `.env` file.
