from itertools import groupby
from pathlib import Path
from typing import List

MYPY_CSV_LENGTH = 4


class MypyError:
    def __init__(self, *, file: str, line: int, type: str, message: str, code: str) -> None:
        self.file = file
        self.line = line
        self.type = type
        self.message = message
        self.code = code


def fix_ignore_without_code(path: str, mypy_output: str, ext: str = "") -> None:
    lines = Path(mypy_output).read_text().splitlines()

    errors: List[MypyError] = []
    for line in lines:
        parts = line.split(":", maxsplit=3)
        if len(parts) < MYPY_CSV_LENGTH:
            continue

        line_number = int(parts[1])
        last_open_bracket = line.rfind("[")
        code = line[last_open_bracket + 1 : -1]
        errors.append(
            MypyError(
                file=parts[0],
                line=line_number,
                type=parts[2].strip(),
                message=parts[3].strip(),
                code=code,
            )
        )

    grouped_errors = groupby(errors, lambda e: e.file)
    for file, errors_in_group in grouped_errors:
        lines = Path(path, file).read_text().splitlines()
        print(file.center(80, "="))
        for error in errors_in_group:
            if error.code != "ignore-without-code":
                continue
            print(error.line)
            print(lines[error.line - 1])
            consider_at = error.message.find("consider")
            instead_at = error.message.find("instead")
            consider = error.message[consider_at + 8 : instead_at].strip().strip('"')
            consider = "# " + consider

            lines[error.line - 1] = lines[error.line - 1].replace("# type: ignore", consider)
            print(lines[error.line - 1])

        Path(path, file + ext).write_text("\n".join(lines))
