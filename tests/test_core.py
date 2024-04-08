import tomllib
from decimal import Decimal

import pytest

from simple_ubl_invoice_generator.cli import template_path
from simple_ubl_invoice_generator.core import generate


@pytest.mark.parametrize(
    ("config", "error"),
    [
        (
            "test_no_customer_match_1.toml",
            "Failed processing config: value of key 'FACT001' of value of key 'invoice' of dict is missing required key(s): \"customer\"",
        ),
        ("test_no_customer_match_2.toml", "Failed processing FACT001: KeyError('customer')"),
    ],
)
def test_no_customer_match(tmp_path, tests_path, config, error):
    with pytest.raises(ValueError) as exc:  # noqa:PT011
        generate(template_path, tomllib.loads(tests_path.joinpath(config).read_text(), parse_float=Decimal), tmp_path)
    assert str(exc.value) == error


@pytest.mark.parametrize(
    "config",
    [
        "test_no_defaults.toml",
        "test_all_defaults.toml",
    ],
)
def test_generation(tmp_path, tests_path, config):
    generate(template_path, tomllib.loads(tests_path.joinpath(config).read_text(), parse_float=Decimal), tmp_path)
    assert (
        tmp_path.joinpath("FACT001.xml").read_text()
        == """<?xml version="1.0" encoding="UTF-8"?>
<Invoice xmlns="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2"
         xmlns:cbc="urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
         xmlns:cac="urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="urn:oasis:names:specification:ubl:schema:xsd:Invoice-2 http://docs.oasis-open.org/ubl/os-UBL-2.1/xsd/maindoc/UBL-Invoice-2.1.xsd">
    <cbc:CustomizationID>urn:cen.eu:en16931:2017#compliant#urn:efactura.mfinante.ro:CIUS-RO:1.0.1</cbc:CustomizationID>
    <cbc:ID>FACT001</cbc:ID>
    <cbc:IssueDate>2001-01-01</cbc:IssueDate>
    <cbc:DueDate>2001-02-02</cbc:DueDate>
    <cbc:InvoiceTypeCode>380</cbc:InvoiceTypeCode>
    <cbc:Note></cbc:Note>
    <cbc:DocumentCurrencyCode>RON</cbc:DocumentCurrencyCode>
    <cac:AccountingSupplierParty>
        <cac:Party>
            <cac:PostalAddress>
                <cbc:StreetName>asdf street</cbc:StreetName>
                <cbc:CityName>asdf city</cbc:CityName>
                <cbc:CountrySubentity>asdf county</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>asdf country</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyTaxScheme>
                <cbc:CompanyID>1234</cbc:CompanyID>
                <cac:TaxScheme/>
            </cac:PartyTaxScheme>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>ASDF S.R.L.</cbc:RegistrationName>
                <cbc:CompanyID>1234</cbc:CompanyID>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingSupplierParty>
    <cac:AccountingCustomerParty>
        <cac:Party>
            <cac:PostalAddress>
                <cbc:StreetName>qwer street</cbc:StreetName>
                <cbc:CityName>qwer city</cbc:CityName>
                <cbc:CountrySubentity>qwer county</cbc:CountrySubentity>
                <cac:Country>
                    <cbc:IdentificationCode>qwer country</cbc:IdentificationCode>
                </cac:Country>
            </cac:PostalAddress>
            <cac:PartyLegalEntity>
                <cbc:RegistrationName>QWER S.R.L</cbc:RegistrationName>
                <cbc:CompanyID>RO234</cbc:CompanyID>
            </cac:PartyLegalEntity>
        </cac:Party>
    </cac:AccountingCustomerParty>
    <cac:PaymentMeans>
        <cbc:PaymentMeansCode>42</cbc:PaymentMeansCode>
        <cac:PayeeFinancialAccount>
            <cbc:ID>IBAN123</cbc:ID>
            <cbc:Name>ASDF S.R.L.</cbc:Name>
        </cac:PayeeFinancialAccount>
    </cac:PaymentMeans>
    <cac:PaymentTerms>
        <cbc:Note></cbc:Note>
    </cac:PaymentTerms>
    <cac:TaxTotal>
        <cbc:TaxAmount currencyID="RON">0.00</cbc:TaxAmount>
        <cac:TaxSubtotal>
            <cbc:TaxableAmount currencyID="RON">1230</cbc:TaxableAmount>
            <cbc:TaxAmount currencyID="RON">0.00</cbc:TaxAmount>
            <cac:TaxCategory>
                <cbc:ID>O</cbc:ID>
                <cbc:Percent>0.00</cbc:Percent>
                <cbc:TaxExemptionReasonCode>VATEX-EU-O</cbc:TaxExemptionReasonCode>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:TaxCategory>
        </cac:TaxSubtotal>
    </cac:TaxTotal>
    <cac:LegalMonetaryTotal>
        <cbc:LineExtensionAmount currencyID="RON">1230</cbc:LineExtensionAmount>
        <cbc:TaxExclusiveAmount currencyID="RON">1230</cbc:TaxExclusiveAmount>
        <cbc:TaxInclusiveAmount currencyID="RON">1230</cbc:TaxInclusiveAmount>
        <cbc:PayableAmount currencyID="RON">1230</cbc:PayableAmount>
    </cac:LegalMonetaryTotal>
    <cac:InvoiceLine>
        <cbc:ID>1</cbc:ID>
        <cbc:InvoicedQuantity unitCode="HUR">10</cbc:InvoicedQuantity>
        <cbc:LineExtensionAmount currencyID="RON">1230.00</cbc:LineExtensionAmount>
        <cac:Item>
            <cbc:Name>Service</cbc:Name>
            <cac:ClassifiedTaxCategory>
                <cbc:ID>O</cbc:ID>
                <cac:TaxScheme>
                    <cbc:ID>VAT</cbc:ID>
                </cac:TaxScheme>
            </cac:ClassifiedTaxCategory>
        </cac:Item>
        <cac:Price>
            <cbc:PriceAmount currencyID="RON">123.00</cbc:PriceAmount>
        </cac:Price>
    </cac:InvoiceLine>
</Invoice>
"""
    )
