import matplotlib.pyplot as plt 
import seaborn as sns
from io import BytesIO
import base64
# from django.contrib.auth.models import User
import random as random
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from matplotlib import pyplot as plt, dates
import datetime
import cufflinks as cf
cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)
import numpy as np
import matplotlib.ticker as ticker



def get_image():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()

    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')

    buffer.close()

    return graph




def get_bar_chart( *args, **kwargs):
    plt.switch_backend('AGG')
    # fig = plt.figure(figsize=(12,6))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    
    fig, ax = plt.subplots(figsize=(10,6))
    plt.xticks(rotation=60)
    plt.ylabel('Count')
    title = "Total Behavior Incidents by Day"
    plt.title(title)

    date_form = DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

    
    # plt.grid(True)   
    
    plt.bar(x, y)
         

    # made this change on 10/4/2023:
    # space = 1
    # ax.yaxis.set_major_locator(ticker.MultipleLocator(space))
    
    bar_graph = get_image()
        
    return bar_graph



# heatmapxxxxxxxxxxxxxx xxxx xxxxxxx


def get_heatmap( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior, Antecedent, Function)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    iheat_graph = get_image()

    return iheat_graph




# antecedent correlation
def get_heatmap_antecedent( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Antecedent)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    iheat_graph_antecedent = get_image()

    return iheat_graph_antecedent


def get_heatmap_antecedent_pdf( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Antecedent)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    
    return buffer

# clustermap


def get_clustermap( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Clustermap (Behaviors, Antecedents, Functions)"
    plt.title(title)
  
  
    sns.clustermap(data,  annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()
    
    iclustermap_graph = get_image()

    return iclustermap_graph


def get_clustermap_antecedent( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Clustermap (Behaviors and Antecedents)"
    plt.title(title)
  



  
    sns.clustermap(data,  annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()
    
    iclustermap_graph_antecedent = get_image()

    return iclustermap_graph_antecedent

def get_box_plot_function( *args, **kwargs):
    plt.switch_backend('AGG')    
    # fig = plt.figure()
    fig = plt.figure(figsize=(10,6))

    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Function and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Function')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    box_graph_function = get_image()

    return box_graph_function

def get_box_plot_pdf( *args, **kwargs):
    plt.switch_backend('AGG')    
    fig = plt.figure(figsize=(10,6))
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Antecedent and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    
    return buffer

def get_box_plot_function_pdf( *args, **kwargs):
    plt.switch_backend('AGG')    
    # fig = plt.figure()
    fig = plt.figure(figsize=(10,6))

    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Function and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Function')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    
    return buffer

# function correlation
def get_heatmap_function( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Function)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    iheat_graph_function = get_image()

    return iheat_graph_function

def get_heatmap_function_pdf( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Function)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    
    return buffer
def get_clustermap_function( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Clustermap (Behaviors and Antecedents)"
    plt.title(title)
  
    sns.clustermap(data,  annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()
    
    iclustermap_graph_function = get_image()

    return iclustermap_graph_function


def get_box_plot_consequence( *args, **kwargs):
    plt.switch_backend('AGG')    
    fig = plt.figure(figsize=(10,6))
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Consequence and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Consequence')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    box_graph_consequence = get_image()

    return box_graph_consequence


def get_box_plot_consequence_pdf( *args, **kwargs):
    plt.switch_backend('AGG')    
    fig = plt.figure(figsize=(10,6))
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Consequence and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Consequence')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    
    return buffer
# consequence correlation
def get_heatmap_consequence( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Consequence)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    iheat_graph_consequence = get_image()

    return iheat_graph_consequence

def get_heatmap_consequence_pdf( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Consequence)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    
    return bufferd

def get_clustermap_consequence( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Clustermap (Behaviors and Consequence)"
    plt.title(title)
  
    sns.clustermap(data,  annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()
    
    iclustermap_graph_consequence = get_image()

    return iclustermap_graph_consequence


def get_box_plot( *args, **kwargs):
    plt.switch_backend('AGG')    
    fig = plt.figure(figsize=(10,6))
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Antecedent and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Antecedent')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    box_graph = get_image()

    return box_graph


def get_box_plot_setting( *args, **kwargs):
    plt.switch_backend('AGG')    
    fig = plt.figure(figsize=(10,6))
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Setting and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Setting')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    box_graph_setting = get_image()

    return box_graph_setting

def get_heatmap_setting( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Correlation Heatmap (Behavior and Setting)"
    plt.title(title)
       
    sns.heatmap(data,annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()

    
    iheat_graph_setting = get_image()

    return iheat_graph_setting


def get_clustermap_setting( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(10,5))
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')

    title = "Clustermap (Behaviors and Setting)"
    plt.title(title)
  
    sns.clustermap(data,  annot=True, cmap='rocket_r', vmin=0, vmax=1, linewidths=.5, linecolor='black')
    sns.despine(top=True,right=False)

    plt.tight_layout()
    
    iclustermap_graph_setting = get_image()

    return iclustermap_graph_setting



def get_multiple_line_plot_five( *args, **kwargs):
    plt.switch_backend('AGG')
    fig,(ax1, ax2,ax3,ax4,ax5) = plt.subplots(4,figsize=(10, 6))

    date_form = DateFormatter("%m/%d")

    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax2.xaxis.set_major_formatter(date_form)
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax3.xaxis.set_major_formatter(date_form)
    ax3.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax4.xaxis.set_major_formatter(date_form)
    ax4.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    
    ax5.xaxis.set_major_formatter(date_form)
    ax5.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    g = kwargs.get('g')
    q = kwargs.get('q')
    m = kwargs.get('m')
    n = kwargs.get('n')
    b = kwargs.get('b')
    c = kwargs.get('c')
    
    
    
  
    data = kwargs.get('data')
    data1 = kwargs.get('data1')
    data2 = kwargs.get('data2')
    data3 = kwargs.get('data3')
    data4 = kwargs.get('data4')

   
    title = "Line Graph"
    plt.title(title)
    
    plt.subplots_adjust(left=0.1,
                    bottom=0.20,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.9)
    
    
    # fig.tight_layout() 
    
    ax1.bar(x, y)
    ax2.bar(z, k)
    ax3.bar(g, q)
    ax4.bar(m,n)
    ax5.bar(b,c)
        
    ax1.title.set_text(data.columns[1])
    ax2.title.set_text(data.columns[2])
    ax3.title.set_text(data.columns[3])
    ax4.title.set_text(data.columns[4])
    ax5.title.set_text(data.columns[5])
    
    multiple_line_plot_five = get_image()

    return multiple_line_plot_five


def get_multiple_line_plot_four( *args, **kwargs):
    plt.switch_backend('AGG')
    fig,(ax1, ax2,ax3,ax4) = plt.subplots(4,figsize=(10, 6))

    date_form = DateFormatter("%m/%d")

    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax2.xaxis.set_major_formatter(date_form)
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax3.xaxis.set_major_formatter(date_form)
    ax3.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax4.xaxis.set_major_formatter(date_form)
    ax4.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    g = kwargs.get('g')
    q = kwargs.get('q')
    m = kwargs.get('m')
    n = kwargs.get('n')
    
    
  
    data = kwargs.get('data')
    data1 = kwargs.get('data1')
    data2 = kwargs.get('data2')
    data3 = kwargs.get('data3')

   
    title = "Line Graph"
    plt.title(title)
    
    plt.subplots_adjust(left=0.1,
                    bottom=0.20,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.9)
    
    
    # fig.tight_layout() 
    
    ax1.bar(x, y)
    ax2.bar(z, k)
    ax3.bar(g, q)
    ax4.bar(m,n)
        
    ax1.title.set_text(data.columns[1])
    ax2.title.set_text(data.columns[2])
    ax3.title.set_text(data.columns[3])
    ax4.title.set_text(data.columns[4])

    multiple_line_plot_four = get_image()

    return multiple_line_plot_four

def get_multiple_line_plot_three( *args, **kwargs):
    plt.switch_backend('AGG')
    # fig, axs,ax = plt.subplots(2)
    fig,(ax1, ax2,ax3) = plt.subplots(3,figsize=(10, 6))


    date_form = DateFormatter("%m/%d")    

    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax2.xaxis.set_major_formatter(date_form)
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax3.xaxis.set_major_formatter(date_form)
    ax3.xaxis.set_major_locator(mdates.DayLocator(interval=2))
   
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    g = kwargs.get('g')
    q = kwargs.get('q')

    data = kwargs.get('data')
    data1 = kwargs.get('data1')
    data2 = kwargs.get('data2')
  
    title = "Line Graph"
    plt.title(title)
    
    plt.subplots_adjust(left=0.1,
                    bottom=0.20,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.9)
    
    
    # fig.tight_layout() 

    ax1.bar(x, y)
    ax2.bar(z, k)
    ax3.bar(g, q)
    
    
    ax1.title.set_text(data.columns[1])
    ax2.title.set_text(data.columns[2])
    ax3.title.set_text(data.columns[3])

    multiple_line_plot_three = get_image()

    return multiple_line_plot_three



def get_multiple_line_plot_two( *args, **kwargs):
    plt.switch_backend('AGG')
    # fig, axs,ax = plt.subplots(2)
    fig,(ax1, ax2) = plt.subplots(2,figsize=(10, 6))


    date_form = DateFormatter("%m/%d")

    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    ax2.xaxis.set_major_formatter(date_form)
    ax2.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
  
  
    data = kwargs.get('data')
    data1 = kwargs.get('data1')
  

    title = "Line Graph"
    plt.title(title)
      
    plt.subplots_adjust(left=0.1,
                    bottom=0.20,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.9)
    
    
    # fig.tight_layout() 


    ax1.bar(x, y)
    ax2.bar(z, k)
  
    ax1.title.set_text(data.columns[1])
    ax2.title.set_text(data.columns[2])

    multiple_line_plot_two = get_image()

    return multiple_line_plot_two


def get_multiple_line_plot_one( *args, **kwargs):
    plt.switch_backend('AGG')
    # fig, axs,ax = plt.subplots(2)
    fig,(ax1) = plt.subplots(1,figsize=(10, 6))


    date_form = DateFormatter("%m/%d")

    ax1.xaxis.set_major_formatter(date_form)
    ax1.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    
    
    x = kwargs.get('x')
    y = kwargs.get('y')

  
  
    data = kwargs.get('data')
 

    title = "Line Graph"
    plt.title(title)
      
    plt.subplots_adjust(left=0.1,
                    bottom=0.20,
                    right=0.9,
                    top=0.9,
                    wspace=0.9,
                    hspace=0.9)
    
    
    # fig.tight_layout() 


    ax1.plot(x, y, marker='o')
  
    ax1.title.set_text(data.columns[1])

    multiple_line_plot_one = get_image()

    return multiple_line_plot_one









def get_multiple_line_plot_chatgpt(*args, **kwargs):
    plt.switch_backend('AGG')
    fig, axs = plt.subplots(len(args), figsize=(10, 6))

    date_form = DateFormatter("%m/%d")

    for i, (ax, data) in enumerate(zip(axs, args)):
        ax.xaxis.set_major_formatter(date_form)
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))

        x = kwargs.get(f'x{i+1}')
        y = kwargs.get(f'y{i+1}')

        ax.bar(x, y)
        ax.title.set_text(data.columns[i+1])

    plt.subplots_adjust(left=0.1, bottom=0.20, right=0.9, top=0.9, wspace=0.9, hspace=0.9)
    fig.tight_layout()

    multiple_line_plot_chatgpt = get_image()

    return multiple_line_plot_chatgpt



def get_count_beh_plot( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure()
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    
    sns.countplot(x=x, data=data)
    plt.xticks(rotation=45)
    plt.xlabel('Behavior')
    plt.ylabel('Frequency')

    title = "Behavior Frequency"
    plt.title(title)

    plt.tight_layout()
  
    
    beh_count_graph = get_image()

    return beh_count_graph



def get_count_beh_plot_pdf( *args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure()
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    
    sns.countplot(x=x, data=data)
    plt.xticks(rotation=45)
    plt.xlabel('')
    plt.ylabel('Frequency')

    title = "Behavior Frequency"
    plt.title(title)

    plt.tight_layout()
  
    
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    return buffer



def get_count_time_plot( *args, **kwargs):
    plt.switch_backend('AGG')
    
    fig = plt.figure()
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    
    sns.countplot(x=x, data=data)
    plt.xticks(rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Count')

    title = "# of Incidents by Behavior"
    plt.title(title)

    plt.tight_layout()
  
    
    time_count_graph = get_image()

    return time_count_graph



def get_multiple_scatter_plot_five( *args, **kwargs):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10,7))
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    g = kwargs.get('g')
    q = kwargs.get('q')
    m = kwargs.get('m')
    n = kwargs.get('n')
    a = kwargs.get('a')
    b = kwargs.get('b')
    data = kwargs.get('data')
    data1 = kwargs.get('data1')
    data2 = kwargs.get('data2')
    data3 = kwargs.get('data3')
    data3 = kwargs.get('data4')

    title = "Target Behavior Incidents by Day"
    plt.title(title)
    date_form = DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.grid(True)
    plt.xlabel(' ')
    plt.ylabel('Count')
  
    # plt.style.use('seaborn')
    plt.xticks(rotation=90)

    plt.scatter(x, y, marker = 6, s = 175, label=data.columns[1])
    
  
    plt.scatter(z, k,  marker = 4,   s = 175,label=data.columns[2])
    
    plt.scatter(g, q,  marker = 7,  s = 175,label=data.columns[3])
    plt.scatter(m, n,  marker = 5,  s = 175, label=data.columns[4])
    
    plt.scatter(a, b,  marker = 0,  s = 175, label=data.columns[5])

    plt.legend()
    
    multiple_scater_plot_five = get_image()

    return multiple_scater_plot_five



def get_multiple_scatter_plot_four( *args, **kwargs):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10,7))
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    g = kwargs.get('g')
    q = kwargs.get('q')
    m = kwargs.get('m')
    n = kwargs.get('n')
    data = kwargs.get('data')
    data1 = kwargs.get('data1')
    data2 = kwargs.get('data2')
    data3 = kwargs.get('data3')

    title = "Target Behavior Incidents by Day"
    plt.title(title)
    date_form = DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.grid(True)
    plt.xlabel(' ')
    plt.ylabel('Count')
  
    # plt.style.use('seaborn')
    plt.xticks(rotation=90)

    plt.scatter(x, y, marker = 6, s = 175, label=data.columns[1])
    
  
    plt.scatter(z, k,  marker = 4,   s = 175,label=data.columns[2])
    
    plt.scatter(g, q,  marker = 7,  s = 175,label=data.columns[3])
    plt.scatter(m, n,  marker = 5,  s = 175, label=data.columns[4])

    plt.legend()
    
    multiple_scater_plot_four = get_image()

    return multiple_scater_plot_four


def get_multiple_scatter_plot_three( *args, **kwargs):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10,7))
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    g = kwargs.get('g')
    q = kwargs.get('q')
    data = kwargs.get('data')
    data1 = kwargs.get('data1')
    data2 = kwargs.get('data2')

    title = "Target Behavior Incidents by Day"
    plt.title(title)
    date_form = DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.grid(True)
    plt.xlabel(' ')
    plt.ylabel('Count')
  
    # plt.style.use('seaborn')
    plt.xticks(rotation=90)

    plt.scatter(x, y, marker = 6, s = 175, label=data.columns[1])
    
  
    plt.scatter(z, k,  marker = 4,   s = 175,label=data.columns[2])
    
    plt.scatter(g, q,  marker = 7,  s = 175,label=data.columns[3])

    plt.legend()
    
    multiple_scater_plot_three = get_image()

    return multiple_scater_plot_three



def get_multiple_scatter_plot_two( *args, **kwargs):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10,7))
    x = kwargs.get('x')
    y = kwargs.get('y')
    z = kwargs.get('z')
    k = kwargs.get('k')
    
    data = kwargs.get('data')
    data1 = kwargs.get('data1')


    title = "Target Behavior Incidents by Day"
    plt.title(title)
    date_form = DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.grid(True)
    plt.xlabel('')
    plt.ylabel('Count')
  
    # plt.style.use('seaborn')
    plt.xticks(rotation=90)

    plt.scatter(x, y, marker = 6, s = 175, label=data.columns[1])
    
  
    plt.scatter(z, k,  marker = 4,   s = 175,label=data.columns[2])
    

    plt.legend()
    
    multiple_scater_plot_two = get_image()

    return multiple_scater_plot_two




def get_multiple_scatter_plot_one( *args, **kwargs):
    plt.switch_backend('AGG')
    fig, ax = plt.subplots(figsize=(10,7))
    x = kwargs.get('x')
    y = kwargs.get('y')
   
    data = kwargs.get('data')
   

    title = "Target Behavior Incidents by Day"
    plt.title(title)
    date_form = DateFormatter("%m/%d")
    ax.xaxis.set_major_formatter(date_form)
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    plt.grid(True)
    plt.xlabel(' ')
    plt.ylabel('Count')
  
    # plt.style.use('seaborn')
    plt.xticks(rotation=90)

    plt.scatter(x, y, marker = 6, s = 175, label=data.columns[1])
    
    plt.legend()
    
    multiple_scater_plot_one = get_image()

    return multiple_scater_plot_one







def get_pie_chart( *args, **kwargs):
    
        plt.switch_backend('AGG')
        x  = kwargs.get('x')
        y = kwargs.get('y')
        labels = kwargs.get('labels')
        data = kwargs.get('data')
       
        fig = plt.figure()
        myexplode = [0.05, 0, 0, 0]
        plt.pie(x, labels=labels, autopct='%1.0f%%')
        plt.title("Behavior")
        pie_graph = get_image()
        
        return pie_graph
        



def get_pie__chart_anticedent( *args, **kwargs):
    
        plt.switch_backend('AGG')
        x  = kwargs.get('x')
        y = kwargs.get('y')
        labels = kwargs.get('labels')
        data = kwargs.get('data')
       
        fig = plt.figure()
        myexplode = [0.05, 0, 0, 0]

        
        plt.pie(x, labels=labels, autopct='%1.0f%%')
        plt.title("Antecedent")
        pie_anticedent_graph = get_image()
        
        return pie_anticedent_graph
    
    
    
    
    
def get_pie__chart_function( *args, **kwargs):

        plt.switch_backend('AGG')
        x  = kwargs.get('x')
        y = kwargs.get('y')
        labels = kwargs.get('labels')
        data = kwargs.get('data')
       
        fig = plt.figure()
        # myexplode = [0.05, 0, 0, ]
        plt.pie(x, labels=labels, autopct='%1.0f%%')
        plt.title("Function")
        pie_function_graph = get_image()
        
        return pie_function_graph
    
    
def get_pie__chart_consequence( *args, **kwargs):

        plt.switch_backend('AGG')
        x  = kwargs.get('x')
        y = kwargs.get('y')
        labels = kwargs.get('labels')
        data = kwargs.get('data')
       
        fig = plt.figure()
        # myexplode = [0.05, 0, 0, ]
        plt.pie(x, labels=labels, autopct='%1.0f%%')
        plt.title("Consequence")
        pie_consequence_graph = get_image()
        
        return pie_consequence_graph  
    
    
def get_duration_bar_chart( *args, **kwargs):
    
    plt.switch_backend('AGG')
    fig = plt.figure()

    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
   
        

   
     
    plt.bar(x, y) 
      
    title = "Average Duration of Behavior"
    plt.title(title)
    
    # plt.yticks(np.arange(min(y), max(y)+10, 30.0))
  
   
    plt.ylabel('Seconds')
 
    box_duration_graph = get_image()

    return box_duration_graph


    
def get_duration_bar_chart_pdf(*args, **kwargs):
   
    plt.switch_backend('AGG')
    fig, ax = plt.subplots()

    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
   
    plt.bar(x, y) 
      
    title = "Average Duration of Behavior"
    plt.title(title)
    
    # plt.yticks(np.arange(min(y), max(y)+10, 30.0))
  
    plt.ylabel('Seconds')
 
    # Create a BytesIO buffer and save the figure into it
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)  # Move to the start of the buffer
    plt.close(fig)  # Close the figure to free memory

    return buffer
def get_intensity_bar_chart(*args, **kwargs):
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6, 6))  # Adjust figure size as needed
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    plt.xticks(rotation=60)
    
    plt.bar(x, y) 
    title = "Average Intensity of Behavior (1-Mild, 2-Moderate, 3-Severe)"
    plt.title(title)
    plt.ylabel('Intensity')
    plt.tight_layout()  # Adjust layout
    
    # Get the image and return
    box_intensity_graph = get_image()
    
    return box_intensity_graph



def get_intensity_bar_chart_pdf( *args, **kwargs):
    
    plt.switch_backend('AGG')
    fig = plt.figure(figsize=(6, 6))  # Adjust figure size as needed
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    plt.xticks(rotation=60)

        

    plt.tight_layout()

     
    plt.bar(x, y) 
      
    title = "Average Intensity of Behavior"
    plt.title(title)
    
  
   
    plt.ylabel('Intensity')
 
    buffer = BytesIO()  # Create a BytesIO buffer
    plt.savefig(buffer, format='png')  # Save the plot to the buffer
    buffer.seek(0)  # Seek to the start of the buffer
    plt.close(fig)  # Close the plot to free memory
    return buffer


def get_box_plot_time( *args, **kwargs):
    plt.switch_backend('AGG')    
    fig = plt.figure()
    
    x = kwargs.get('x')
    y = kwargs.get('y')
    data = kwargs.get('data')
    title = "Time and Behavior"
    plt.title(title)

    sns.countplot(x=x, hue='Behavior', data=data)

    plt.xticks(rotation=45)
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.legend(title='Behavior')
    
    box_graph_time = get_image()

    return box_graph_time