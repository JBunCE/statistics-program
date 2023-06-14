import customtkinter
import pandas
import pandastable

from utilities.calculator_util import CalculatorUtil
from utilities.charts_util import ChartsCreator


class MainWindow(customtkinter.CTk):
    title_font = ('Roboto', 24)
    normal_font = ('Roboto', 10)
    normal_alternative_font = ('Roboto', 14)
    quantitative_charts = ['grafica_de_pastel_cn', 'histograma', 'ojiva', 'poligono_de_frecuencia']
    qualitative_charts = ['grafica_de_pastel', 'grafica_de_barras']

    def __init__(self):
        super().__init__()
        self.fig = None
        self.recurrence_table = None
        self.results_label = None
        self.recurrence_table_widget = None
        self.table_widget: pandastable.Table
        self.geometry('1300x650')

        self.selection_frame = customtkinter.CTkFrame(master=self)
        self.selection_frame.pack(pady=10, fill='y', expand=True)

        self.title_label = customtkinter.CTkLabel(master=self.selection_frame,
                                                  text='Data system',
                                                  font=self.title_font)
        self.title_label.pack(pady=10, padx=25)

        self.load_dataset_btn = customtkinter.CTkButton(master=self.selection_frame,
                                                        text='Cargar dataset',
                                                        command=self.__load_data_event)
        self.load_dataset_btn.pack(pady=10, padx=25)

        self.select_chart_title = customtkinter.CTkLabel(master=self.selection_frame,
                                                         text='seleccion de grafica',
                                                         font=self.title_font)

        self.select_column_label = customtkinter.CTkLabel(master=self.selection_frame,
                                                          text='Seleccione una columna del data frame',
                                                          font=self.normal_font)

        self.group_data = customtkinter.CTkButton(master=self.selection_frame,
                                                  text='Generar tabla de frecuencia',
                                                  command=self.generate_rec_table_event)

        self.qual_charts_selector = customtkinter.CTkComboBox(self.selection_frame,
                                                              values=self.qualitative_charts,
                                                              state='readonly',
                                                              command=self.select_chart_event)

        self.quan_charts_selector = customtkinter.CTkComboBox(self.selection_frame,
                                                              values=self.quantitative_charts,
                                                              state='readonly',
                                                              command=self.select_chart_event)

        self.export_qua_btn = customtkinter.CTkButton(master=self.selection_frame,
                                                      text='exportar tabla')

        self.export_quan_btn = customtkinter.CTkButton(master=self.selection_frame,
                                                       text='exportar tabla')

        self.data_group_frame = customtkinter.CTkFrame(master=self)
        self.data_group_frame.pack(padx=10,
                                   pady=10,
                                   anchor='e',
                                   fill='both',
                                   side='right',
                                   expand=True,
                                   before=self.selection_frame)

        self.results_frame = customtkinter.CTkFrame(master=self)
        self.results_frame.pack(padx=10,
                                pady=10,
                                anchor='e',
                                fill='both',
                                side='right',
                                expand=True,
                                before=self.data_group_frame)

        self.charts_frame = customtkinter.CTkFrame(master=self)
        self.charts_frame.pack(padx=10,
                               pady=10,
                               anchor='e',
                               fill='both',
                               side='right',
                               expand=True,
                               before=self.results_frame)

        self.dataset_frame = customtkinter.CTkFrame(master=self)
        self.dataset_frame.pack(padx=5,
                                pady=5,
                                anchor='s',
                                fill='x',
                                side='bottom',
                                before=self.results_frame)

    def __load_data_event(self):
        dataset_path = customtkinter.filedialog.askopenfilename(filetypes=[('CSV Files', '*csv')])
        selected_dataframe = pandas.read_csv(dataset_path)

        self.table_widget = pandastable.Table(self.dataset_frame, dataframe=selected_dataframe, editable=False)
        self.table_widget.show()

        self.select_column_label.pack(pady=12, padx=25)
        self.group_data.pack(pady=12, padx=25)
        self.load_dataset_btn.destroy()

    def generate_rec_table_event(self):
        self.__clean_frames()
        selected_colum = self.table_widget.getSelectedDataFrame().columns[0]
        selected_attribute = self.table_widget.getSelectedDataFrame()[selected_colum].values
        calculator_util = CalculatorUtil()
        calculation = calculator_util.calculate(selected_attribute)

        self.recurrence_table = calculation["recurrence_table"]
        results = calculation["params"]

        self.recurrence_table_widget = pandastable.Table(self.data_group_frame,
                                                         dataframe=self.recurrence_table, editable=False)
        self.recurrence_table_widget.show()
        self.select_chart_title.pack(pady=10, padx=15)

        if type(selected_attribute[0]) == str:
            self.quan_charts_selector.pack_forget()
            self.qual_charts_selector.pack(pady=10, padx=10)

            results_text = f" -------- RESULTADOS --------" \
                           f"\n Moda: {results['moda']}" \
                           f"\n Mediana: {results['mediana']}"

            self.results_label = customtkinter.CTkLabel(master=self.results_frame,
                                                        text=results_text,
                                                        font=self.normal_alternative_font,
                                                        justify="left")
            self.results_label.pack(padx=15, pady=15)
        else:
            self.qual_charts_selector.pack_forget()
            self.quan_charts_selector.pack(pady=10, padx=10)

            group_results = calculation["group_params"]

            results_text = f" -------- RESULTADOS --------" \
                           f"\n Rango: {results['rango']}" \
                           f"\n Media: {results['media']}" \
                           f"\n Medaia geometrica: {results['media geometrica']}" \
                           f"\n Media truncada: {results['media truncada']}" \
                           f"\n Mediana: {results['mediana']}" \
                           f"\n Moda: {results['moda']}" \
                           f"\n Varianza: {results['varianza']}" \
                           f"\n Desviacion estandar: {results['desviacion estandar']}" \
                           f"\n Sesgo: {results['sesgo']}" \
                           f"\n Posicion del sesgo: {results['posicion del sesgo']} " \
                           f"\n"\
                           f"\n -------- RESULTADOS DATOS AGRUPADOS --------" \
                           f"\n Media: {group_results['media']}" \
                           f"\n Mediana: {group_results['mediana']}" \
                           f"\n Moda: {group_results['moda']}" \
                           f"\n Varianza: {group_results['varianza']}" \
                           f"\n Desviacion estandar: {group_results['desviacion estandar']}"

            self.results_label = customtkinter.CTkLabel(master=self.results_frame,
                                                        text=results_text,
                                                        font=self.normal_alternative_font,
                                                        justify="left")
            self.results_label.pack(padx=15, pady=15)

    def select_chart_event(self, event):
        self.__clean_charts_frames()
        charts = ChartsCreator()
        if event == "grafica_de_pastel":
            self.fig = charts.pie_graphic(self.recurrence_table, self.charts_frame)

        if event == "grafica_de_barras":
            self.fig = charts.bar_graphic(self.recurrence_table, self.charts_frame)

        if event == "grafica_de_pastel_cn":
            self.fig = charts.pie_chart_quantitative(self.recurrence_table, self.charts_frame)

        if event == "histograma":
            self.fig = charts.histogram(self.recurrence_table, self.charts_frame)

        if event == "ojiva":
            self.fig = charts.ojiva(self.recurrence_table, self.charts_frame)

        if event == "poligono_de_frecuencia":
            self.fig = charts.recurrence_polygon(self.recurrence_table, self.charts_frame)

    def __clean_frames(self):
        for widget in self.results_frame.winfo_children():
            widget.destroy()

    def __clean_charts_frames(self):
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
