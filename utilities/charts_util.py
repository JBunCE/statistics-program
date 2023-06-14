from copy import copy

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class ChartsCreator:
    def __init__(self):
        self.canvas = None
        self.fig = None
        self.fake_data = None
        print("soy la grafica")

    def bar_graphic(self, data, frame):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        ax.bar(data['marca_de_clase'], data['frecuencia'])
        ax.set_xlabel('marca de clase')
        ax.set_ylabel('Frecuencia absoluta')
        ax.set_title('Gráfica de Barras')
        ax.set_xticklabels(data['marca_de_clase'], rotation=45, ha='right')

        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="center")
        return self.fig

    def pie_graphic(self, data, frame):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        ax.pie(data['frecuencia'], labels=data['marca_de_clase'], autopct='%1.1f%%', rotatelabels=45)
        ax.set_title('Gráfica de Pastel')
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="center")
        return self.fig

    def pie_chart_quantitative(self, data, frame):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        ax.pie(data['frecuencia_relativa'], labels=data['marca_de_clase'], autopct='%1.1f%%', rotatelabels=45)
        ax.set_title('Gráfica de Pastel')
        ax.axis('equal')

        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="center")
        return self.fig

    def histogram(self, table, frame):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        table.plot(x='marca_de_clase', y='frecuencia', kind='bar', ax=ax)
        plt.xlabel('Marca de clase')
        plt.ylabel('Frecuencia')
        plt.title('Histograma')

        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="center")
        return self.fig

    def ojiva(self, original_data, frame):
        data = copy(original_data)
        self.fig = Figure(figsize=(6, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        data.at[0, "frecuencia"] = 0
        data.at[len(data) - 1, "frecuencia"] = 0

        data['frecuencia_acumulada'] = data['frecuencia'].cumsum()

        data['porcentaje_acumulado'] = (data['frecuencia_acumulada'] / data['frecuencia'].sum()) * 100

        data.plot(x='marca_de_clase', y='porcentaje_acumulado', kind='line', ax=ax)

        plt.xlabel('Marca de clase')
        plt.ylabel('Porcentaje acumulado')
        plt.title('Ojiva')

        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="center")
        return self.fig

    def recurrence_polygon(self, data, frame):
        self.fig = Figure(figsize=(6, 4), dpi=100)
        ax = self.fig.add_subplot(111)

        data.at[0, "frecuencia"] = 0
        data.at[len(data) - 1, "frecuencia"] = 0

        data.plot(x='marca_de_clase', y='frecuencia', ax=ax)
        plt.xlabel('Marca de clase')
        plt.ylabel('Frecuencia')
        plt.title('Histograma')

        canvas = FigureCanvasTkAgg(self.fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=20, pady=20, anchor="center")
        return self.fig