from pathlib import Path


def system_type_hints() -> dict[str, str]:
    return {"mocker": "MockerFixture", "requests_mock": "RequestsMock"}


def get_hints() -> dict[str, str]:
    lines = Path("tests/conftest.py").read_text().splitlines()

    type_hints: dict[str, str] = system_type_hints()
    is_fixture = False
    for line in lines:
        if is_fixture and "def " in line:
            fixture_start = line.index("def ")
            fixture_end = line.index("(")
            fixture_name = line[fixture_start + 4 : fixture_end]
            print("fixture_name", fixture_name)
            arrow_at = line.index("->")
            fixture_type = line[arrow_at + 2 :].strip().strip(":")
            if fixture_type.startswith("Generator["):
                fixture_type = fixture_type[10:-1]
                fixture_type = fixture_type.split(", ")[0].strip()

            type_hints[fixture_name] = fixture_type
            is_fixture = False

        if line.startswith("@pytest.fixture"):
            is_fixture = True

    return type_hints


def set_hints(test_file: Path, type_hints: dict[str, str]) -> None:
    print(str(test_file).center(80, "-"))
    lines = test_file.read_text().splitlines()

    for index, line in enumerate(lines):
        param_hints = {}
        if "def test" in line:
            print("line", line)
            params_start = line.index("(")
            params_end = line.index(")")
            params_str = line[params_start + 1 : params_end]
            params = params_str.split(", ")
            for param_index, param in enumerate(params):
                print("param", param)
                if ":" in param:
                    param_no_hint, hint = param.split(":")
                    print("param", param_no_hint, "hint", hint)
                    param_hints[param_no_hint] = hint
                    params[param_index] = param_no_hint
                else:
                    param_hints[param] = type_hints.get(param, "")

            print("param_hints", param_hints)
            params_str = ", ".join(
                [f"{param}: {param_hints[param]}" if param_hints[param] else param for param in params]
            )

            if "->" in line:
                lines[index] = line[0 : params_start + 1] + params_str + line[params_end:]
            else:
                lines[index] = line[0 : params_start + 1] + params_str + line[params_end:-1] + " -> None:"

    test_file.write_text("\n".join(lines))


if __name__ == "__main__":
    hints = get_hints()
    print(hints)

    for py_file in Path("tests/unit").rglob("test_*.py"):
        set_hints(py_file, hints)

    for py_file in Path("tests/integration").rglob("test_*.py"):
        set_hints(py_file, hints)
