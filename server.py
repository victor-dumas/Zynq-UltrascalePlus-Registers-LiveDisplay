from flask import Flask, render_template, render_template_string, request
from bs4 import BeautifulSoup
import copy
import json
import re
import time

from comm import Comm

hostname = '192.168.9.1'

'''
@brief  Get bits from value using the selected mask (bits)
        The masks has a VHDL syntax (e.g. [8:16])
'''
def getBits(value, bits):
    result = 0
    splits = bits.split(':')
    # Value to binary array
    bin_list = [int(x) for x in bin(value)[2:]]
    
    start = len(bin_list) - int(splits[0]) - 1
    if start < 0:
        start = 0
    end = start + 1
    if len(splits) > 1:
        end = len(bin_list) - int(splits[1])
    
    # Binary array to value (selecting only the masked bits)
    for bit in bin_list[start:end]:
        result = (result << 1) | bit

    return result

'''
@brief  Inserts tables for each register and display current value of each register/bits per module
        Handles both module and register pages
'''
def genHtml(file):
    with open(f'templates/{file}', 'r') as html:
        soup = BeautifulSoup(html, 'html.parser')

        tables = soup.find_all('table')
        addrs_tables = []

        if len(tables) == 2:
            # Get the base addresses for all registers for module pages and the register being dissected for a reg page
            addrs_soup = tables[0].find_all('tr')[2].find('td')
            addrs = addrs_soup.renderContents().decode('utf-8').split('<br/>')
            addrs_soup.clear()

            # Get the addresses and names of each register for a module
            for i, addr in enumerate(addrs):
                # Remove newlines
                addr = addr.strip()
                groups = re.split(' ', addr, maxsplit=2)
                # Check that both address and name are present
                if len(groups) > 1:
                    # Table title
                    addrs_tables.append(groups)
                    table_title = soup.new_tag('h2', id=groups[0])
                    table_title.append(f'{groups[1]}')
                    # Link for navigating to the top of the page
                    table_fast_top = soup.new_tag('a', href='#top')
                    table_fast_top.string = u'\u21E7'
                    table_title.append(table_fast_top)
                    # Table containing the values
                    tables[1].insert_before(table_title)
                    new_table = copy.copy(tables[1])
                    table_title.insert_after(new_table)
                    # Links to get to each base address table
                    addr_href = soup.new_tag('a', href=f'#{groups[0]}', id='top')
                    addr_href.string = addr
                    addrs_soup.append(addr_href)
                    addrs_soup.append(soup.new_tag('br'))
        else:
            # If the page is not recognized as a module/register page then return the render of the original HTML page
            return render_template(file)
        
        # Add live js script
        liveview = soup.new_tag('script', type='text/javascript', language='javascript', src='static/scripts/liveview.js')
        soup.find('head').append(liveview)

        # Record if the current page is a register page or a module page
        reg_page = False
        h2 = soup.find('h2')
        if h2 is not None and "Register" in h2.string:
            reg_page = True
        
        tables = soup.find_all('table')
        
        reg = 0
        for table in range (0, max(len(addrs_tables), 1)):
            # For each line in the table
            lines = tables[table + 1].find_all('tr')
            for line in lines:
                append_index = 2
                i = 0
                # Remove empty columns
                for col in line:
                    if col == '\n':
                        append_index += 1
                    if i == append_index - 1:
                        reg = col.string
                    i += 1
                # Value line
                if len(line.find_all('td')) > 0:
                    selection = ""
                    sub_id = ""
                    if reg_page:
                        selection = f'->{reg}'
                        sub_id += f'@[{reg.strip()}]'
                        reg = int(addrs_tables[table][0], 16)
                    else:
                        reg = int(reg, base = 16) + int(addrs_tables[table][0], base = 16)
                    line.insert(append_index, BeautifulSoup(f'''<td class='hex value' id='0x{reg:08X}{sub_id}' width='10%'>0x{reg:08X}''' + selection + '''</td>''', 'html.parser'))
                # Header line
                elif len(line.find_all('th')) > 0:
                    line.insert(append_index, BeautifulSoup(f'''<th width='10%'>Value</th>''', 'html.parser'))
        # Remove original table
        tables[-1].extract()
        return render_template_string(str(soup))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('ug1087-zynq-ultrascale-registers.htm')

@app.route('/values', methods=['POST'])
def value():
    req = request.get_json()
    result = {}
    soc = Comm(hostname=hostname)
    for full_addr in req['values']:
        addr = full_addr
        split = addr.split('@')
        bits = ''
        if len(split) == 2:
            addr = split[0]
            bits = split[1]
        reg = 'DEADBEEF'
        try:
            reg = soc.regrd(int(addr, 16), 0)
        except:
            print("ERROR addr:", full_addr)
        if bits != '':
            reg = getBits(reg, bits[1:len(bits) - 1])
        result[full_addr] = f'0x{reg:08X}'
    #soc.close()
    return json.dumps(result)

@app.route('/target')
def change_target():
    global hostname
    target = request.args.get('hostname')
    status = False
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target):
        hostname = target
    return render_template(f'branding.html'), 200

@app.route('/<name>')
def route(name):
    if re.match('.*\.html', name):
        return genHtml(f'{name}')
    else:
        return render_template(f'{name}')