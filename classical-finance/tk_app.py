import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar, DateEntry
import tk_ui as ui

root = tk.Tk()
root.title("Finance")
s = ttk.Style(root)
s.theme_use('clam')

start_var = tk.StringVar()
end_var = tk.StringVar()
amount_var = tk.StringVar()

def start_dateentry_view():
    def print_sel(e):
        global start_var
        start_var = cal.get_date()
        print('start_date="{}"'.format(cal.get_date()))
    top = tk.Toplevel(root)

    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    cal.bind("<<DateEntrySelected>>", print_sel)
    ttk.Button(top, text="ok", command=top.destroy).pack()

def end_dateentry_view():
    def print_sel(e):
        global end_var
        end_var = cal.get_date()
        print('end_date="{}"'.format(cal.get_date()))
    top = tk.Toplevel(root)
    ttk.Label(top, text='Choose date').pack(padx=10, pady=10)
    cal = DateEntry(top, width=12, background='darkblue',
                    foreground='white', borderwidth=2)
    cal.pack(padx=10, pady=10)
    cal.bind("<<DateEntrySelected>>", print_sel)
    ttk.Button(top, text="ok", command=top.destroy).pack()

def stocks_entry_view():
    for i in range(10):
        stocks_entry.insert(i, str(i) + " item" )

def submit():
    amount = amount_var.get()
    start_date = start_var.get()
    end_date = end_var.get()
    r = ui.optimal_portfolio(amount)
    print(r)
    top = tk.Toplevel(root)
    result = r[0]['result']
    ttk.Label(top, text="Weights Result", font=('calibre',10, 'bold')).pack()
    for k, v in result.items():
        res = k + ":" + str(v)
        ttk.Label(top, text=res).pack()
    amo = r[1]['amount']
    ttk.Label(top, text="Amount Result", font=('calibre',10, 'bold')).pack()
    for k, v in amo.items():
        amou = k + ":" + str(v)
        ttk.Label(top, text=amou).pack()
    ttk.Button(top, text="ok", command=top.destroy).pack()
    amount_var.set("")
        
start_label = tk.Label(root, text = 'Start Date', font=('calibre',10, 'bold'))
start_entry = ttk.Button(root, text='Date Entry', command=start_dateentry_view)

end_label = tk.Label(root, text = 'End Date', font=('calibre',10, 'bold'))
end_entry = ttk.Button(root, text='Date Entry', command=end_dateentry_view)

#tickers_label = tk.Label(root, text = 'Select Ticker(s)', font=('calibre',10, 'bold'))
#tickers_entry = tk.Listbox(root, selectmode = "multiple") 

amount_label = tk.Label(root, text = 'Enter Amount', font=('calibre',10, 'bold'))
amount_entry = ttk.Entry(root, textvariable = amount_var, font=('calibre', 10, 'normal'))

submit = ttk.Button(root, text='Submit', command=submit)

start_label.grid(row=0, column=1)
start_entry.grid(row=0, column=2)
end_label.grid(row=1, column=1)
end_entry.grid(row=1, column=2)
#tickers_label.grid(row=2, column=1)
#tickers_entry.grid(row=2, column=2)
amount_label.grid(row=3, column=1)
amount_entry.grid(row=3, column=2)
submit.grid(row=4, column=2)
root.mainloop()
