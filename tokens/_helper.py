from pathlib import Path


def _find_token_dir() -> Path:
    """Returns the directory containing this file."""
    this_dir = Path(__file__).absolute().parent
    return this_dir


def _find_token_file(file: Path | str) -> Path:
    """Given a `file` which may be a relative path or simple filename,
    `_find_token_file` constructs an absolute filepath with a .txt extension
    and raises `FileNotFoundError` if it doesn't exist. Otherwise, it returns
    the filepath.

    Examples:
    - `_find_token_file("foo")` looks for `foo.txt` in the token directory,
    - `_find_token_file("bar.txt")` looks for `bar.txt` in the token directory,
    - `_find_token_file(Path("foobar"))` looks for `foobar.txt` in the token
    directory,
    - and so on.
    """
    if isinstance(file, Path):
        if file.is_absolute():
            filepath = file.with_suffix(".txt")
        else:
            token_dir = _find_token_dir()
            filepath = (token_dir / file.name).with_suffix(".txt")
    else:
        file = Path(file)
        filepath = _find_token_file(file=file)

    if filepath.exists():
        return filepath
    else:
        print(f"Looked for {filepath} but could not find it.")
        print()
        raise FileNotFoundError


def _parse_token_file(lines: list[str]) -> str:
    """"""
    actual_token = ""
    for line in lines:
        line.strip()
        split_line = line.split("#", 1)
        text_to_keep = split_line[0]
        actual_token = actual_token + text_to_keep
    return actual_token


def get_token(file: Path | str):
    """"""
    filepath = _find_token_file(file)
    with filepath.open() as f:
        contents = f.readlines()
    token = _parse_token_file(contents)
    return token
