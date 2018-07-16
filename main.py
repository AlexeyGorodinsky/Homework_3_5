import requests
import xml.etree.ElementTree as ET
from chardet.universaldetector import UniversalDetector

# Задача № 1 -------------------------


def fahrenheit_to_celsius(fahrenheit_temp):

    headers = {"Content-Type": "text/xml"}
    data = f'''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"
xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <FahrenheitToCelsius xmlns="https://www.w3schools.com/xml/">
      <Fahrenheit>{fahrenheit_temp}</Fahrenheit>
    </FahrenheitToCelsius>
  </soap:Body>
</soap:Envelope>'''

    res = requests.post("https://www.w3schools.com/xml/tempconvert.asmx", data=data, headers=headers)
    root = ET.fromstring(res.text)
    celsius_temp = float(root[0][0][0].text)
    return round(celsius_temp, 1)


def code_type(filename):

    detector = UniversalDetector()

    with open(filename, 'rb') as file:
        for line in file:
            detector.feed(line)
            if detector.done:
                break
        detector.close()
    code_type = detector.result['encoding']
    print('Файл {} выполнен в кодировке {}'.format(filename, code_type))
    return code_type


def avg_temp(filename):

    with open(filename, 'r', encoding=code_type(filename)) as f:
        temp = f.read().split()
        temp_amounts = [int(s) for s in temp if s.isdigit()]
        avg_temp = sum(temp_amounts)/len(temp_amounts)
        return round(avg_temp, 1)


filename = 'temps.txt'
print(f'Средняя температура в Фаренгейтах: {avg_temp(filename)}')

fahrenheit_temp = avg_temp(filename)

print(f'Средняя температура в Цельсиях: {fahrenheit_to_celsius(fahrenheit_temp)}')

# Задача № 2 -------------------------


def currencies(value, cur_from, cur_to):
    res = requests.post(
        'http://fx.currencysystem.com/webservices/CurrencyServer4.asmx',
        headers={
            'Content-Type': 'text/xml; charset=utf-8'
        },
        data='''<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <ConvertToNum xmlns="http://webservices.cloanto.com/currencyserver/">
      <licenseKey></licenseKey>
      <fromCurrency>'''+ str(cur_from) +'''</fromCurrency>
      <toCurrency>'''+ str(cur_to) +'''</toCurrency>
      <amount>''' + str(value) + '''</amount>
      <rounding>true</rounding>
      <date></date>
      <type></type>
    </ConvertToNum>
  </soap:Body>
</soap:Envelope>'''
    )

    root = ET.fromstring(res.text)
    return root[0][0][0].text


print('\n')
print('------------------')
print('\n')
with open('currencies.txt') as f:
    cur_to = 'RUB'
    flights = []
    for line in f:
        flight = (line.strip()).split(' ')
        flights.append(int(float(currencies(flight[1], flight[2], cur_to))))
    print(f'Общая стоиомсть перелетов: {sum(flights)} рбулей')
