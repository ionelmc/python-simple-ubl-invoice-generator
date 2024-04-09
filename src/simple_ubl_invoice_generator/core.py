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


class ValidationError(Exception):
    pass


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
    supplier = config["supplier"]
    customers = config.get("customers", {})
    defaults = config.get("defaults", {})
    invoice: CompleteInvoice
    line: CompleteInvoiceLine
    for invoice_id, invoice in config["invoices"].items():
        filename_default = "{{ id }}.xml"
        for field, default in defaults.items():
            match field:
                case "due":
                    invoice["due"] = invoice["date"] + timedelta(**default)
                case "lines":
                    for line in invoice["lines"]:
                        line.update(default)
                case "customer":
                    invoice["customer"] = default
                case "filename":
                    filename_default = default
                case _:
                    raise NotImplementedError
        if "customer" in invoice:
            customer = invoice["customer"]
        else:
            raise ValidationError(f"Failed processing {invoice_id}: Missing customer field.")
        if isinstance(customer, str):
            if customer in customers:
                invoice["customer"] = customers[customer]
            else:
                raise ValidationError(f"Failed processing {invoice_id}: Customer {customer!r} not in customers table.")
        total = Decimal(0)
        for line in invoice["lines"]:
            line["total"] = line_total = line["amount"] * line["price"]
            total += line_total
        invoice["total"] = total.quantize(ONE, rounding=ROUND_DOWN)
        invoice["id"] = invoice_id
        invoice.setdefault("correction", False)
        filename_template = jinja_env.from_string(invoice.pop("filename", filename_default))
        filename = filename_template.render(**invoice)
        logger.debug("Compiled invoice %s: %s", invoice_id, pformat(invoice))
        try:
            check_type(invoice, CompleteInvoice)
        except TypeCheckError as exc:
            raise ValidationError(f"Failed processing {invoice_id}: {exc}") from None

        destination_path.joinpath(filename).write_text(
            template.render(
                invoice=invoice,
                supplier=supplier,
            )
        )
