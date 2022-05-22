from flask import Flask, render_template, render_template_string
from BeautifulSoup import BeautifulSoup, Tag


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
        table = soup.find_all('table')
        table_index = 0
        if len(table) > 1:
            table_index = 1
        lines = table[table_index].find_all('tr')

        for line in lines:
            append_index = 3
            for col in line:
                #print('col=', col)
                if col == '\n':
                    append_index += 1
            if len(line.find_all('td')) > 0:
                #print('found td', line)
                line.insert(append_index, BeautifulSoup(f'''<td>{0}</td>''', 'html.parser'))
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