"""
Module that contains the command line app.

Why does this file exist, and why not put this in __main__?

  You might be tempted to import things from __main__ later, but that will cause
  problems: the code will get executed twice:

  - When you run `python -msimple_ubl_invoice_generator` python will execute
    ``__main__.py`` as a script. That means there will not be any
    ``simple_ubl_invoice_generator.__main__`` in ``sys.modules``.
  - When you import __main__ it will get executed again (as a module) because
    there"s no ``simple_ubl_invoice_generator.__main__`` in ``sys.modules``.

  Also see (1) from http://click.pocoo.org/5/setuptools/#setuptools-integration
"""

import argparse
import logging
import tomllib
from decimal import Decimal
from pathlib import Path

from . import __version__
from .generator import generate
from .utils import pformat

logger = logging.getLogger(__name__)

template_path = Path(__file__).parent / "template.xml"

parser = argparse.ArgumentParser(description="Command description.")
parser.add_argument(
    "config",
    metavar="CONFIG",
    type=argparse.FileType("rb"),
    help="Invoice TOML config file.",
)
parser.add_argument(
    "--template",
    "-t",
    metavar="TEMPLATE",
    default=template_path,
    type=Path,
    help="Invoice UBL Jinja2 template. Default: %(default)s",
)
parser.add_argument(
    "--output-path",
    "-o",
    metavar="OUTPUT_PATH",
    default=Path.cwd(),
    type=Path,
    help="Output path for resulting invoice XML files. Default: %(default)s",
)
parser.add_argument(
    "--verbose",
    "-v",
    action="store_true",
)
parser.add_argument(
    "--version",
    action="version",
    version=f"%(prog)s v{__version__}",
)


def run(args=None):
    args = parser.parse_args(args=args)
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

    if not args.template.exists():
        parser.exit(1, f"{args.template} does not exist.")

    with args.config as fh:
        config = tomllib.load(fh, parse_float=Decimal)

    logger.debug("Loaded %s", pformat(config))

    generate(args.template, config, args.output_path)
    parser.exit(0)
