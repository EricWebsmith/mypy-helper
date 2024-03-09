from pathlib import Path


def compare_files(file1: str, file2: str) -> None:
    with Path(file1).open() as f1, Path(file2).open() as f2:
        for line1, line2 in zip(f1, f2):
            assert line1 == line2
