import tkinter as objTK
from tkinter import ttk as objTTK
from functools import partial
import datetime as objDateTime
from ttkthemes import ThemedTk


class MyTreeview(objTTK.Treeview):
    def heading(self, column, sort_by=None, **kwargs):
        if sort_by and not hasattr(kwargs, 'command'):
            func = getattr(self, f"_sort_by_{sort_by}", None)
            if func:
                kwargs['command'] = partial(func, column, False)
            # End of if
        # End of if
        return super().heading(column, **kwargs)
    # End of heading()

    def _sort(self, column, reverse, data_type, callback):
        l = [(self.set(k, column), k) for k in self.get_children('')]
        l.sort(key=lambda t: data_type(t[0]), reverse=reverse)
        for index, (_, k) in enumerate(l):
            self.move(k, '', index)
        # End of for loop
        self.heading(column, command=partial(callback, column, not reverse))
    # End of _sort()

    def _sort_by_num(self, column, reverse):
        self._sort(column, reverse, int, self._sort_by_num)
    # End of _sort_by_num()

    def _sort_by_name(self, column, reverse):
        self._sort(column, reverse, str, self._sort_by_name)
    # End of _sort_by_num()

    def _sort_by_date(self, column, reverse):
        def _str_to_datetime(string):
            return objDateTime.datetime.strptime(string, "%Y-%m-%d")
        # End of _str_to_datetime()
        
        self._sort(column, reverse, _str_to_datetime, self._sort_by_date)
    # End of _sort_by_num()
    
    def _sort_by_time(self, column, reverse):
        def _str_to_time(string):
            return int(string.replace(":", ""))
        # End of _str_to_datetime()
        
        self._sort(column, reverse, _str_to_time, self._sort_by_time)
        



    def _sort_by_multidecimal(self, column, reverse):
        def _multidecimal_to_str(string):
            arrString = string.split(".")
            strNum = ""
            for iValue in arrString:
                strValue = f"{int(iValue):02}"
                strNum = "".join([strNum, str(strValue)])
            # End of for loop
            strNum = "".join([strNum, "0000000"])
            return int(strNum[:8])
        # End of _multidecimal_to_str()
        
        self._sort(column, reverse, _multidecimal_to_str, self._sort_by_multidecimal)
    # End of _sort_by_num() 

    def _sort_by_numcomma(self, column, reverse):
        def _numcomma_to_num(string):
            return int(string.replace(",", ""))
        # End of _numcomma_to_num()
        
        self._sort(column, reverse, _numcomma_to_num, self._sort_by_numcomma)
    # End of _sort_by_num() 

# End of class MyTreeview

objWindow = objTK.Tk()

objWindow=ThemedTk(theme='scidpink')
print(objWindow.get_themes())

Themed_Btn = objTTK.Button(objWindow,text='Themed button')
Themed_Btn.pack()


objWindow.title('Warehouse Logger V1.0')
arrlbHeader = ["Time" ,"Event Type","Order ID" "Bot Type", "Bot ID","Message"]

treeview = MyTreeview(columns=arrlbHeader, show="headings")


arrRows=[["13:56:56","New Order","ab123","Warehouse","1422412","Done"],["12:16:56","New Order","sdffds123","Sorting","232412","Done"]]

# arrRows = [["Expenses", "Curds milk", "Dairy products", "2.5.2.1", "456", "31", "8", "2021", "2021-08-31", ""],
# ["Expenses", "Aug", "Maid", "2.12.4", "1,000", "31", "8", "2021", "2021-08-31", ""],
# ["Expenses", "Aug", "Water", "2.12.8", "200", "31", "8", "2021", "2021-08-31", "AAA"],
# ["Income", "Aug", "Electricity", "2.12.2", "190", "31", "8", "2021", "2021-08-31", "OMG"],
# ["Expenses", "Aug - garbage collection", "Miscellaneous", "2.12.9", "20", "31", "8", "2021", "2021-08-31", "Test1"],
# ["Expenses", "Bread", "Bakery", "2.5.1.1", "10", "29", "8", "2021", "2021-08-29", ""],
# ["Income", "Veggies", "Vegetables", "2.5.2.7", "21", "28", "8", "2021", "2021-08-28", ""],
# ["Expenses", "Groceries", "Grains", "2.5.2.3", "76", "28", "8", "2021", "2021-08-28", "Test"],
# ["Expenses", "Phenyl", "Toiletries", "2.16", "34", "28", "8", "2021", "2021-08-28", ""]]
arrColWidth = [100,100,100,100,100,100]
arrColAlignment = ["center", "center", "center", "center", "center", "center"]

arrSortType = ["time", "name", "name", "name","num", "name"]

for iCount in range(len(arrlbHeader)):
    strHdr = arrlbHeader[iCount]
    treeview.heading(strHdr, text=strHdr.title(), sort_by=arrSortType[iCount])
    treeview.column(arrlbHeader[iCount], width=arrColWidth[iCount], stretch=True, anchor=arrColAlignment[iCount])
# End of for loop

treeview.pack()

for iCount in range(len(arrRows)):
    treeview.insert("", "end", values=arrRows[iCount])
# End of for loop

objWindow.bind("<Escape>", lambda funcWinSer: objWindow.destroy())

objWindow.mainloop()