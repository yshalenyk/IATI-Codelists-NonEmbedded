"""

Converts codelist files from external sources into the format used by IATI.

Note not all external codelists are converted automatically yet.

"""

from lxml import etree as ET

"""

IANA Media Types (FileFormat)

"""

template = ET.parse('templates/FileFormat.xml', ET.XMLParser(remove_blank_text=True))
codelist_items = template.find('codelist-items')

media_types = ET.parse('source/media-types.xml')
for registry in media_types.findall('{http://www.iana.org/assignments}registry'):
    registry_id = registry.attrib['id']
    for record in registry.findall('{http://www.iana.org/assignments}record'):
        codelist_item = ET.Element('codelist-item')

        code = ET.Element('code')
        code.text = registry_id + '/' + record.find('{http://www.iana.org/assignments}name').text
        codelist_item.append(code)

        category = ET.Element('category')
        category.text = registry_id
        codelist_item.append(category)

        codelist_items.append(codelist_item)

template.write('xml/FileFormat.xml', pretty_print=True)



"""

ISO Country Alpha 2

"""

XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'

template = ET.parse('templates/Country.xml', ET.XMLParser(remove_blank_text=True))
codelist_items = template.find('codelist-items')

countries = ET.parse('source/iso_country_codes.xml')
for country in countries.findall('country'):
    if country.find('status').text == 'officially-assigned':
        codelist_item = ET.Element('codelist-item')

        code = ET.Element('code')
        code.text = country.find('alpha-2-code').text
        codelist_item.append(code)
        
        for short_name in country.findall('short-name'):
            if XML_LANG in short_name.attrib:
                name = ET.Element('name')
                name.attrib[XML_LANG] = short_name.attrib[XML_LANG]
                name.text = short_name.text
                codelist_item.append(name)

        for full_name in country.findall('full-name'):
            if XML_LANG in full_name.attrib:
                description = ET.Element('description')
                description.attrib[XML_LANG] = full_name.attrib[XML_LANG]
                description.text = full_name.text
                codelist_item.append(description)

        codelist_items.append(codelist_item)

template.write('xml/Country.xml', pretty_print=True)



"""

ISO Currency Alpha Code

"""

template = ET.parse('templates/Currency.xml', ET.XMLParser(remove_blank_text=True))
codelist_items = template.find('codelist-items')

currency_codes = {}
country_currencies = ET.parse('source/table_a1.xml')
for country_currency in country_currencies.find('CcyTbl').findall('CcyNtry'):
    currency_name = country_currency.find('CcyNm').text
    if currency_name == 'No universal currency':
        continue
    currency_code = country_currency.find('Ccy').text
    if currency_code in currency_codes:
        assert currency_codes[currency_code] == currency_name
    else:
        currency_codes[currency_code] = currency_name

for currency_code, currency_name in sorted(currency_codes.items()):
    codelist_item = ET.Element('codelist-item')

    code = ET.Element('code')
    code.text = currency_code
    codelist_item.append(code)
    
    name = ET.Element('name')
    name.text = currency_name
    codelist_item.append(name)

    codelist_items.append(codelist_item)

template.write('xml/Currency.xml', pretty_print=True)

