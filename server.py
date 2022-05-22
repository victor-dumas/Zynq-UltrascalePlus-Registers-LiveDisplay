from flask import Flask, render_template, render_template_string
from bs4 import BeautifulSoup
import copy
import re


def getBits(value, bits):
    result = 0
    splits = bits.split(':')
    bin_list = [int(x) for x in bin(value)[2:]]
    
    start = len(bin_list) - int(splits[0]) - 1
    end = start + 1
    if len(splits) > 1:
        end = len(bin_list) - int(splits[1])
    
    for bit in bin_list[start:end]:
        result = (result << 1) | bit

    return result

'''
@brief  Inserts tables for each register and display current value
        Handles both module and register pages
'''
def genHtml(file):
    with open(f'templates/{file}', 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.find_all('table')
        addrs_tables = []

        reg_page = False
        h2 = soup.find('h2')
        if h2 is not None and "Register" in h2.string:
            reg_page = True

        if len(tables) == 2:
            addrs = tables[0].find_all('tr')[2].find('td').renderContents().decode('utf-8') .split('<br/>')

            for addr in addrs:
                # Remove newlines
                addr = addr.strip()
                groups = re.split(' ', addr, maxsplit=2)
                if len(groups) > 1:
                    addrs_tables.append(groups)
                    new_table = copy.copy(tables[1])
                    tables[1].insert_after(new_table)
        else:
            return render_template(file)

        print(addrs_tables)
        
        tables = soup.find_all('table')
        
        reg = 0
        for table in range (0, max(len(addrs_tables), 1)):

            lines = tables[table + 1].find_all('tr')
            for line in lines:
                append_index = 2
                i = 0
                for col in line:
                    if col == '\n':
                        append_index += 1
                    if i == append_index - 1:
                        reg = col.string
                    i += 1
                if len(line.find_all('td')) > 0:
                    selection = ""
                    if reg_page:
                        selection = f'->{reg}'
                        reg = int(addrs_tables[table][0], 16)
                    else:
                        reg = int(reg, base = 16) + int(addrs_tables[table][0], base = 16)
                    line.insert(append_index, BeautifulSoup(f'''<td class='hex'>0x{reg:08X}''' + selection + '''</td>''', 'html.parser'))
                elif len(line.find_all('th')) > 0:
                    line.insert(append_index, BeautifulSoup(f'''<th >Value</th>''', 'html.parser'))
        return render_template_string(str(soup))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ug1087-zynq-ultrascale-registers.htm')

@app.route('/<name>')
def route(name):
    print(name)
    if re.match('.*\.html', name):
        return genHtml(f'{name}')
    else:
        return render_template(f'{name}')