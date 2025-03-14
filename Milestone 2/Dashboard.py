import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"]

data_path = "Data/Data After Milestone 1.csv"
sales = pd.read_csv(data_path, encoding="latin-1")

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1("Sales Dashboard", className="title"),
    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Revenue" , className = "s_h3"),
                html.P()
            ], className="summary_div"),
            html.Div([
                html.H3("Total Profit" , className = "s_h3"),
                html.P()
            ], className="summary_div"),
            html.Div([
                html.H3("Total Units Sold" , className = "s_h3"),
                html.P()
            ], className="summary_div"),
        ], className="mini_container"),
        html.Div([
            html.Div([
                html.H3("Average Discount" , className = "s_h3"),
                html.P()
            ], className="summary_div"),
            html.Div([
                html.H3("Total Orders" , className = "s_h3"),
                html.P()
            ], className="summary_div"),
            html.Div([
                html.H3("Average Shipping Time" , className = "s_h3"),
                html.P()
            ], className="summary_div")
        ], className="mini_container")
    ], id="summary_container")
], id="body")

if __name__ == "__main__":
    app.run(debug=True)
