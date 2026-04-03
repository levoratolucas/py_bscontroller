from datetime import datetime

def validar_data(data_str):
    """Valida se a data está no formato YYYY-MM-DD HH:MM:SS"""
    try:
        datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return True
    except ValueError:
        return False

def formatar_data_para_exibicao(data_str):
    """Formata a data para exibição"""
    try:
        dt = datetime.strptime(data_str, "%Y-%m-%d %H:%M:%S")
        return dt.strftime("%d/%m/%Y %H:%M:%S")
    except:
        return data_str