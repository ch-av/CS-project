import tkinter as tk
import matplotlib

matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import math
from matplotlib.widgets import Slider, Button  # import Sliders and Buttons
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from tkinter import ttk




######################################################################
############### Input -->  variables for graphic #####################
######################################################################

class budget_line(object):
    def __init__(self, income, price_1, price_2, price_1_new=0):
        self.income = income
        self.price_1 = price_1
        self.price_2 = price_2
        self.price_1_new = price_1_new

    def axes_intersection_initial(self):
        point_y = self.income / self.price_2
        point_x = self.income / self.price_1
        return [0, point_x], [point_y, 0]

    def price_1_new(self):
        return price_1_new

    def axes_intersection_provisional(self, utility_tangent):
        self.income_provisional = self.price_1_new * utility_tangent[0] + self.price_2 * utility_tangent[1]
        point_y = round(self.income_provisional / self.price_2, 7)
        point_x = round(self.income_provisional / price_1_new, 7)
        return [[0, point_y], [point_x, 0]]

    def axes_intersection_final(self):
        point_y = self.income / self.price_2
        point_x = self.income / self.price_1_new
        print([point_x, 0], [0, point_y])
        return [[point_x, 0], [0, point_y]]


class Cobb_Douglas(object):
    def __init__(self, power_x1, power_x2, income, price_1, price_2, coeff):
        self.coeff = coeff
        self.power_x1 = power_x1
        self.power_x2 = power_x2
        self.income = income
        self.price_1 = price_1
        self.price_2 = price_2

    def demand_points(self):
        x1 = (self.power_x1 * self.income) / (self.price_1 * (self.power_x1 + self.power_x2))
        x2 = (self.power_x2 * self.income) / (self.price_2 * (self.power_x1 + self.power_x2))
        return x1, x2

    def ploting(self, utility, var1=1, var2=1):
        pointsX = np.arange(0.1, (self.income / self.price_1), round((self.income / self.price_1) / 50, 5))
        pointsY = []

        for i in pointsX:
            y = round((utility / ((i) ** self.power_x1)) ** (1 / self.power_x2), 5)
            pointsY += [y]

        return pointsX, pointsY

    def calc_utility(self, x1, x2):
        a = x1 ** self.power_x1
        b = x2 ** self.power_x2
        utility = round(a * b, 5)
        return utility


class perfect_complements(object):
    def __init__(self, coeff_1, coeff_2, income, price_1, price_2):
        self.coeff_1 = coeff_1
        self.coeff_2 = coeff_2
        self.income = income
        self.price_1 = price_1
        self.price_2 = price_2

    def demand_points(self):

        x1 = self.income / (self.price_1 + self.coeff_1 * self.price_2 / self.coeff_2)
        x2 = self.income / (self.price_2 + self.coeff_2 * self.price_1 / self.coeff_1)
        return x1, x2

    def calc_utility(self, x1, x2):

        if self.coeff_1 * x1 > self.coeff_2 * x2:
            utility = round(self.coeff_2 * x2, 5)
        else:
            utility = round(self.coeff_1 * x1, 5)
        return utility

    def ploting(self, utility, x1, x2):
        x1 = round(self.income / (self.price_1 + self.coeff_1 * self.price_2 / self.coeff_2), 5)
        x2 = round(self.income / (self.price_2 + self.coeff_2 * self.price_1 / self.coeff_1), 5)

        s = min(self.price_1, self.price_2)
        scale = (self.income / s) * 1.3

        pointsX = [x1 + scale, x1, x1]
        pointsY = [x2, x2, x2 + scale]

        return pointsX, pointsY


class perfect_subs(object):
    def __init__(self, coeff_1, coeff_2, income, price_1, price_2):
        self.coeff_1 = coeff_1
        self.coeff_2 = coeff_2
        self.income = income
        self.price_1 = price_1
        self.price_2 = price_2

    def demand_points(self):
        if self.income / self.price_1 > self.income / self.price_2:
            x1 = self.income / self.price_1
            x2 = 0
        else:
            x1 = 0
            x2 = self.income / self.price_2

        return x1, x2

    def calc_utility(self, x1, x2):

        utility = self.coeff_1 * x1 + self.coeff_2 * x2
        return round(utility, 5)

    def ploting(self, utility, x1, x2):

        pointsX = [utility / self.coeff_1, 0]

        pointsY = [0, utility / self.coeff_2]
        return pointsX, pointsY


class Quazi(
    object):

    def __init__(self, coeff_1, coeff_2, income, price_1, price_2):
        self.coeff_1 = coeff_1
        self.coeff_2 = coeff_2
        self.income = income
        self.price_1 = price_1
        self.price_2 = price_2

    def demand_points(self):
        x1 = (self.coeff_1 * self.price_2) / (self.coeff_2 * self.price_1)
        x2 = self.income / self.price_2 - self.coeff_1 / self.coeff_2

        return x1, x2

    def calc_utility(self, x1, x2):
        utility = self.coeff_1 * np.log(
            x1) + self.coeff_2 * x2
        return utility

    def ploting(self, utility, x1, x2):
        pointsX = np.arange(0.1, (self.income / self.price_1), (self.income / self.price_1) / 50)
        pointsY = []

        for i in pointsX:
            y = (utility - self.coeff_1 * np.log(i)) / self.coeff_2
            #             print(i)
            pointsY += [y]

        return pointsX, pointsY


def plotted(utility_type, income, price_1, price_2, coeff_1=1, coeff_2=1, coeff_cd=1):
    if utility_type == "Cobb-Douglas production function":
        cd = Cobb_Douglas(coeff_1, coeff_2, income, price_1, price_2, coeff_cd)
        return arguments(cd)

    elif utility_type == "Perfect complements utility function":
        pc = perfect_complements(coeff_1, coeff_2, income, price_1, price_2)
        return arguments(pc)

    elif utility_type == "Perfect substitutes utility function":
        ps = perfect_subs(coeff_1, coeff_2, income, price_1, price_2)
        return arguments(ps)

    elif utility_type == "Quasilinear utility function":
        qq = Quazi(coeff_1, coeff_2, income, price_1, price_2)
        return arguments(qq)


def arguments(func):
    tangent = func.demand_points()

    utility = func.calc_utility(tangent[0], tangent[1])

    demand_points = func.demand_points()
    points_graph = func.ploting(utility, tangent[0], tangent[1])

    x = points_graph[0]
    y = points_graph[1]
    #     print("***")
    return x, y, tangent, demand_points


#################################################
#################################################
#################################################


class program(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Start Page", font="Times 20 bold")
        label.pack(pady=10, padx=10)

        labelq = tk.Label(self, text='''
Hello and welcome!
This app can calculate substitution, income, and total effects for a set of two goods.
Please choose your income, prices for goods 1 and 2, new price for good 1, and relevant taxes (optional). Then pick the desired function from the drop donw menu, and chose corresponding coefficient.
Once information is filled, you can have a choice of exploring an animation with explanations, or play with different values using sliders.''', font="Times 12")
        labelq.pack(pady=20, padx=10)

        StartPage.entries = {}

        StartPage.stop = False

        self.ents = self.input_values()

        options = ["Cobb-Douglas production function",
                   "Perfect substitutes utility function",
                   "Perfect complements utility function",
                   "Quasilinear utility function"]

        self.var = tk.StringVar()
        self.var.set(options[0])

        drop = tk.OptionMenu(self, self.var, *options)
        drop.pack(anchor="w", padx=100, pady=5)

        button1 = ttk.Button(self, text="See animation with explanations",
                             command=lambda: [controller.show_frame(PageOne), self.send_uti(),
                                              self.vals_boxes()])  #, lab_vals(),lab_vals1()])
        button1.pack(pady=5)

        button2 = ttk.Button(self, text="Sliders", command=lambda: [controller.show_frame(PageTwo), self.send_uti(),
                                                                    self.vals_boxes()])  #, lab_vals(),lab_vals1()])
        button2.pack(pady=5)

        self.uti = self.send_uti()

        StartPage.entries = self.entries

    def send_uti(self):
        StartPage.uti = self.var.get()
        return StartPage.uti

    def vals_boxes(self):
        self.entries = {}
        for field in self.fields:
            try:
                self.entries[field] = float(self.ents[field].get())
            except Exception:

                self.entries[field] = 0

        StartPage.stop = True

        StartPage.entries = self.entries
        return self.entries


    def input_values(self):

        boxes = ["Income Tax (%):", "Tax on good 1 (%):", "Tax on good 2 (%):"]
        questions = ['Is there an income tax?',
                     'Is there a tax on good 1?',
                     'Is there a tax on good 2?']

        row = tk.Frame(self)
        lbl1 = ttk.Label(row, text=questions[0], anchor='w')
        row.pack(side="top",
                 fill=tk.X,
                 padx=100,
                 pady=5)
        lbl1.pack(side="left")
        self.aChillerVast1 = tk.IntVar()

        def activateCheck1():
            if self.aChillerVast1.get() == 1:  #whenever checked
                self.ents[boxes[0]].config(state='normal')
            elif self.aChillerVast1.get() == 0:  #whenever unchecked
                self.ents[boxes[0]].config(state='disabled')

        self.chk1 = ttk.Checkbutton(row, variable=self.aChillerVast1, command=activateCheck1).pack(side="left",
                                                                                                   padx=10)  #(row = 1, column = 3)    #command is given

        row = tk.Frame(self)
        lbl2 = ttk.Label(row, text=questions[1], anchor='w')
        row.pack(side="top",
                 fill=tk.X,
                 padx=100,
                 pady=5)
        lbl2.pack(side="left")
        self.aChillerVast2 = tk.IntVar()

        def activateCheck2():
            if self.aChillerVast2.get() == 1:  #whenever checked
                self.ents[boxes[1]].config(state='normal')
            elif self.aChillerVast2.get() == 0:  #whenever unchecked
                self.ents[boxes[1]].config(state='disabled')

        self.chk2 = ttk.Checkbutton(row, variable=self.aChillerVast2, command=activateCheck2).pack(side="left",
                                                                                                   padx=10)  #(row = 1, column = 3)    #command is given

        row = tk.Frame(self)
        lbl3 = ttk.Label(row, text=questions[2], anchor='w')
        row.pack(side="top",
                 fill=tk.X,
                 padx=100,
                 pady=5)
        lbl3.pack(side="left")
        self.aChillerVast3 = tk.IntVar()

        def activateCheck3():
            if self.aChillerVast3.get() == 1:  #whenever checked
                self.ents[boxes[2]].config(state='normal')
            elif self.aChillerVast3.get() == 0:  #whenever unchecked
                self.ents[boxes[2]].config(state='disabled')

        self.chk3 = ttk.Checkbutton(row, variable=self.aChillerVast3, command=activateCheck3).pack(side="left",
                                                                                                   padx=10)  #(row = 1, column = 3)    #command is given

        self.fields = ["Income:", "Income Tax (%):", "Price 1:", "Tax on good 1 (%):", "Price 2:", "Tax on good 2 (%):",
                       "New price 1:", "Coefficient for good 1:", "Coefficient for good 2:"]
        self.ents = {}

        for field in self.fields:
            row = tk.Frame(self)

            lab = ttk.Label(row, width=30, text=field, anchor='w')
            ent = ttk.Entry(row)
            ent.insert(0, "0")
            row.pack(side="top",
                     fill=tk.X,
                     padx=120,
                     pady=5)
            lab.pack(side="left")
            ent.pack(side="right",
                     expand=True,
                     fill=tk.X, padx=0)
            self.ents[field] = ent

        self.ents["Income Tax (%):"].config(state='disabled')
        self.ents["Tax on good 1 (%):"].config(state='disabled')
        self.ents["Tax on good 2 (%):"].config(state='disabled')
        return self.ents


class PageOne(StartPage):
    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)
        self.text_box = tk.Frame(self, borderwidth=0, relief="solid")
        self.text_box.configure(background="white")
        self.text_box.pack(side="right", expand=False, fill="both")
        self.list_of_labs = []

        self.sub_expl = False
        self.inc_expl = False

        self.num = 0

        self.utility_type = "Cobb-Douglas production function"
        self.income = 0  #StartPage.income
        self.price_1 = 0
        self.price_2 = 0

        self.price_1_new = 0
        self.coeff_1 = 0
        self.coeff_2 = 0
        self.coeff_ = 0

        self.income_tax = 0
        self.tax_g1 = 0
        self.tax_g2 = 0

        self.runItSub = False
        self.runItInc = False
        self.pause = False
        self.msg_window = False

        self.fig = plt.figure(figsize=(13, 10))
        self.canvas = FigureCanvasTkAgg(self.fig, self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)
        #         self.canvas.get_tk_widget().pack(side = tk.TOP, fill=tk.BOTH, expand = True)

        #         self.ax = self.fig.add_subplot(111, aspect='equal', autoscale_on=False)          ############## I DID NOT ADD SUBPLOTS BUT THE SHIT WORKS WHY??????????
        scale = 100
        self.ax = plt.axes()
        self.ax.axes.set_aspect('equal')

        self.fig.subplots_adjust(left=0.3, bottom=0.1, top=0.9)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ax.grid()
        self.ax.set(xlabel='good 1', ylabel='good 2',
                    title='Demand-price Function')

        #         self.ax.style.use("fivethirtyeight")

        self.axButton_back = plt.axes([0.05, 0.1, 0.15, 0.15])
        self.btn_back = Button(self.axButton_back, "Back")

        def go_back(event):
            self.bd_init.set_data(0, 0)

            self.uni_init.set_data(0, 0)

            self.bd_mid.set_data(0, 0)

            self.uni_mid.set_data(0, 0)

            self.p.set_data(0, 0)

            self.q.set_data(0, 0)

            self.reset_labels_int()
            self.reset_labels()
            print("+++++++++++++++++ StartPage.stop", StartPage.stop)
            StartPage.stop = False
            print("+++++++++++++++++ StartPage.stop", StartPage.stop)
            self.refr.event_source.start()
            controller.show_frame(StartPage)
            if self.msg_window == True:
                stop = self.popup.destroy()
                self.msg_window = False

        self.btn_back.on_clicked(go_back)

        self.axButton_sub = plt.axes([0.05, 0.535, 0.15, 0.15])
        self.btn_sub = Button(self.axButton_sub, "Sub.Effect")

        def Sub_Effect(event):
            self.runAni1()

        self.btn_sub.on_clicked(Sub_Effect)

        self.axButton_tot = plt.axes([0.05, 0.75, 0.15, 0.15])
        self.btn_tot = Button(self.axButton_tot, "Total Effect")

        def tot_Effect(event):
            print("tot_Effect")
            self.runAni2()

        self.btn_tot.on_clicked(tot_Effect)

        self.axButton1 = plt.axes([0.05, 0.312, 0.15, 0.15])
        self.btn1 = Button(self.axButton1, "Reset")

        def reset(event):
            self.reset_it()

        self.btn1.on_clicked(reset)

        self.bd_init, = self.ax.plot(0, 0, label="Initial budget curve")

        self.uni_init, = self.ax.plot(0, 0, label="Initial utility function")

        self.bd_mid, = self.ax.plot(0, 0, label="Provisional budget curve")

        self.uni_mid, = self.ax.plot(0, 0, label="Provisional utility function")

        self.p, = self.ax.plot(0, 0, label="Final budget curve")

        self.q, = self.ax.plot(0, 0, label="Final utility function")

        self.p.set_color("red")
        self.q.set_color("red")

        self.bd_mid.set_color("green")
        self.uni_mid.set_color("green")

        self.bd_init.set_color("blue")
        self.uni_init.set_color("blue")

        self.ents = StartPage.entries

        self.refr = animation.FuncAnimation(self.fig, self.refreshing, frames=10, interval=100, repeat=True)

    def reset_labels_int(self):
        print("))0)")
        try:
            self.label1.pack_forget()
            print("AAAAAAAAAAAAAAAAAAAAAAA")
        except Exception:
            print("BBBBBBBBBBBBBBBBBBBBBBB")
            pass

        try:
            self.label2.pack_forget()
        except Exception:
            pass

        try:
            self.label3.pack_forget()
        except Exception:
            pass

        try:
            self.label4.pack_forget()
        except Exception:
            pass

        try:
            self.label5.pack_forget()
        except Exception:
            pass

        try:
            self.label6.pack_forget()
        except Exception:
            pass

        try:
            self.label7.pack_forget()
        except Exception:
            pass

    def reset_labels(self):
        self.sub_expl = False
        self.incPexpl = False
        try:
            self.label7.pack_forget()
        except Exception:
            pass

        try:
            self.label8.pack_forget()
        except Exception:
            pass

        try:
            self.label9.pack_forget()
        except Exception:
            pass

        try:
            self.label10.pack_forget()
        except Exception:
            pass

        try:
            self.label11.pack_forget()
        except Exception:
            pass

        try:
            self.label12.pack_forget()
        except Exception:
            pass

        try:
            self.label13.pack_forget()
        except Exception:
            pass

        try:
            self.label14.pack_forget()
        except Exception:
            pass

        try:
            self.label15.pack_forget()
        except Exception:
            pass

        try:
            self.label16.pack_forget()
        except Exception:
            pass

    def reset_it(self):

        self.reset_labels()
        self.reset_labels_int()

        self.income = self.income_not_taxed = self.income_not_taxed
        self.price_1 = self.price_1_not_taxed
        self.price_1_new = self.price_1_new_not_taxed
        self.price_2 = self.price_2_not_taxed

        self.bd_init.set_data(0, 0)

        self.uni_init.set_data(0, 0)

        self.bd_mid.set_data(0, 0)

        self.uni_mid.set_data(0, 0)

        self.p.set_data(0, 0)

        self.q.set_data(0, 0)
        self.func()
        print("good to 0################################################")

    def refreshing(self, i):
        var = i
        self.ents = StartPage.entries
        if len(self.ents) > 0:
            if type(self.ents["Income:"]) == float:
                self.income = self.ents["Income:"]
                self.price_1 = self.ents["Price 1:"]
                self.price_2 = self.ents["Price 2:"]
                self.price_1_new = self.ents["New price 1:"]
                self.coeff_1 = self.ents["Coefficient for good 1:"]
                self.coeff_2 = self.ents["Coefficient for good 2:"]
                self.coeff_cd = 1
                self.income_tax = self.ents["Income Tax (%):"]
                self.tax_g1 = self.ents["Tax on good 1 (%):"]
                self.tax_g2 = self.ents["Tax on good 2 (%):"]
                self.utility_type = StartPage.uti


        else:
            self.income = 1  #self.ents["Income:"]
            self.price_1 = 1  #self.ents[:"Price 1:"]
            self.price_2 = 1  #self.ents["Price 2:"]
            self.price_1_new = 1  #self.ents["New pirce 1:"]
            self.utility_type = "Cobb-Douglas production function"
            self.coeff_1 = 1
            self.coeff_2 = 1
            self.coeff_cd = 1
            self.income_tax = 0
            self.tax_g1 = 0
            self.tax_g2 = 0

        if StartPage.stop == True:
            self.refr.event_source.stop()
            print("STOPPED")
            #             print(self.ents)
            self.utility_type = StartPage.uti

            if self.income == 0 or self.price_1 == 0 or self.price_2 == 0 or self.coeff_1 == 0 or self.coeff_2 == 0 or self.coeff_cd == 0 or type(
                    self.price_1_new) != float:
                print(self.income, self.price_1, self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd,
                      type(self.price_1_new))
                self.try_other_vals()
                self.message(""" 
The function supports only integers and floating-point numbers.\n\
The function does not support zero values for income, price1, and price2.\n\
The function does not support same values for price1 and new price1.\n\
Please go back and try other values.""", "Error!")

            else:
                self.func()

    def message(self, message, title):
        self.popup = tk.Tk()
        self.popup.wm_title(title)
        label = ttk.Label(self.popup, text=message, font="Times 12")
        label.pack(side="top", fill="both", anchor="w", expand=True, pady=15, padx=30)
        self.msg_window = True
        B1 = ttk.Button(self.popup, text="Okay!", command=self.popup.destroy)
        B1.pack(side="top", pady=20)

        self.popup.mainloop()

    def try_other_vals(self):
        self.p.set_data(0, 0)

        self.q.set_data(0, 0)

    def func(self):

        self.label1 = tk.Label(self.text_box, text=
        '''

In this model, we have two goods – x and y, with  prices pₓ and pᵧ, respectively.
We also have income m. The budget curve is m = pₓ⋅x + pᵧ⋅y
On the final graph, the initial curves are in blue.''', justify="left", font="Times 12")

        self.label1.configure(background="white")
        #         text_box.pack(side="right", expand=False, fill="both")
        self.label1.pack(padx=5, pady=5, anchor="w")

        self.label3 = tk.Label(self.text_box, text=

        '''You indicated that income tax is %0.2f, tax in good x is %0.2f, and tax on good y is %0.2f. 
Adjusting for taxes and inserting proper values, the budget curve has the form of:''' % (
        self.income_tax, self.tax_g1, self.tax_g2), justify="left", font="Times 12")

        self.label3.configure(background="white")
        #         text_box.pack(side="right", expand=False, fill="both")
        self.label3.pack(padx=5, pady=0, anchor="w")

        self.label4 = tk.Label(self.text_box, text=

        '''
%0.2f ⋅ (1-%0.2f) = (1+%0.2f) ⋅ %0.2f⋅x + (1+%0.2f) ⋅ %0.2f⋅y''' % (
        self.income, self.income_tax / 100, self.tax_g1 / 100, self.price_1, self.tax_g2 / 100, self.price_2),
                               justify="left", font="Times 12 bold")

        self.label4.configure(background="white")
        #         text_box.pack(side="right", expand=False, fill="both")
        self.label4.pack(padx=5, pady=0, anchor="w")

        self.label6 = tk.Label(self.text_box, text=
        '''
When the price of good x changes, the model is affected in two ways: 
    - ∆xˢ – substitution effect, which is defined as the change in demand
        due to the change in the rate of exchange between two goods.
        On the graph, the curves for ∆xˢ are in green      
    - ∆xⁿ – income effect, which is defined as the change in demand
        due to the change in the purchasing power of income.
        On the graph, the curves for ∆xⁿ are the same as for total effect, i.e. red''', justify="left", font="Times 12")

        self.label6.configure(background="white")
        self.label6.pack(padx=5, pady=0, anchor="w")

        self.income_not_taxed = self.income
        self.income = self.income * (100 - self.income_tax) / 100
        self.price_1_not_taxed = self.price_1
        self.price_1 = self.price_1 * (100 + self.tax_g1) / 100
        self.price_1_new_not_taxed = self.price_1_new
        self.price_1_new = self.price_1_new * (100 + self.tax_g1) / 100
        self.price_2_not_taxed = self.price_2
        self.price_2 = self.price_2 * (100 + self.tax_g1) / 100

        self.utility_type = StartPage.uti

        self.line = budget_line(self.income, self.price_1, self.price_2, self.price_1_new)
        self.price_change = self.price_1_new - self.price_1

        coordinates = self.line.axes_intersection_initial()
        self.x = coordinates[0]
        self.y = coordinates[1]

        self.utilityFunction = plotted(self.utility_type, self.income, self.price_1, self.price_2, self.coeff_1,
                                       self.coeff_2, self.coeff_cd)

        self.bd_mid, = self.ax.plot(0, 0)

        self.uni_mid, = self.ax.plot(0, 0)

        self.bd_init.set_data(self.x, self.y)

        self.uni_init.set_data(self.utilityFunction[0], self.utilityFunction[1])
        #
        #
        self.p.set_data(self.x, self.y)

        self.q.set_data(self.utilityFunction[0], self.utilityFunction[1])

        self.thePoint = self.utilityFunction[2]
        self.income_new = self.price_1_new * self.thePoint[0] + self.price_2 * self.thePoint[1]

        self.coor_init = self.utilityFunction[3]

        self.p.set_color("red")
        self.q.set_color("red")

        self.bd_mid.set_color("green")
        self.uni_mid.set_color("green")

        self.bd_init.set_color("blue")
        self.uni_init.set_color("blue")

        s1 = self.income / min(self.price_1, self.price_2)
        s2 = self.income_new / min(self.price_1_new, self.price_2)
        scale = max(s1, s2) * 1.3

        self.ax.set_xlim([0, scale])
        self.ax.set_ylim([0, scale])

    def runAni1(self):

        self.pause = False
        self.bd_mid.set_data(0, 0)

        self.uni_mid.set_data(0, 0)

        self.runItSub = True
        self.runItInc = False
        self.anim = animation.FuncAnimation(self.fig, self.animate, frames=np.arange(0, abs(self.price_change),
                                                                                     round(abs(self.price_change / 50),
                                                                                           7)), interval=10,
                                            repeat=False)
        msg = self.message("Caclulating Sub. effect...", "In progress")

    def runAni2(self):
        print("runAni2")

        self.pause = False

        self.bd_mid.set_data(0, 0)

        self.uni_mid.set_data(0, 0)

        print("RUNIN *** ")
        self.runItSub = True
        self.runItInc = True
        b = np.arange(0.01, abs(self.price_change), round(abs(self.price_change / 50), 7))
        print("b", b)
        self.anim1 = animation.FuncAnimation(self.fig, self.animate, frames=b, interval=10, repeat=False)
        msg = self.message("Caclulating Tot. effect...", "In progress")

        print("***************************************************")

    def stop(self):
        self.anim.event_source.stop()

    def animate(self, i):

        self.reset_labels()

        if self.sub_expl == False:
            self.reset_labels()
            self.sub_expl = True
            if self.price_1 < self.price_1_new:

                self.label7 = tk.Label(self.text_box, text=
                '''
The first step is substitution effect, ∆xˢ = x (pₓ’, m’) - x (pₓ, m), where
            pₓ’ is the new price, and m' is the adjusted income
As the new price is larger, the curve pivots clockwise till the price is at its new level.
Then, substitution effect is''', justify="left", font="Times 12")

                self.label7.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label7.pack(padx=5, pady=0, anchor="w")

            else:

                self.label7 = tk.Label(self.text_box, text=
                '''
The first step is substitution effect, ∆xˢ = x (pₓ’, m’) - x (pₓ, m), where
            pₓ’ is the new price, and m' is the adjusted income
As the new price is smaller, the curve pivots counterclockwise till the price is at its new level.
Then, substitution effect is''', justify="left", font="Times 12")

                self.label7.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label7.pack(padx=5, pady=0, anchor="w")

            self.label8 = tk.Label(self.text_box, text=
            '''
∆xˢ = x(%0.2f, %0.2f) - x(%0.2f, %0.2f)''' % (self.price_1_new, self.income_new, self.price_1, self.income),
                                   justify="left", font="Times 12 bold")

            self.label8.configure(background="white")
            #         text_box.pack(side="right", expand=False, fill="both")
            self.label8.pack(padx=5, pady=0, anchor="w")

        if self.msg_window == True:
            self.msg_window = False
            close = self.popup.destroy()
        #         print(self.runItSub)
        if self.runItSub == False:
            self.stop()

        self.num += 1
        #         print("anim", self.num)
        self.income_change = abs((self.income_new - self.income) / self.price_change)

        if self.price_change > 0 and self.runItSub == True:
            self.line = budget_line(self.income + i * self.income_change, self.price_1 + i, self.price_2,
                                    self.price_1_new)

            self.utilityFunction = plotted(self.utility_type, self.income + i * self.income_change, self.price_1 + i,
                                           self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd)
        elif self.price_change <= 0 and self.runItSub == True:
            self.line = budget_line(self.income - i * self.income_change, self.price_1 - i, self.price_2,
                                    self.price_1_new)

            self.utilityFunction = plotted(self.utility_type, self.income - i * self.income_change, self.price_1 - i,
                                           self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd)

        #         print(income_new)
        coordinates = self.line.axes_intersection_initial()
        self.x = coordinates[0]
        self.y = coordinates[1]

        if self.runItSub == True:
            self.p.set_data(self.x, self.y)

            self.q.set_data(self.utilityFunction[0], self.utilityFunction[1])

        print(0.01 + i, "---", self.price_change, "---", self.price_change / 50)
        if math.isclose(0.01 + i, abs(self.price_change), abs_tol=round(abs(self.price_change / 50), 7)):
            print("%%%%%%%%%%%%%%%%%%%%%%%")
            print(self.runItInc)
            self.coor_sub = self.utilityFunction[3]
            self.runItSub = False
            if self.runItInc == True:
                self.bd_mid.set_data(self.x, self.y)

                self.uni_mid.set_data(self.utilityFunction[0], self.utilityFunction[1])

                self.anim1 = animation.FuncAnimation(self.fig, self.animate1,
                                                     frames=np.arange(0, abs(self.price_change),
                                                                      round(abs(self.price_change / 50), 7)),
                                                     interval=10, repeat=False)

    def animate1(self, i):

        if self.inc_expl == False:
            self.inc_expl = True

            if self.price_1 < self.price_1_new:

                self.label9 = tk.Label(self.text_box, text=
                '''
The second step is the income effect, ∆xⁿ = x(pₓ’, m) - x(pₓ, m’).
As the new price is larger, the adjusted income was higher than original.
It means that the budget line shifts inwards. Then, the income effect is:''', justify="left", font="Times 12")

                self.label9.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label9.pack(padx=5, pady=0, anchor="w")


            else:

                self.label9 = tk.Label(self.text_box, text=
                '''
The second step is the income effect, ∆xⁿ = x(pₓ’, m) - x(pₓ, m’).
As the new price is smaller, the adjusted income was lower than original.
It means that the budget line shifts outwards. Then, the income effect is:''', justify="left", font="Times 12")

                self.label9.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label9.pack(padx=5, pady=0, anchor="w")

            self.label10 = tk.Label(self.text_box, text=
            '''
∆xⁿ = x (%0.2f, %0.2f) - x (%0.2f, %0.2f)''' % (self.price_1_new, self.income, self.price_1, self.income_new),
                                    justify="left", font="Times 12 bold")

            self.label10.configure(background="white")
            #         text_box.pack(side="right", expand=False, fill="both")
            self.label10.pack(padx=5, pady=0, anchor="w")

        if self.price_change > 0:
            self.line = budget_line(self.income_new - i * self.income_change, self.price_1_new, self.price_2,
                                    self.price_1_new)

            self.utilityFunction = plotted(self.utility_type, self.income_new - i * self.income_change,
                                           self.price_1_new, self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd)

        else:
            self.line = budget_line(self.income_new + i * self.income_change, self.price_1_new, self.price_2,
                                    self.price_1_new)

            self.utilityFunction = plotted(self.utility_type, self.income_new + i * self.income_change,
                                           self.price_1_new, self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd)

        coordinates = self.line.axes_intersection_initial()
        self.x = coordinates[0]
        self.y = coordinates[1]

        self.p.set_data(self.x, self.y)

        self.q.set_data(self.utilityFunction[0], self.utilityFunction[1])
        self.count = 0
        if math.isclose(0.01 + i, abs(self.price_change), abs_tol=round(abs(self.price_change / 50), 7)):
            self.runItInc = False
            self.count = +1
            if self.count == 1:
                self.coor_fin = self.utilityFunction[3]
                res = self.results()

    def results(self):
        self.inc_expl = False
        self.sub_expl = False

        count = 0
        if self.count == 1 and self.pause == False:
            print("substitution effect is...", self.coor_sub[0] - self.coor_init[0])
            print("income effect is...", self.coor_fin[0] - self.coor_sub[0])
            print("total effect is...", self.coor_fin[0] - self.coor_init[0])

            self.pause = True

            self.label11 = tk.Label(self.text_box, text=
            '''
Calculating total effect: ∆x = ∆xˢ + ∆xⁿ
Using the results of the previous steps and demand equations, we know that:
    - ∆xˢ = %0.2f
    - ∆xⁿ = %0.2f
Then, the total effect is:''' % (self.coor_sub[0] - self.coor_init[0], self.coor_fin[0] - self.coor_sub[0]),
                                    justify="left", font="Times 12")

            self.label11.configure(background="white")
            #         text_box.pack(side="right", expand=False, fill="both")
            self.label11.pack(padx=5, pady=0, anchor="w")

            self.label12 = tk.Label(self.text_box, text=
            '''
∆x = (%0.2f) + (%0.2f) = %0.2f''' % (self.coor_sub[0] - self.coor_init[0], self.coor_fin[0] - self.coor_sub[0],
                                     self.coor_fin[0] - self.coor_init[0]), justify="left", font="Times 12 bold")

            self.label12.configure(background="white")
            #         text_box.pack(side="right", expand=False, fill="both")
            self.label12.pack(padx=5, pady=0, anchor="w")

            if (self.coor_fin[0] - self.coor_init[0]) > 0:

                self.label13 = tk.Label(self.text_box, text=
                '''
The total effect (and the change in demand) is positive''', justify="left", font="Times 12")

                self.label13.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label13.pack(padx=5, pady=0, anchor="w")

            else:

                self.label13 = tk.Label(self.text_box, text=
                '''
The total effect (and the change in demand) is negative.''', justify="left", font="Times 12")

                self.label13.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label13.pack(padx=5, pady=0, anchor="w")

            sub_pos = (self.coor_sub[0] - self.coor_init[0]) > 0

            inc_pos = (self.coor_fin[0] - self.coor_sub[0]) > 0

            if sub_pos and inc_pos:

                self.label14 = tk.Label(self.text_box, text=
                '''Both, ∆xˢ and ∆xⁿ are positive and work in the same direction.
It means that good x is a normal good.''', justify="left", font="Times 12")

                self.label14.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label14.pack(padx=5, pady=0, anchor="w")

            elif sub_pos == False and inc_pos == False:

                self.label14 = tk.Label(self.text_box, text=
                '''Both, ∆xˢ and ∆xⁿ are negative and work in the same direction.
It means that good x is a normal good.''', justify="left", font="Times 12")

                self.label14.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label14.pack(padx=5, pady=0, anchor="w")

            else:

                self.label14 = tk.Label(self.text_box, text=
                '''∆xˢ and ∆xⁿ work in different directions.
It means that the good x is an inferior good.''', justify="left", font="Times 12")

                self.label14.configure(background="white")
                #         text_box.pack(side="right", expand=False, fill="both")
                self.label14.pack(padx=5, pady=0, anchor="w")


class PageTwo(StartPage):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.text_box = tk.Frame(self, borderwidth=0, relief="solid")
        self.text_box.configure(background="white")
        self.text_box.pack(side="right", expand=False, fill="both")
        self.list_of_labs = []
        self.income = 0

        self.label1 = tk.Label(self.text_box, text=
        '''



In this model, we have two goods – x and y, with respective prices pₓ and pᵧ.          
We also have an income m. Them, the budget curve is m = pₓ⋅x + pᵧ⋅y.
See the blue curve to find initial position.

When the price of good x changes, there are two sorts of effects: 
    - ∆xˢ – substitution effect, which is the defined as the change in demand
        due to the change in the rate of exchange between the two goods.
        See the green curves for ∆xˢ
    - ∆xⁿ – income effect, which is defined as the change in demand
        due to the change in the purchasing power of an income.
        See the red curve for ∆xⁿ and total effects.

The frist step is substitution effect, ∆xˢ = x (pₓ’, m’) - x (pₓ, m), where
                pₓ’ is the new price, and m' is the adjusted income
                             
The second step is the income effect, ∆xⁿ = x(pₓ’, m) - x(pₓ, m’).

The Total Effect is ∆x = ∆xˢ + ∆xⁿ
''', justify="left", font="Times 12")

        self.label1.configure(background="white")
        #         text_box.pack(side="right", expand=False, fill="both")
        self.label1.pack(padx=5, pady=5, anchor="w")

        self.utility_type = "Cobb-Douglas production function"
        self.income = 0  #StartPage.income
        self.price_1 = 0
        self.price_2 = 0

        self.price_1_new = 0
        self.coeff_1 = 0
        self.coeff_2 = 0
        self.coeff_cd = 0

        self.income_tax = 0
        self.tax_g1 = 0
        self.tax_g2 = 0

        self.msg_window = False

        self.fig1 = plt.figure(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.fig1, self)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True)

        self.ax = plt.axes()  # which one should i keep? seems like this one is more respinsive
        #         plt.axes().set_aspect('equal', 'datalim')
        self.ax.axes.set_aspect('equal')

        self.fig1.subplots_adjust(left=0.05, bottom=0.3, top=0.9, right=0.95)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.ax.grid()
        self.ax.set(xlabel='good 1', ylabel='good 2',
                    title='Demand-price function')

        self.axButton_back = plt.axes([0.05, 0.45, 0.1, 0.1])
        self.btn_back = Button(self.axButton_back, "Back")

        def go_back(event):
            self.label1.pack_forget()

            self.bd_init.set_data(0, 0)

            self.uni_init.set_data(0, 0)

            self.bd_mid.set_data(0, 0)

            self.uni_mid.set_data(0, 0)

            self.p.set_data(0, 0)

            self.q.set_data(0, 0)
            print("+++++++++++++++++ StartPage.stop", StartPage.stop)
            StartPage.stop = False
            print("+++++++++++++++++ StartPage.stop", StartPage.stop)
            self.refr.event_source.start()
            controller.show_frame(StartPage)
            if self.msg_window == True:
                stop = self.popup.destroy()
                self.msg_window = False

        self.btn_back.on_clicked(go_back)

        def reset(event):
            self.p1_slider.reset()
            self.p2_slider.reset()
            self.p1n_slider.reset()
            self.a_slider.reset()

        self.axButton1 = plt.axes([0.05, 0.65, 0.1, 0.1])
        self.btn1 = Button(self.axButton1, "Reset")
        self.btn1.on_clicked(reset)

        self.bd_init, = self.ax.plot(0, 0)

        self.uni_init, = self.ax.plot(0, 0)

        self.bd_mid, = self.ax.plot(0, 0)

        self.uni_mid, = self.ax.plot(0, 0)

        self.p, = self.ax.plot(0, 0)

        self.q, = self.ax.plot(0, 0)

        self.p.set_color("red")
        self.q.set_color("red")

        self.bd_mid.set_color("green")
        self.uni_mid.set_color("green")

        self.bd_init.set_color("blue")
        self.uni_init.set_color("blue")

        self.ents = StartPage.entries
        #

        self.refr = animation.FuncAnimation(self.fig1, self.refreshing, frames=10, interval=100, repeat=True)

    #         self.fig1.subplots_adjust(left=0.05, bottom=0.3)

    def refreshing(self, i):
        var = i

        self.ents = StartPage.entries
        if len(self.ents) > 0:
            if type(self.ents["Income:"]) == float:
                self.income = self.ents["Income:"]
                self.price_1 = self.ents["Price 1:"]
                self.price_2 = self.ents["Price 2:"]
                self.price_1_new = self.ents["New price 1:"]
                self.coeff_1 = self.ents["Coefficient for good 1:"]
                self.coeff_2 = self.ents["Coefficient for good 2:"]
                self.coeff_cd = 1
                self.income_tax = self.ents["Income Tax (%):"]
                self.tax_g1 = self.ents["Tax on good 1 (%):"]
                self.tax_g2 = self.ents["Tax on good 2 (%):"]
                self.utility_type = StartPage.uti


        else:
            self.income = 1  #self.ents["Income:"]
            self.price_1 = 1  #self.ents[:"Price 1:"]
            self.price_2 = 1  #self.ents["Price 2:"]
            self.price_1_new = 1  #self.ents["New pirce 1:"]
            self.utility_type = "Cobb-Douglas production function"
            self.coeff_1 = 1
            self.coeff_2 = 1
            self.coeff_cd = 1
            self.income_tax = 0
            self.tax_g1 = 0
            self.tax_g2 = 0

        if StartPage.stop == True:
            self.refr.event_source.stop()
            print("STOPPED")
            #             print(self.ents)
            self.utility_type = StartPage.uti

            if self.income == 0 or self.price_1 == 0 or self.price_2 == 0 or self.coeff_1 == 0 or self.coeff_2 == 0 or self.coeff_cd == 0 or type(
                    self.price_1_new) != float or self.price_1 == self.price_1_new:
                print(self.income, self.price_1, self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd,
                      type(self.price_1_new))
                self.try_other_vals()
                self.message(
                    """ 
The function supports only integers and floating-point numbers.\n\
The function does not support zero values for income, price1, and price2.\n\
The function does not support same values for price1 and new price1.\n\
Please go back and try other values.""", "Error!")

            else:
                print("go page 2")

                self.income_not_taxed = self.income
                self.income = self.income * (100 - self.income_tax) / 100
                self.price_1_not_taxed = self.price_1
                self.price_1 = self.price_1 * (100 + self.tax_g1) / 100
                self.price_1_new_not_taxed = self.price_1_new
                self.price_1_new = self.price_1_new * (100 + self.tax_g1) / 100
                self.price_2_not_taxed = self.price_2
                self.price_2 = self.price_2 * (100 + self.tax_g1) / 100

                self.func()

    def message(self, message, title):  # https://pythonprogramming.net/tkinter-popup-message-window/
        self.popup = tk.Tk()
        self.popup.wm_title(title)
        label = ttk.Label(self.popup, text=message, font="Times 12")
        label.pack(side="top", fill="both", anchor="w", expand=True, pady=15, padx=30)
        self.msg_window = True
        B1 = ttk.Button(self.popup, text="Okay!", command=self.popup.destroy)
        B1.pack(side="top", pady=20)

        self.popup.mainloop()

    def try_other_vals(self):
        self.p.set_data(0, 0)

        self.q.set_data(0, 0)

    def func(self):

        self.utility_type = StartPage.uti

        self.line = budget_line(self.income, self.price_1, self.price_2, self.price_1_new)
        self.price_change = self.price_1_new - self.price_1

        coordinates = self.line.axes_intersection_initial()
        self.x = coordinates[0]
        self.y = coordinates[1]

        self.utilityFunction = plotted(self.utility_type, self.income, self.price_1, self.price_2, self.coeff_1,
                                       self.coeff_2, self.coeff_cd)

        #
        self.p, = self.ax.plot(self.x, self.y)

        self.q, = self.ax.plot(self.utilityFunction[0], self.utilityFunction[1])

        self.thePoint = self.utilityFunction[2]
        self.income_new = self.price_1_new * self.thePoint[0] + self.price_2 * self.thePoint[1]

        self.income_change = abs((self.income_new - self.income) / self.price_change)

        self.line_mid = budget_line(self.income + self.price_change * self.income_change,
                                    self.price_1 + self.price_change, self.price_2, self.price_1_new)

        self.utilityFunction_mid = plotted(self.utility_type, self.income + self.price_change * self.income_change,
                                           self.price_1 + self.price_change, self.price_2, self.coeff_1, self.coeff_2,
                                           self.coeff_cd)

        coordinates_mid = self.line_mid.axes_intersection_initial()
        self.x_mid = coordinates_mid[0]
        self.y_mid = coordinates_mid[1]

        self.p_mid, = self.ax.plot(self.x_mid, self.y_mid)

        self.q_mid, = self.ax.plot(self.utilityFunction_mid[0], self.utilityFunction_mid[1])

        self.line_fin = budget_line(self.income, self.price_1 + self.price_change, self.price_2, self.price_1_new)

        self.utilityFunction_fin = plotted(self.utility_type, self.income, self.price_1 + self.price_change,
                                           self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd)

        coordinates_fin = self.line_fin.axes_intersection_initial()
        self.x_fin = coordinates_fin[0]
        self.y_fin = coordinates_fin[1]

        self.p_fin, = self.ax.plot(self.x_fin, self.y_fin)

        self.q_fin, = self.ax.plot(self.utilityFunction_fin[0], self.utilityFunction_fin[1])

        s1 = self.income / min(self.price_1, self.price_2)
        s2 = self.income_new / min(self.price_1_new, self.price_2)
        scale = max(s1, s2) * 1.3

        self.ax.set_xlim([0, scale])
        self.ax.set_ylim([0, scale])

        self.coor_init = self.utilityFunction[3]

        self.p_fin.set_color("red")
        self.q_fin.set_color("red")

        self.p_mid.set_color("green")
        self.q_mid.set_color("green")

        self.p.set_color("blue")
        self.q.set_color("blue")

        self.slider_ax = plt.axes([0.2, 0.05, 0.6, 0.025])
        self.a_slider = Slider(self.slider_ax,  # the axes object containing the slider
                               'income',  # the name of the slider parameter
                               0.01,  # minimal value of the parameter
                               3 * self.income,  # maximal value of the parameter
                               self.income,  # initial value of the parameter
                               closedmin=True, closedmax=True)
        self.a_slider.on_changed(self.update_income)

        self.slider_ax1 = plt.axes([0.2, 0.1, 0.6, 0.025])
        self.p1_slider = Slider(self.slider_ax1,  # the axes object containing the slider
                                'price 1',  # the name of the slider parameter
                                0.01,  # minimal value of the parameter
                                3 * self.price_1,  # maximal value of the parameter
                                self.price_1,  # initial value of the parameter
                                closedmin=True, closedmax=True)
        self.p1_slider.on_changed(self.update_income)

        self.slider_ax2 = plt.axes([0.2, 0.15, 0.6, 0.025])
        self.p2_slider = Slider(self.slider_ax2,  # the axes object containing the slider
                                'price 2',  # the name of the slider parameter
                                0.01,  # minimal value of the parameter
                                3 * self.price_2,  # maximal value of the parameter
                                self.price_2,  # initial value of the parameter
                                closedmin=True, closedmax=True)
        self.p2_slider.on_changed(self.update_income)

        self.slider_ax3 = plt.axes([0.2, 0.2, 0.6, 0.025])
        self.p1n_slider = Slider(self.slider_ax3,  # the axes object containing the slider
                                 'price 1 new',  # the name of the slider parameter
                                 0.01,  # minimal value of the parameter
                                 3 * self.price_1_new,  # maximal value of the parameter
                                 self.price_1_new,  # initial value of the parameter
                                 closedmin=True, closedmax=True)
        self.p1n_slider.on_changed(self.update_income)

    def update_income(self, val):

        self.update_idletasks()

        self.price_1 = self.p1_slider.val
        self.price_2 = self.p2_slider.val
        self.income = self.a_slider.val
        self.price_1_new = self.p1n_slider.val
        self.price_change = self.price_1_new - self.price_1
        self.thePoint = self.utilityFunction[2]
        self.income_new = self.price_1_new * self.thePoint[0] + self.price_2 * self.thePoint[1]

        self.income_change = abs((self.income_new - self.income) / self.price_change)

        self.line = budget_line(self.income, self.price_1, self.price_2, self.price_1_new)
        coordinates = self.line.axes_intersection_initial()

        self.line_mid = budget_line(self.income + self.price_change * self.income_change,
                                    self.price_1 + self.price_change, self.price_2, self.price_1_new)

        self.utilityFunction_mid = plotted(self.utility_type, self.income + self.price_change * self.income_change,
                                           self.price_1 + self.price_change, self.price_2, self.coeff_1, self.coeff_2,
                                           self.coeff_cd)

        coordinates_mid = self.line_mid.axes_intersection_initial()
        self.x_mid = coordinates_mid[0]
        self.y_mid = coordinates_mid[1]

        self.p_mid.set_data(self.x_mid, self.y_mid)

        self.q_mid.set_data(self.utilityFunction_mid[0], self.utilityFunction_mid[1])

        self.x = coordinates[0]
        self.y = coordinates[1]
        self.utilityFunction = plotted(self.utility_type, self.income, self.price_1, self.price_2, self.coeff_1,
                                       self.coeff_2, self.coeff_cd)
        self.q.set_data(self.utilityFunction[0], self.utilityFunction[1])
        self.p.set_data(self.x, self.y)

        self.line_fin = budget_line(self.income, self.price_1 + self.price_change, self.price_2, self.price_1_new)

        self.utilityFunction_fin = plotted(self.utility_type, self.income, self.price_1 + self.price_change,
                                           self.price_2, self.coeff_1, self.coeff_2, self.coeff_cd)

        coordinates_fin = self.line_fin.axes_intersection_initial()
        self.x_fin = coordinates_fin[0]
        self.y_fin = coordinates_fin[1]

        self.p_fin.set_data(self.x_fin, self.y_fin)

        self.q_fin.set_data(self.utilityFunction_fin[0], self.utilityFunction_fin[1])

        s1 = self.income / min(self.price_1, self.price_2)
        s2 = self.income_new / min(self.price_1_new, self.price_2)
        scale = max(s1, s2) * 1.3

        self.ax.set_xlim([0, scale])
        self.ax.set_ylim([0, scale])


app = program()
app.mainloop()
