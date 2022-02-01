import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

def circles(x, y, df) :
    
    bg_color = '#4d6887'
    
    colors = {
    'background': bg_color,
    'text': '#111111'
    }
    
    fig = px.scatter(df, x = x, y = y, 
                    width = 834, 
                    height = 580, 
                    color = 'categ', 
                    hover_name = 'categ', 
                    size_max = 100,
                    opacity = 0.8)
    
    fig.update_layout(   
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        
        font=dict(
            family='Open Sans',
            size=14,
            color="black")
        )
    
    fig.update_xaxes(
        range=(-1.2, 1.2),
        constrain='domain',
        showgrid=True, gridwidth=1, gridcolor=bg_color)
    
    fig.update_yaxes(
        range=(-1.2, 1.2),
        constrain='domain',
        showgrid=True, gridwidth=1, gridcolor=bg_color)
    
    fig.add_shape(type="circle",
        xref="x", yref="y",
        x0=1, y0=1, x1=-1, y1=-1,
        line_color='bLACK')
    
    fig.update_traces(marker=dict(size=16))
    
    return fig



def blank_fig():
    
    bg_color = '#4d6887'
    
    colors = {
    'background': bg_color,
    'text': '#111111'
    }
    
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_layout(   
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],)
    
    return fig