# pragma: no cover

from click import Path, argument, command, group, option

from mypy_helper.fix_ignore_without_code import fix_ignore_without_code


@group()
def mypy_helper() -> None:
    pass


@command(
    "fix-ignore-without-code",
    help="Fix ignore without code. Use this before you have tried your best to eleminate the ignore",
)
@argument("path", type=Path(exists=True, file_okay=True, dir_okay=True))
@argument("mypy_output", type=Path(exists=True, file_okay=True, dir_okay=False))
@option("-e", "--ext", type=str, help="Append another extension", default="")
def fix_ignore_without_code_command(path: str, mypy_output: str, ext: str = "") -> None:
    fix_ignore_without_code(path, mypy_output, ext)


mypy_helper.add_command(fix_ignore_without_code_command)
