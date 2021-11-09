from pathlib import Path
from tkinter import Scrollbar, ttk as objTTK
from functools import partial
import datetime as objDateTime
# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, PhotoImage,Frame
from tkinter.constants import RIGHT


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

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
def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

def on_configure(event):
    # update scrollregion after starting 'mainloop'
    # when all widgets are in canvas
    canvas.configure(scrollregion=canvas.bbox('all'))

window = Tk()

window.geometry("1287x851")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 851,
    width = 1287,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    643.0,
    80.0,
    image=image_image_1
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    650.0,
    200.0,
    image=entry_image_1
)

window.title('Warehouse Logger V1.0')
window.resizable(width=1,height=1)

arrlbHeader = ["Time" ,"Event Type","Order ID", "Bot Type", "Bot ID","Message"]



scrollbar = Scrollbar(window, command=canvas.yview)
scrollbar.pack(side='left', fill='y')
canvas.configure(yscrollcommand = scrollbar.set)
canvas.bind('<Configure>', on_configure)


frame = Frame(canvas)
canvas.create_window((100,250), window=frame, anchor='nw')
treeview = MyTreeview(frame,columns=arrlbHeader, show="headings",selectmode='browse')
# verticalbar=Scrollbar(window,orient='vertical',command=treeview.yview)
# verticalbar.pack(side='right',fill='y')

# treeview.config(xscrollcommand=verticalbar.set)
# verticalbar.config(command=treeview.yview)

lst=["13:56:56","New Order","ab123","Warehouse","1422412",'Done']
arrRows=[["13:56:56","New Order","ab123","Warehouse","1422412","Done"],["12:16:56","New Order","sdffds123","Sorting","232412","Done"]]
for i in range(100):
    new_list=lst.copy()
    new_list[-1]+=str(i)
    arrRows.append(new_list)

arrColAlignment = ["center", "center", "center", "center", "center", "center"]

arrSortType = ["time", "name", "name", "name","num", "name"]
arrColWidth = [150,150,150,150,150,400]
for iCount in range(len(arrlbHeader)):
    strHdr = arrlbHeader[iCount]
    treeview.heading(strHdr, text=strHdr.title(), sort_by=arrSortType[iCount])
    treeview.column(arrlbHeader[iCount], width=arrColWidth[iCount], stretch=True, anchor=arrColAlignment[iCount])
treeview.configure(height=100)
treeview.pack()
# treeview.place(x=50,y=250,relheight=80)
# treeview.pack(side='right')

for iCount in range(len(arrRows)):
    treeview.insert("", "end", values=arrRows[iCount])

window.bind("<Escape>", lambda funcWinSer: window.destroy())

window.resizable(False, False)
window.mainloop()
