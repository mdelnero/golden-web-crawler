from crawler.webpage import *
from misc.util import *
from bs4 import BeautifulSoup
from misc.util import *
import re

def trim_lines(text):
    lines = text.splitlines()
    trimmed_lines = [line.strip() for line in lines]
    result = '\n'.join(trimmed_lines)
    return result

def remove_excessive_newlines(input_string):
    pattern = r'\n{3,}'
    cleaned_string = re.sub(pattern, '\n\n', input_string)
    return cleaned_string.strip('\n')

def remove_excessive_spaces(input_string):
    return re.sub(r' +', ' ', input_string)

def remove_excessive_periods(input_string):
    return re.sub(r'\.+', '.', input_string)

def prepare_text(input_string):
    res = input_string
    res = remove_excessive_periods(res)
    res = remove_excessive_spaces(res)
    res = trim_lines(res)
    res = remove_excessive_newlines(res)
    return res

def prepare_line(input_string):
    res = input_string
    res = remove_excessive_periods(res)
    res = remove_excessive_spaces(res)
    res = remove_excessive_newlines(res)
    return res