from typedefs import Plot_Data
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class Plotter:
    def begin_plotting(Schedulers_To_Test, x_label="n", y_label="Makespan", x_scale="linear"):
        figure, axis = plt.subplots(nrows=len(Schedulers_To_Test),gridspec_kw={'hspace': 1, 'wspace': 0})
        for i in range(len(Schedulers_To_Test)):            
            axis[i].set_title(Schedulers_To_Test[i].__name__)
            axis[i].set_xlabel(x_label)
            axis[i].set_ylabel(y_label)
            axis[i].set_xscale(x_scale)
        return figure,axis

    def plot_graphs(figure, axis, plot_data_list : list[Plot_Data], x, color):
        x_values = x
        for i in range(len(plot_data_list)):
            plot_data = plot_data_list[i]
            y = np.array(plot_data.means)
            axis[i].plot(x_values, y, color=color)
            

    def plot_graph(plot_data_list : list[Plot_Data], x, x_label="n", y_label="Makespan", x_scale="linear"):
        figure, axis = plt.subplots(nrows=len(plot_data_list),gridspec_kw={'hspace': 1, 'wspace': 0})
        x_values = x
        for i in range(len(plot_data_list)):
            plot_data = plot_data_list[i]
            y = np.array(plot_data.means)
            lower_error = np.array(plot_data.neg_deviations)
            upper_error = np.array(plot_data.pos_deviations)
            axis[i].errorbar(x_values, y, yerr=[lower_error,upper_error], linestyle='-', marker='o')
            
            axis[i].set_title(plot_data.scheduler_name)
            axis[i].set_xlabel(x_label)
            axis[i].set_ylabel(y_label)
            axis[i].set_xscale(x_scale)

        figure.subplots_adjust(wspace=20)
        plt.show()
    
    def plot_table(data_list, column_labels, row_labels):
        figure, axis = plt.subplots()
        axis.axis('off')
        axis.axis('tight')

        table_data = np.transpose(np.array(data_list))

        df=pd.DataFrame(table_data,columns=column_labels)
        table= axis.table(cellText=df.values, colLabels=df.columns, rowLabels=row_labels, loc='center')
        figure.tight_layout()
        table.auto_set_font_size(value=False)
        table.set_fontsize(8)

        plt.show()