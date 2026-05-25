import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import datetime as dt
from pathlib import Path

from shiny.express import input, render, ui
from shinywidgets import output_widget, render_plotly

# -------------------- LOAD DATA --------------------
LBJ = pd.read_csv("data/LBJ.csv")
MJ = pd.read_csv("data/MJ.csv")
KAJ = pd.read_csv("data/KAJ.csv")
NBA_avg = pd.read_csv("data/NBA_avg.csv")
Pace = pd.read_csv("data/Pace.csv")
NBA_avg_standardized = pd.read_csv("data/NBA_avg_standardized.csv")

# Clean Season column
NBA_avg["Season"] = NBA_avg["Season"].astype(str).str.split("-").str[0]
NBA_avg["Season"] = NBA_avg["Season"].astype(int)

first_season = NBA_avg["Season"].min()
latest_season = NBA_avg["Season"].max()

DATA = {
    "Lebron James NBA statistics": LBJ,
    "Michael Jordan NBA statistics": MJ,
    "Kareem Abdul-Jabbar NBA statistics": KAJ,
    "NBA Average statistics": NBA_avg,
    "NBA Pace": Pace,
}

Players = {
    "Lebron James": LBJ,
    "Michael Jordan": MJ,
    "Kareem Abdul-Jabbar": KAJ,
}

# -------------------- APP UI & SERVER --------------------


ui.page_opts(title="NBA Legends Analysis/Comparison", id="page")

with ui.nav_control():
    ui.input_dark_mode()

with ui.nav_panel("Visualizations"):
    ui.input_slider(
        "slider",
        "Year Range",
        min=first_season,
        max=latest_season,
        value=[first_season, latest_season],
    )

    @render.text
    def val1():
        start, end = input.slider()
        return f"{start} - {end}: {end - start} seasons"
    #Now I will create a line plot showing the average statistics of the NBA throughout the years.

    #We will do this using plotly express for better interactivity and layout.

    ui.input_select(  
    "choose_Stats",  
    "Select statistic to visualize:",  
    {"PTS": "Points", "TRB": "Rebounds", "AST": "Assists", "STL": "Steals", "BLK": "Block", "PER": "Player Efficiency Rating"},  
    )  

    @render_plotly
    def nba_visualization():
        
        start, end = input.slider()
        filtered_data = NBA_avg[(NBA_avg["Season"] >= start) & (NBA_avg["Season"] <= end)]
        return px.line(filtered_data, x="Season", y=input.choose_Stats(), title=f"NBA Average {input.choose_Stats()} Over Time")


    ui.card_header("MY GITHUB", class_="bg-dark")
    ui.markdown("Click [Here](https://github.com/Moahhid/Cross-Era-Greatness.-A-Statistical-NBA-GOAT-comparison) to view my project on GitHub.")


with ui.nav_panel("Player Comparison graphics"):

    ui.input_checkbox_group(  
    "checkbox_group",  
    "Select player to compare:",  
    {  
        "Lebron James" : "LBJ" ,  
        "Michael Jordan" : "MJ" ,  
        "Kareem Abdul-Jabbar" : "KAJ" ,  
    },  )

    @render_plotly
    def relative_PER_plot():
        selected_players = input.checkbox_group()
        if not selected_players:
            return px.line(title="Please select at least one player to compare.")
        
        fig = px.line(title="Player Efficiency Rating (PER) Comparison")
        
        for player in selected_players:
            player_data = Players[player]
            fig.add_scatter(x=player_data["Season Number"], y=player_data["PER"], mode='lines+markers', name=player)
        
        fig.update_layout(xaxis_title="Season", yaxis_title="PER", legend_title="Player")
        return fig
    

with ui.nav_panel("Datasets"):
    ui.input_select(
        "select",
        "Select dataset:",
        {
            "Lebron James NBA statistics": "Lebron James",
            "Michael Jordan NBA statistics": "Michael Jordan",
            "Kareem Abdul-Jabbar NBA statistics": "Kareem Abdul-Jabbar",
            "NBA Average statistics": "NBA Average",
            "NBA Pace": "Pace",
        },
    )

    @render.text
    def val2():
        return f"{input.select()}"

    @render.data_frame
    def datasets():
        key = input.select()
        return render.DataGrid(DATA[key])
