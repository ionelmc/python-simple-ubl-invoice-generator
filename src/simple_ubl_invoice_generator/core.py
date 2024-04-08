from datetime import timedelta
from decimal import ROUND_DOWN
from decimal import Decimal
from logging import getLogger
from pathlib import Path

import jinja2
from typeguard import TypeCheckError
from typeguard import check_type

from .types import CompleteInvoice
from .types import CompleteInvoiceLine
from .types import Config
from .utils import pformat

logger = getLogger(__name__)

ONE = Decimal(1)


def generate(template_path: Path, config: Config, destination_path: Path):
    try:
        check_type(config, Config)
    except TypeCheckError as exc:
        raise ValueError(f"Failed processing config: {exc}") from None

    jinja_env = jinja2.Environment(
        autoescape=True,
        keep_trailing_newline=True,
        loader=jinja2.FileSystemLoader(template_path.parent),
        lstrip_blocks=True,
        trim_blocks=True,
    )

    template = jinja_env.get_template(template_path.name)

    defaults = config.get("default", {})
    invoice: CompleteInvoice
    line: CompleteInvoiceLine
    for invoice_id, invoice in config["invoice"].items():
        for field, default in defaults.items():
            if field == "due":
                invoice["due"] = invoice["date"] + timedelta(**default)
            elif field == "lines":
                for line in invoice["lines"]:
                    line.update(default)
        customer = invoice["customer"]
        if isinstance(customer, str):
            try:
                invoice["customer"] = config["customer"][customer]
            except KeyError as exc:
                raise ValueError(f"Failed processing {invoice_id}: {exc!r}") from None
        total = Decimal(0)
        for line in invoice["lines"]:
            line["total"] = line_total = line["amount"] * line["price"]
            total += line_total
        invoice["total"] = total.quantize(ONE, rounding=ROUND_DOWN)
        logger.debug("Compiled invoice %s: %s", invoice_id, pformat(invoice))
        try:
            check_type(invoice, CompleteInvoice)
        except TypeCheckError as exc:
            raise ValueError(f"Failed processing {invoice_id}: {exc}") from None

        destination_path.joinpath(f"{invoice_id}.xml").write_text(
            template.render(
                **invoice,
                id=invoice_id,
                supplier=config["supplier"],
            )
        )
