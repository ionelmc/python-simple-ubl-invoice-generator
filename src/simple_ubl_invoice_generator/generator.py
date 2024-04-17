from decimal import Decimal
from logging import getLogger
from pathlib import Path

import jinja2
from pydantic import ValidationError

from .schema import Config

logger = getLogger(__name__)

DOT01 = Decimal(".01")
DOT0001 = Decimal(".0001")


class ConfigError(Exception):
    pass


def generate(template_path: Path, config_data: dict, destination_path: Path):
    try:
        config: Config = Config(**config_data)
    except ValidationError as exc:
        raise ConfigError(f"Failed validating config {config_data}: {exc}") from None

    jinja_env = jinja2.Environment(
        autoescape=True,
        keep_trailing_newline=True,
        loader=jinja2.FileSystemLoader(template_path.parent),
        lstrip_blocks=True,
        trim_blocks=True,
    )

    template = jinja_env.get_template(template_path.name)
    supplier = config.supplier
    customers = config.customers
    defaults = config.defaults
    for invoice_id, invoice in config.invoices.items():
        invoice.update_defaults(defaults)
        customer = invoice.customer
        if customer is None:
            raise ConfigError(f"Failed processing {invoice_id}: Missing customer field.")
        elif isinstance(customer, str):
            if customer in customers:
                invoice.customer = customers[customer]
            else:
                raise ConfigError(f"Failed processing {invoice_id}: Customer {customer!r} not in customers table.")
        total = Decimal(0)
        for line in invoice.lines:
            price = line.price
            line_total = line.amount * price
            if line.rounding:
                line_total = line_total.quantize(*line.rounding)
            line_total = line_total.quantize(DOT01)
            total += line_total
            line.total = line_total
            line.price = price.quantize(DOT0001)
        if invoice.rounding:
            total = total.quantize(*invoice.rounding)
        invoice.total = total.quantize(DOT01)
        invoice.id = invoice_id
        try:
            invoice.model_validate(invoice, strict=True)
        except ValidationError as exc:
            raise ConfigError(f"Failed validating invoice {invoice}: {exc}") from None
        logger.debug("Compiled invoice: %s", invoice)
        filename_template = jinja_env.from_string(invoice.filename)
        filename = filename_template.render(invoice)
        destination_path.joinpath(filename).write_text(
            template.render(
                invoice=invoice,
                supplier=supplier,
            )
        )
