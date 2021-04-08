from config import CONFIG

# NOTIFICATION TABLE

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
