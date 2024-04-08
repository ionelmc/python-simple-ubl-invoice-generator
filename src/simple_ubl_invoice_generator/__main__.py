"""
Entrypoint module, in case you use `python -msimple_ubl_invoice_generator`.


Why does this file exist, and why __main__? For more info, read:

- https://www.python.org/dev/peps/pep-0338/
- https://docs.python.org/2/using/cmdline.html#cmdoption-m
- https://docs.python.org/3/using/cmdline.html#cmdoption-m
"""

from simple_ubl_invoice_generator.cli import run

if __name__ == "__main__":
    run()
