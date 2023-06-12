import pandas as pd

def convert_k_m_to_numeric(value):
    if isinstance(value, str):
        value = value.replace(',', '')
        if 'K' in value:
            return float(value.replace('K', '')) * 1000
        elif 'M' in value:
            return float(value.replace('M', '')) * 1000000
    return float(value)
