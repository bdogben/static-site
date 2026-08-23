def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[:2] == "# ":
            return line[2:].strip()
    raise Exception ("no header")
