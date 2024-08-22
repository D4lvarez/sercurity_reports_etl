def read_file(path: str) -> str:
    content = None

    with open(path) as file:
        content = file.read()

    if content is None:
        raise ValueError("file is empty.")

    return content
