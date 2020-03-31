def parse_victor70c(data):
    # URL for RS232 port datasheet https://www.ic-fortune.com/upload/Download/FS9922-DMM4-DS-13_EN.pdf
    """
    Parse a data line from a Victor 70C digital multimeter
    The Victor 70C outputs at 2400 BAUD at 1 second intervals,
    each line of data is terminated by a new line
    
    Args: data - byte literal with one line of data
            
    Returns: Dictionary 
    
    NUM - signed number on the display (integer)
    TEXT - full text number plus units (string) 
    RAW_DATA - dictionary with the following data
        RAW - the raw 4 bytes as a byte literal
        SIGN - positive or negative as an integer
        DEC_MOD - the decimal modifier
    """
    global decimal_modifier
    global num
    if data[0] == 43: # ASCII '+'
        sign = 1
    elif data[0] == 45: # ASCII '-'
        sign = -1
    
    if data[6] == 52:  # ASCII '4'
        decimal_modifier = 10
    elif data[6] == 50: # ASCII '2'
        decimal_modifier = 100
    elif data[6] == 49: # ASCII '1'
        decimal_modifier = 1000

    raw_num = data[1:5]
    try:
        num = int(raw_num) * sign / decimal_modifier
    except Exception:
        num = -1 # 0.L
    
    um = unit_modifiers(data[9])
    u = units(data[10])
    # print(f'{um}{u}')
    # print('num:', num)
    
    return {'NUM': num,
            'UNITS': str(um) + str(u),
            'TEXT': f'{str(num)} {um}{u}',
            'RAW_DATA': {
                'SIGN': sign, 
                'NUM': raw_num,
                'DEC_MOD': decimal_modifier
            }
           }

def units(byte):
    unit_types = {
        0x80: 'Volts',
        0x40: 'Amps',
        0x20: 'Ohms',
        0x10: 'hFE',
        0x08: 'Hz',
        0x04: 'Farads',
        0x02: 'Celcius',
        0x01: 'Fahrenheit'
    }
    return unit_types.get(byte, 'Invalid unit type')

def unit_modifiers(byte):
    unit_modifier_types = {
        0x80: 'micro',
        0x40: 'm',
        0x20: 'k',
        0x10: 'M',
        0x08: 'Beep',
        0x04: 'Diode',
        0x02: 'Percent',
        0x01: 'None',
        0x00: ''
    }
    return unit_modifier_types.get(byte, 'Invalid unit modifier type')