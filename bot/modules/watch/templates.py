from config import CONFIG

# NOTIFICATION TABLE - expected input
# ALL DATA SHOULD BE IN STR FORMAT
#
# Horizontal [ver=False] - DEFAULT
# HEADERS = ['HEADER 1', HEADER 2', ...,]
# DATA    = [
#   [R1-C1, R1-C2, ...,]
#   [R2-C1, R2-C2, ...,]
#   [R3-C1, R3-C2, ...,]
#   [R4-C1, R4-C2, ...,]
# ]

# Vertical [ver=True]
# HEADERS = ['HEADER 1', HEADER 2', ...,]
# DATA    = [
#   [R1-C1, R2-C1, ...,]
#   [R1-C2, R2-C2, ...,]
#   [R1-C3, R2-C3, ...,]
#   [R1-C4, R2-C4, ...,]
# ]
def gen_table(headers, data, ver=False, row_sep='|', col_sep='-', padding=4):
    row_map = col_map = None
    if ver:
        row_map = [list(d) for d in zip(*data)]
        col_map = data
    else:
        col_map = [list(d) for d in zip(*data)]
        row_map = data

    
    # Locate the largest item
    col_widths = [max(len(headers[i]), len(max(d, key=len))) for i, d in enumerate(col_map)]

    spacer = col_sep.join([col_sep*(width+padding) for width in col_widths])
    col_break =f'{ col_sep }{ spacer }{ col_sep }\n'    

    table = '```\n'
    table += col_break

    table += row_sep # Header Row
    table += row_sep.join([h.center(col_widths[i] + padding) for i, h in enumerate(headers)])
    table += f'{ row_sep }\n'
    table += col_break
    
    for row in row_map: # Data Rows
        for i, col in enumerate(row):
            table += row_sep
            table += col.center(col_widths[i] + padding)
            if len(table) >= 1800: break # hotfix...this is a terrible fix
        table += f'{ row_sep }\n'
        table += col_break
    table += '```'
    
    return table

def gen_notification_table(data):
    col_1 = ['SYMBOL']
    col_2 = ['BOUND']
    col_3 = ['PRICE']

    for symbol in data.keys():
        for bound in data[symbol]:
            col_1.append(symbol)
            col_2.append(bound['BOUND'])
            col_3.append(bound['PRICE'])

    # add 4 chars to make sure longest string has padding
    col_1_width = len(max(col_1, key=len))+4
    col_2_width = len(max(col_2, key=len))+4
    col_3_width = len(max(col_3, key=len))+4

    notify_table =  f'={ "="*col_1_width }={ "="*col_2_width }={ "="*col_3_width }=\n'
    notify_table += f'|{ "SYMBOL".center(col_1_width) }|{ "BOUND".center(col_2_width) }|{ "PRICE".center(col_3_width) }|\n'
    for symbol in data.keys():
        for bound in data[symbol]:
            notify_table += f'={ "="*col_1_width }={ "="*col_2_width }={ "="*col_3_width }=\n'
            notify_table += f"|{ symbol.center(col_1_width) }|{ bound['BOUND'].center(col_2_width) }|{ bound['PRICE'].center(col_3_width) }|\n"
    notify_table += f'={ "="*col_1_width }={ "="*col_2_width }={ "="*col_3_width }=\n'
    return notify_table

    # EXAMPLE INPUT
    # {
    #     'XRP':[
    #         {
    #             'BOUND': '$1.00',
    #             'PRICE': '$1.07'
    #         },{
    #             'BOUND': '$1.05',
    #             'PRICE': '$1.07'
    #         },
    #     ],
    #     'BTC':[
    #         {
    #             'BOUND': '$60000.00',
    #             'PRICE': '$60025.00'
    #         },
    #     ],
    # }

    # EXAMPLE OUTPUT
    # ================================
    # |  SYMBOL  |  BOUND  |  PRICE  |
    # ================================
    # |   XRP    |   $1.00 |  $1.07  |
    # ================================
    # |   XRP    |   $1.05 |  $1.07  |
    # ================================
    # |   BTX    |  $60000 | $600025 |
    # ================================
