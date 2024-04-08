from datetime import date
from decimal import Decimal
from typing import NotRequired
from typing import TypedDict


class Company(TypedDict):
    street: str
    city: str
    county: str
    country: str
    fiscal_id: str
    name: str


class Supplier(Company):
    iban: str


class InvoiceLine(TypedDict):
    unit: NotRequired[str]
    amount: Decimal | int
    price: Decimal | int
    service: NotRequired[str]


class CompleteInvoiceLine(TypedDict):
    unit: str
    amount: Decimal | int
    price: Decimal | int
    total: Decimal
    service: str


class Invoice(TypedDict):
    customer: str | Company
    date: date
    due: NotRequired[date]
    lines: list[InvoiceLine]


class CompleteInvoice(TypedDict):
    customer: str | Company
    date: date
    due: date
    total: Decimal
    lines: list[CompleteInvoiceLine]


class InvoiceLineDefaults(TypedDict):
    service: str


class TimeDeltaArguments(TypedDict):
    days: int


class InvoiceDefault(TypedDict):
    lines: NotRequired[InvoiceLineDefaults]
    customer: NotRequired[str]
    due: NotRequired[TimeDeltaArguments]


class Config(TypedDict):
    supplier: Supplier
    customer: NotRequired[dict[str, Company]]
    default: NotRequired[InvoiceDefault]
    invoice: dict[str, Invoice]
