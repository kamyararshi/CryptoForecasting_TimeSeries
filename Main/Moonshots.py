import tkinter as tk
from PIL import ImageTk, Image
from tkinter.font import BOLD
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.animation import FuncAnimation
from matplotlib import style

import subprocess
import os
import sys

import forecaster

#Use with caution and your own responsibility
#Maintanance between 00:00 and 01:00

def main():
    splash_root = tk.Tk()
    splash_root.title("Cryptocaster")
    splash_root.iconbitmap("python.ico")
    splash_root.geometry("400x300+550+250")
    # Hide title bar
    splash_root.overrideredirect(True)

    splash_label = tk.Label(splash_root, text="You are about to get rich!", font=("Calibri", 15, BOLD))
    splash_img = ImageTk.PhotoImage(Image.open("logo_splash.png"))
    splash_img_lbl = tk.Label(splash_root, image=splash_img)
    cred_label = tk.Label(splash_root, text="All Rights Reserved", font=("Arial", 8))

    splash_label.pack(pady=10)
    splash_img_lbl.pack()
    cred_label.pack()

    def main_window():
        splash_root.destroy()


        root = tk.Tk()
        root.title("Cryptocaster")
        root.iconbitmap("python.ico")
        root.geometry("1400x750+100-60")


        """ Top """
        tk.Label(root, text="In Bitcoin We Trust!", font=("Helvetica",18, BOLD), width=30).grid(row=0, column=0, columnspan=2)
        var_main = tk.IntVar()
        
        """ End Top """
        
        #LARGE_FONT=
        style.use("ggplot")

        #Set path directories for data and model
        main_pth = os.path.dirname(os.path.realpath(sys.argv[0]))
        pth = os.path.join(main_pth, r"Data\finaldata.csv")
        pthm = os.path.join(main_pth, r"Data\bilstmnew.h5")
                

    ################### FRAME1 ###################
        """ FRAME 1"""
        frame_1 = tk.LabelFrame(root, text="Price Plot: Predictions and Data", padx=10, pady=10)
        frame_1.grid(row=1, column=1, padx=5, pady=5)


        def show_plot():

            global fig
            global axs
            global ani

            fig, axs = plt.subplots(1, 1, sharex=True, sharey=True, figsize=(10,5))


            def animate(i):
                print(os.path.dirname(os.path.realpath(sys.argv[0])))
                
                # Get the dataframe and prepared data
                X, Y, pullData = forecaster.prepare_data(pth)
                # Predict using the prepared data
                predictions = forecaster.forecast(X, pthm)
                # Plot the price and predictions
                axs.clear()
                pullData.iloc[-500:].plot('Date', 'next_day_closing_price', ax=axs, label='Actual')
                axs.plot(predictions[-500:], label="Predictions")
                axs.legend()

                #Rotate
                for ax in fig.axes:
                    plt.sca(ax)
                    plt.xticks(rotation=90)
                
                axs.set_ylabel("Price USD")
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
        frame_2 = tk.LabelFrame(root, text="Options", padx=10, pady=20)
        frame_2.grid(row=1, column=0, padx=10, pady=10)

        lbl_info = tk.Label(frame_2, text="We shoot for the infinity",
        anchor=tk.N,
        font=("Playfair", 12, BOLD)
        ).grid(row=0, column=0, padx=5, pady=5)

        my_logo = ImageTk.PhotoImage(Image.open("img.png"))
        lbl_img = tk.Label(frame_2, image=my_logo)
        lbl_img.grid(
            row=1, column=0, padx=5, pady=45, columnspan=2)
        
        lbl_capita = tk.Label(frame_2, text="Initial Capita $").grid(row=2, column=0)
        inp_capita = tk.Entry(frame_2, width=20)
        inp_capita.grid(row=2, column=1, columnspan=2)



        ################### FRAME3 ###################
        """ FRAME 3"""
        frame_3 = tk.LabelFrame(root, text="Profit", padx=270, pady=10)
        frame_3.grid(row=3, column=1, padx=5, pady=5)
        

        def prof():
            
            init_cap = int(inp_capita.get())
            X, _, pullData = forecaster.prepare_data(pth)
            predictions = forecaster.forecast(X, pthm)
            num_btc, profit = forecaster.estimate_profit(data=pullData,
            predictions=predictions, 
            initial_capita=init_cap)
            
            date_lbl = tk.Label(frame_3,
            text=f"from {pullData['Date'].iloc[-2]} to {pullData['Date'].iloc[-1]}",
            fg='blue')
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

            date_lbl.grid(row=1, column=0, columnspan=2)
            init_lbl.grid(row=2, column=0, columnspan=2)
            prof_lbl.grid(row=3, column=1)
            btc_lbl.grid(row=4, column=1)

        """" End FRAME3 """

        btn =tk.Button(frame_2, text="Submit",
        padx=5, command=prof,
        bg='grey', activebackground='white'
        ).grid(row=4, column=0, pady=10)

        #Strategies and candle stick
        Strats = tk.StringVar()
        options = [
            "No Strategy",
            "BarUpDn",
            "Greedy",
            "MACD",
            "MovingAvg"
        ]
        Strats.set(options[0])
        lbl_drp = tk.Label(frame_2, text="Strategies").grid(row=3, column=0)
        strat_list = tk.OptionMenu(frame_2, Strats, *options).grid(row=3, column=1)
        
        #Streamlit
        def open():
            """
            Opens the Streamlit application
            """
            root.destroy()
            lst = subprocess.run(["streamlit", "run", "btc_app.py"])

            
            


        btn_update = tk.Button(frame_2,
        text="Update Data", command=forecaster.update,
        bg='white', activebackground='white',
        ).grid(row=5, column=0, pady=5)
        
        btn_candle = tk.Button(frame_2,
        text="More insights", command=open,
        bg='grey', activebackground='white').grid(row=6, column=0)

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
    #Splash Screen timer
    splash_root.after(2500, main_window)
    tk.mainloop()

######################################################
######################################################

if __name__ == '__main__':

    main()