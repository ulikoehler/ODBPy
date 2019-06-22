# https://techoverflow.net/2018/01/23/converting-namedtuples-to-xlsx-in-python/
import xlsxwriter
import itertools
from collections import namedtuple

def xlsx_write_rows(filename, rows):
    """
    Write XLSX rows from an iterable of rows.
    Each row must be an iterable of writeable values.
    Returns the number of rows written
    """
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet()
    # Write values
    nrows = 0
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            worksheet.write(i, j, val)
        nrows += 1
    # Cleanup
    workbook.close()
    return nrows

def namedtuples_to_xlsx(filename, values):
    """
    Convert a list or generator of namedtuples to an XLSX file.
    Returns the number of rows written.
    """
    try:
        # Ensure its a generator (next() not allowed on lists)
        values = (v for v in values)
        # Use first row to generate header
        peek = next(values)
        header = list(peek.__class__._fields)
        return xlsx_write_rows(filename, itertools.chain([header], [peek], values))
    except StopIteration:  # Empty generator
        # Write empty xlsx
        return xlsx_write_rows(filename, [])
