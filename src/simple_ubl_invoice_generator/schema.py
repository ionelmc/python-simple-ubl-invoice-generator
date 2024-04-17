import decimal
import enum
from datetime import date
from datetime import timedelta

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field


class Model(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        revalidate_instances="always",
    )


class Company(Model):
    street: str
    city: str
    county: str
    country: str
    fiscal_id: str
    name: str


class Supplier(Company):
    iban: str


class RoundingValues(enum.StrEnum):
    ROUND_CEILING = decimal.ROUND_CEILING
    ROUND_DOWN = decimal.ROUND_DOWN
    ROUND_FLOOR = decimal.ROUND_FLOOR
    ROUND_HALF_DOWN = decimal.ROUND_HALF_DOWN
    ROUND_HALF_EVEN = decimal.ROUND_HALF_EVEN
    ROUND_HALF_UP = decimal.ROUND_HALF_UP
    ROUND_UP = decimal.ROUND_UP
    ROUND_05UP = decimal.ROUND_05UP


class InvoiceLineDefaults(Model):
    rounding: RoundingValues | None = None
    unit: str | None = None
    service: str | None = None


class TimeDeltaArguments(Model):
    days: int


class InvoiceDefaults(Model):
    customer: str | None = None
    due: TimeDeltaArguments | None = None
    filename: str | None = None
    lines: InvoiceLineDefaults | None = None
    rounding: RoundingValues | None = None


class InvoiceLine(Model):
    amount: decimal.Decimal | int
    price: decimal.Decimal | int
    rounding: RoundingValues | None = None
    service: str = None
    unit: str = None
    total: decimal.Decimal = None


class Invoice(Model):
    correction: bool = False
    customer: str | Company = None
    date: date
    id: str = None
    due: date = None
    filename: str = None
    lines: list[InvoiceLine]
    rounding: RoundingValues | None = None
    total: decimal.Decimal = None

    def update_defaults(self, defaults: InvoiceDefaults):
        if self.filename is None:
            self.filename = defaults.filename or "{{ id }}.xml"
        if self.due is None:
            self.due = self.date + timedelta(**defaults.due.model_dump())
        if defaults.lines is not None:
            for line in self.lines:
                for field, value in defaults.lines.model_dump().items():
                    if getattr(line, field) is None:
                        setattr(line, field, value)
        if self.customer is None:
            self.customer = defaults.customer
        if self.rounding is None:
            self.rounding = defaults.rounding


class Config(Model):
    customers: dict[str, Company] = Field(default_factory=dict)
    defaults: InvoiceDefaults = Field(default_factory=InvoiceDefaults)
    invoices: dict[str, Invoice]
    supplier: Supplier
