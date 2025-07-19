import gradio as gr
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from rpy2.robjects import r
import subprocess
import os

def eda_python(df):
    """Genera informe EDA básico en Python como string."""
    info_str = str(df.info())
    desc_str = df.describe().T.to_string()
    return info_str, desc_str

def plot_pairplot(df):
    plt.figure(figsize=(8, 6))
    sns.pairplot(df.select_dtypes(include=np.number), diag_kind="hist")
    plt.tight_layout()
    plt.savefig("pairplot.png")
    plt.close()
    return "pairplot.png"

def plot_histogram(df, column):
    plt.figure(figsize=(8, 6))
    df[column].hist(bins=30)
    plt.title(f"Histograma: {column}")
    plt.savefig("hist.png")
    plt.close()
    return "hist.png"

def plot_bar(df, column):
    plt.figure(figsize=(8, 6))
    df[column].value_counts().plot(kind='bar')
    plt.title(f"Barra: {column}")
    plt.savefig("bar.png")
    plt.close()
    return "bar.png"

def plot_pie(df, column):
    plt.figure(figsize=(8, 6))
    df[column].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title(f"Pie: {column}")
    plt.savefig("pie.png")
    plt.close()
    return "pie.png"

def generar_eda_r(df):
    """Genera reporte EDA usando R."""
    input_csv = "df_temp.csv"
    eda_output = "reporte_R.html"
    df.to_csv(input_csv, index=False)
    subprocess.run(["Rscript", "r_eda_script.R", input_csv, eda_output])
    return eda_output

def process_file(file, show_info, graph_type, graph_column, eda_python_chk, eda_r_chk):
    if file is None:
        return "No file uploaded.", None, None, None, None, None
    df = pd.read_csv(file.name)
    info_str, desc_str = "", ""
    if show_info:
        info_str, desc_str = eda_python(df)
        pairplot_path = plot_pairplot(df)
    else:
        pairplot_path = None

    graph_output = None
    if graph_type and graph_column:
        if graph_type == "Histograma":
            graph_output = plot_histogram(df, graph_column)
        elif graph_type == "Barras":
            graph_output = plot_bar(df, graph_column)
        elif graph_type == "Pie":
            graph_output = plot_pie(df, graph_column)

    eda_python_report = ""
    eda_r_report = ""
    if eda_python_chk:
        eda_python_report = (info_str, desc_str)
    if eda_r_chk:
        eda_r_report = generar_eda_r(df)
    return (info_str, desc_str, pairplot_path, graph_output, eda_python_report, eda_r_report)

# Gradio INTERFACE

def interface(file, show_info, graph_type, graph_column, eda_python_chk, eda_r_chk):
    res = process_file(file, show_info, graph_type, graph_column, eda_python_chk, eda_r_chk)
    info_str, desc_str, pairplot_path, graph_output, eda_python_report, eda_r_report = res
    eda_r_link = None
    if eda_r_report:
        eda_r_link = f'<a href="{eda_r_report}" download>Descargar EDA R</a>'
    return info_str, desc_str, (pairplot_path if pairplot_path else None), (graph_output if graph_output else None), eda_r_link

with gr.Blocks() as demo:
    gr.Markdown("# Análisis Exploratorio: Python + R + Gradio")
    file = gr.File(label="Sube tu archivo CSV")
    show_info = gr.Checkbox(label="Ver info del DataFrame (info, describe, pairplot)")
    with gr.Row():
        graph_type = gr.Radio(choices=["Histograma", "Barras", "Pie"], label="Tipo de gráfico")
        graph_column = gr.Textbox(label="Columna para graficar (nombre exacto)")

    eda_python_chk = gr.Checkbox(label="Generar EDA en Python")
    eda_r_chk = gr.Checkbox(label="Generar EDA en R")
    submit = gr.Button("Procesar")

    info_str = gr.Textbox(label="DataFrame info()", interactive=False)
    desc_str = gr.Textbox(label="DataFrame describe().T", interactive=False)
    pairplot_img = gr.Image(label="Pairplot (sólo numéricos)")
    graph_img = gr.Image(label="Gráfico elegido")
    eda_r_link = gr.HTML(label="Descargar reporte EDA R")

    submit.click(interface,
                 inputs=[file, show_info, graph_type, graph_column, eda_python_chk, eda_r_chk],
                 outputs=[info_str, desc_str, pairplot_img, graph_img, eda_r_link])

if __name__ == "__main__":
    demo.launch()