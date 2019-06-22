# ODBPy
ODB++ support for Python

While most "raw" parsing works, this project is still Alpha.
If you want to help, please drop me a line!

## Example: Extracting XLSX BOM from ODB++ directory

```sh
./ParseODBComponents.py ~/my-odbpp-directory
```
This will save a basic BOM in BOM.xlsx (or use `-o` CLI option for a custom output filename).

Tested with DIPTrace 3.x and ODB++ 8.1.