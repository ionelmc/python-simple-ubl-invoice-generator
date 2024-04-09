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
    customer: NotRequired[str | Company]
    correction: NotRequired[bool]
    date: date
    due: NotRequired[date]
    lines: list[InvoiceLine]
    filename: NotRequired[str]


class CompleteInvoice(TypedDict):
    id: str
    correction: bool
    customer: str | Company
    date: date
    due: date
    total: Decimal
    lines: list[CompleteInvoiceLine]


class InvoiceLineDefaults(TypedDict):
    service: str


class TimeDeltaArguments(TypedDict):
    days: int


class InvoiceDefaults(TypedDict):
    lines: NotRequired[InvoiceLineDefaults]
    customer: NotRequired[str]
    due: NotRequired[TimeDeltaArguments]
    filename: NotRequired[str]


class Config(TypedDict):
    supplier: Supplier
    customers: NotRequired[dict[str, Company]]
    defaults: NotRequired[InvoiceDefaults]
    invoices: dict[str, Invoice]
