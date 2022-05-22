from flask import Flask, render_template, render_template_string
from BeautifulSoup import BeautifulSoup, Tag
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

def genHtml(file):
    with open(file, 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.find_all('table')
        table_index = 0
        addrs_tables = []
        if len(tables) > 1:
            table_index = 1

            addrs = tables[0].find_all('tr')[2].find('td').renderContents().decode('utf-8') .split('<br/>')

            for addr in addrs:
                # Remove newlines
                addr = addr.strip()
                #print(addr)
                groups = re.split(' ', addr, maxsplit=2)
                #print(groups)
                if groups[1] is not None:
                    addrs_tables.append(groups)
                    new_table = copy.copy(tables[table_index])
                    tables[table_index].insert_after(new_table)
            #print(addrs_tables)

        reg_page = False
        h1 = soup.find('h1')
        if "Register" in h1.string:
            reg_page = True
        
        tables = soup.find_all('table')
        #print(len(addrs_tables))
        
        reg = 0
        for table in range (0, max(len(addrs_tables), 1)):

            lines = tables[table + table_index].find_all('tr')
            for line in lines:
                append_index = 3
                if reg_page:
                    append_index = 2
                i = 0
                for col in line:
                    #print('col=', col)
                    if col == '\n':
                        append_index += 1
                    if i == append_index - 1:
                        reg = col.string
                    i += 1
                if len(line.find_all('td')) > 0:
                    #print('found td', line)
                    if reg_page:
                        reg = str(table) + ';' + reg + '->' + addrs_tables[table][0]
                    line.insert(append_index, BeautifulSoup(f'''<td>{reg}</td>''', 'html.parser'))
                    #break
                elif len(line.find_all('th')) > 0:
                    #print('found th', line, line.find_all('th'))
                    line.insert(append_index, BeautifulSoup(f'''<th >Value</th>''', 'html.parser'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ug1087-zynq-ultrascale-registers.htm')

@app.route('/<name>')
def route(name):
    return render_template(f'{name}')