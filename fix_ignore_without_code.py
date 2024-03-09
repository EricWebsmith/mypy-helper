from itertools import groupby
from pathlib import Path

from pydantic import BaseModel


class MypyError(BaseModel):
    file: str
    line: int
    type: str
    message: str
    code: str


def main():
    lines = Path("logs/result.txt").read_text().splitlines()

    errors: list[MypyError] = []
    for line in lines:
        print(line.strip())
        parts = line.split(":", maxsplit=3)
        if len(parts) < 4:
            continue

        line_number = int(parts[1])
        last_open_bracket = line.rfind("[")
        code = line[last_open_bracket + 1 : -1]
        errors.append(
            MypyError(file=parts[0], line=line_number, type=parts[2].strip(), message=parts[3].strip(), code=code)
        )

    for error in errors:
        print(error)

    grouped_errors = groupby(errors, lambda e: e.file)
    for file, errors in grouped_errors:
        errors = list(errors)
        print(file, len(errors))
        lines = Path(file).read_text().splitlines()
        for error in errors:
            print(lines[error.line - 1])
            consider_at = error.message.find("consider")
            instead_at = error.message.find("instead")
            consider = error.message[consider_at + 8 : instead_at].strip().strip('"')
            consider = "# " + consider

            lines[error.line - 1] = lines[error.line - 1].replace("# type: ignore", consider)
            print(lines[error.line - 1])

        Path(file).write_text("\n".join(lines))


if __name__ == "__main__":
    main()
