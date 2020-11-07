from tkinter import *
from tkinter.ttk import Combobox
import requests
import json
from tkinter import messagebox

# All Currency ISO-4217 codes
currencies = ('AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT', 'BGN',
              'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTN', 'BWP', 'BYR', 'BZD', 'CAD', 'CDF', 'CHF',
              'CLP', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK', 'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN',
              'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP', 'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD',
              'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS', 'INR', 'IQD', 'IRR', 'ISK', 'JMD', 'JOD', 'JPY', 'KES',
              'KGS', 'KHR', 'KMF', 'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD',
              'MAD', 'MDL', 'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRO', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN',
              'NAD', 'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG',
              'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL', 'SOS',
              'SRD', 'SSP', 'STD', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP', 'TRY', 'TTD', 'TWD', 'TZS',
              'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VEF', 'VND', 'VUV', 'WST', 'XAF', 'XCD', 'XOF', 'XPF', 'YER',
              'ZAR', 'ZMW')


# Functions
def convertCurrency():
    fromCurr = from_currency.get()
    toCurr = to_currency.get()
    if not fromCurr or not toCurr:
        messagebox.showerror('Error', 'Invalid currency.')
        return
    api_request = requests.get\
        (f"https://free.currconv.com/api/v7/convert?q={fromCurr.upper()}_{toCurr.upper()}"
         f"&compact=ultra&apiKey=277a29d591fe5ad48aaa")
    api = json.loads(api_request.content)

    INPUT = ent.get()
    if '$' in INPUT:
        INPUT = INPUT.strip('$')
    if not api:
        messagebox.showerror('Error', 'Invalid currency.')
        return
    if not INPUT or int(INPUT) < 0 or not INPUT.isnumeric():
        messagebox.showerror('Error', 'Invalid amount.')
        return
    rate = api[f'{fromCurr.upper()}_{toCurr.upper()}']
    output['text'] = '$' + str(round(float(rate) * float(INPUT), 2))
    from_currency.event_generate('<FocusOut>')
    to_currency.event_generate('<FocusOut>')


# Function to do Autocomplete search ISO-4217.
def on_keyrelease(event):
    # get text from entry
    value = event.widget.get()
    value = value.strip().lower()

    # get data from test_list
    if value == '':
        data = currencies
    else:
        data = []
        for item in currencies:
            if value in item.lower():
                data.append(item)

    event.widget.config(value=tuple(data))
    event.widget.event_generate('<Down>')


# Creating main window
root = Tk()
root.title('Currency Converter')
root.iconbitmap('coins.ico')

# Adding restriction to resizing of window
root.minsize(width=600, height=200)

# Setting the app height, width and position
app_width = 800
app_height = 200

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f"{app_width}x{app_height}+{int(x)}+{int(y)}")

# Resizing the window will not affect placement of labels
root.rowconfigure([0, 1], minsize=50, weight=1)
root.columnconfigure([i for i in range(4)], minsize=50, weight=1)

# Creating the widgets to use
ent = Entry(root, width=10, font=('Helvetica', 15))
ent.insert(0, '$')
ent.grid(row=0, column=0, rowspan=2, padx=10)
ent.focus()

from_currency_lbl = Label(root, text='Currency ISO-4217', font=('Helvetica', 15, 'bold', 'underline'))
from_currency_lbl.grid(row=0, column=1, sticky='s')

from_currency = Combobox(root, font=('Helvetica', 15, 'bold'), width=5, value=currencies)
from_currency.grid(row=1, column=1, sticky='n', padx=10, pady=10)
from_currency.bind('<KeyRelease>', on_keyrelease)

convert_btn = Button(root, text="\N{RIGHTWARDS ARROW}", command=convertCurrency, width=5)
convert_btn.grid(row=0, column=2, rowspan=2, sticky='ns')

to_currency_lbl = Label(root, text='Currency ISO-4217', font=('Helvetica', 15, 'bold', 'underline'))
to_currency_lbl.grid(row=0, column=3, sticky='s')

to_currency = Combobox(root, font=('Helvetica', 15, 'bold'), width=5, value=currencies)
to_currency.grid(row=1, column=3, sticky='n', padx=10, pady=10)
to_currency.bind('<KeyRelease>', on_keyrelease)

output = Label(root, font=('Helvetica', 15))
output.grid(row=0, column=4, padx=10, rowspan=2)

root.mainloop()
