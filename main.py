import warnings

from ui.main_window import MainWindow

if __name__ == "__main__":
    warnings.filterwarnings("ignore", category=UserWarning)
    app = MainWindow()
    app.mainloop()
