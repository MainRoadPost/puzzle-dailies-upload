import argparse
import mimetypes
import os
import asyncio
from puzzle.client import Client, PostAddBlind
from puzzle.base_model import Upload
from puzzle.input_types import UserWithoutDomain, UserBy
from puzzle.exceptions import GraphQLClientHttpError
import dotenv


async def upload_post(puzzle_upload_url, username, project, path, description, tags, files):
    async with Client(puzzle_upload_url) as client:
        try:
            if files:
                upload_files = [
                    Upload(
                        filename=os.path.basename(file_path),
                        content=open(file_path, "rb"),
                        content_type=str(mimetypes.guess_type(os.path.basename(file_path))[0]),
                    )
                    for file_path in files
                    if os.path.exists(file_path)
                ]
            else:
                upload_files = []

            post_add = PostAddBlind(
                userBy=UserBy(withoutDomain=UserWithoutDomain(login=username)),
                projectCode=project,
                productPaths=path,
                description=description,
                tags=tags,
                uploads=upload_files,
            )

            result = await client.post_create_blind(post_add)
            print("Post created:", result.post_create_blind)

        except GraphQLClientHttpError as e:
            print(e)
            for error in e.response.json().get("errors"):
                print(error.get("message"))
            return


async def main():
    dotenv.load_dotenv()

    # Check if PUZZLE_API is set
    puzzle_upload_url = os.environ.get("PUZZLE_API")
    print(f"Puzzle upload URL: {puzzle_upload_url}")
    if not puzzle_upload_url:
        raise ValueError("PUZZLE_API not set")

    # Create an argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("--username")
    parser.add_argument("--project", required=True)
    parser.add_argument("--description")
    parser.add_argument("--files", nargs="+")
    parser.add_argument("--tags", nargs="+", required=False)
    parser.add_argument("--path", nargs="+", required=True)
    parser.add_argument("--src_files", nargs="+")

    # Parse the command line arguments
    args = parser.parse_args()
    username = args.username
    if username is None:
        username = os.environ.get("PUZZLE_USERNAME")
        if username is None:
            raise ValueError("Username not set and PUZZLE_USERNAME not set")
    project = args.project
    description_text = args.description
    files = args.files
    tags = args.tags if args.tags is not None else []
    path = args.path
    src_files = args.src_files

    description = {
        "ops": [
            {"insert": description_text + "\n"},
        ]
    }

    if src_files:
        for src in src_files:
            description["ops"].append({"insert": src})
            description["ops"].append({"attributes": {"list": "bullet"}, "insert": "\n"})
    description["ops"].append({"insert": "\n"})

    await upload_post(puzzle_upload_url, username, project, path, description, tags, files)


if __name__ == "__main__":
    asyncio.run(main())
