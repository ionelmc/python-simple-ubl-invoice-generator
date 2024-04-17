import subprocess

import pytest


def test_version():
    assert subprocess.check_output(["sublig", "--version"], text=True).startswith("sublig v")


def test_bad_template(tmp_path, tests_path):
    with pytest.raises(subprocess.CalledProcessError) as exc:
        subprocess.check_output(
            ["sublig", f"--template={tmp_path / 'foobar'}", tests_path / "test_filename.toml"], text=True, stderr=subprocess.STDOUT
        )
    assert exc.value.stdout.endswith("foobar does not exist.")
    assert exc.value.returncode == 1
