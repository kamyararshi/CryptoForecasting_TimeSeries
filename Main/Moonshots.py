import tkinter as tk
from tkinter.font import BOLD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib import style
import numpy as np
import os
import sys

import forecaster


def moonshots():
    root = tk.Tk()
    root.title("Moonshots")
    root.iconbitmap("python.ico")
    root.geometry("1400x750")


    """ Top """
    tk.Label(root, text="In Bitcoin We Trust!", font=("Helvetica",18, BOLD), width=30).grid(row=0, column=0, columnspan=2)
    var_main = tk.IntVar()
    '''
    c_main = tk.Checkbutton(
        root, text="check this I dare u!",
        variable=var_main, onvalue="on",
        offvalue="off").grid(row=0, column=1, columnspan=2)
    '''
    """ End Top """
    
    #LARGE_FONT=
    style.use("ggplot")

    #Set path directories for data and model
    main_pth = os.path.dirname(os.path.realpath(sys.argv[0]))
    pth = os.path.join(main_pth, "Data\BINANCE_BTCUSDT, 1D.csv")
    pthm = os.path.join(main_pth, "Data\Multivariate_LSTM_4out_diff_stdscale.h5")
            

################### FRAME1 ###################
    """ FRAME 1"""
    frame_1 = tk.LabelFrame(root, text="This is my Frame", padx=10, pady=10)
    frame_1.grid(row=1, column=1, padx=5, pady=5)


    def show_plot():

        global fig
        global axs
        global ani

        fig, axs = plt.subplots(2, 2, sharex=True, sharey=True, figsize=(10,5))


        def animate(i):
            print(os.path.dirname(os.path.realpath(sys.argv[0])))
            
            # Get the dataframe and prepared data
            X, scaler, pullData = forecaster.prepare_data(pth)
            # Predict using the prepared data
            predictions = forecaster.forecast(X, scaler, pthm)
            # Plot the price and predictions
            axs[0,0].clear(); axs[0,1].clear(); axs[1,0].clear(); axs[1,1].clear()
            pullData.iloc[60:].plot('time', 'close', ax=axs[0,0])
            axs[0,0].plot(predictions[:,-1], label="Predictions")
            axs[0,0].legend()

            pullData.iloc[60:].plot('time', 'open', ax=axs[0,1])
            axs[0,1].plot(predictions[:,0], label="Predictions")
            axs[0,1].legend()
            pullData.iloc[60:].plot('time', 'high', ax=axs[1,0])
            axs[1,0].plot(predictions[:,1], label="Predictions")
            axs[1,0].legend()

            pullData.iloc[60:].plot('time', 'low', ax=axs[1,1])
            axs[1,1].plot(predictions[:,3], label="Predictions")
            axs[1,1].legend()

            #Rotate
            for ax in fig.axes:
                plt.sca(ax)
                plt.xticks(rotation=90)
            
            axs[0,0].set_ylabel("Price USD")
            axs[1,0].set_ylabel("Price USD")
            plt.subplots_adjust(bottom=0.29)
            

        canvas = FigureCanvasTkAgg(fig, master=frame_1)
        # pack_toolbar=False will make it easier to use a layout manager later on.
        toolbar = NavigationToolbar2Tk(canvas, frame_1)
        toolbar.update()
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


        ani = FuncAnimation(fig, animate, interval=15500)
    show_plot()
    """ End FRAME 1"""



################### FRAME2 ###################
    """ FRAME 2"""
    frame_2 = tk.LabelFrame(root, text="Options", padx=20, pady=220)
    frame_2.grid(row=1, column=0, padx=5, pady=5)

    lbl_info = tk.Label(
        frame_2, text="You can do a bunch of stuff from here",
        anchor=tk.N,
        font=("Playfair", 12, BOLD)
        ).grid(row=0, column=0, columnspan=2, pady=5)
    
    lbl_btn = tk.Label(frame_2, text="Initial Capita").grid(row=1, column=0)
    inp_capita = tk.Entry(frame_2, width=20)
    inp_capita.grid(row=1, column=1, columnspan=1)
    

    Strats = tk.StringVar()
    options = [
        "No Strategy",
        "BarUpDn",
        "Greedy",
        "MACD",
        "MovingAvg"
    ]
    Strats.set(options[0])
    lbl_drp = tk.Label(frame_2, text="Strategies").grid(row=2, column=0)
    strat_list = tk.OptionMenu(frame_2, Strats, *options).grid(row=2, column=1)



    ################### FRAME3 ###################
    """ FRAME 3"""
    frame_3 = tk.LabelFrame(root, text="Profit", padx=290, pady=10)
    frame_3.grid(row=3, column=1, padx=5, pady=5)
    

    def prof():
        
        init_cap = int(inp_capita.get())
        X, scaler, pullData = forecaster.prepare_data(pth)
        predictions = forecaster.forecast(X, scaler, pthm)
        num_btc, profit = forecaster.estimate_profit(data=pullData,
         predictions=predictions, 
         initial_capita=init_cap)
        
        init_lbl = tk.Label(frame_3, text=f"Initial Capita: {init_cap}", anchor=tk.W)
        if float(profit)>0:
            prof_lbl = tk.Label(
                frame_3, text=f"Your profit at the end of next day: {profit}$",
                fg='green'
                )
        else:
            prof_lbl = tk.Label(
                frame_3, text=f"Your profit at the end of next day: {profit}$",
                fg='red'
                )

        btc_lbl = tk.Label(frame_3, text=f"You have {num_btc} bitcoins")

        init_lbl.grid(row=1, column=0, columnspan=2)
        prof_lbl.grid(row=2, column=1)
        btc_lbl.grid(row=3, column=1)

    """" End FRAME3 """

    btn =tk.Button(frame_2, text="Submit",
     padx=5, command=prof
     ).grid(row=3, column=0)

    """ End FRAME 2 """




    """Quit"""
    def popup():
        response = tk.messagebox.askyesno("Quit", "Exit the program?")
        #Button TEST
        tk.Label(root, text=response).grid(row=3, column=0)

        if response:
            root.destroy()

    button_quit = tk.Button(
        master=root, text="Quit",
        command=popup, width=6,
        padx=8, pady=8,
        bg='white', activebackground='grey'
         ).grid(
         row=3, column=0
         )
    """ End Quit """

    root.update_idletasks()
    root.mainloop()

######################################################
######################################################

if __name__ == '__main__':

    moonshots()