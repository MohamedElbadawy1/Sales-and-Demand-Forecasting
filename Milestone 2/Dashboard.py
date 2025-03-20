# ::::::::::::::::::::::::::::::::::::::::::::::: Libraries :::::::::::::::::::::::::::::::::::::::::::::::

import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, Input, Output, callback

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"]

# :::::::::::::::::::::::::::::::::::::::::::::: Loading Data :::::::::::::::::::::::::::::::::::::::::::::
main_data = "D:/depi/New folder/Sales-and-Demand-Forecasting/Data/Data After Milestone 1.csv"
original_data = "D:/depi/New folder/Sales-and-Demand-Forecasting/Data/Original Data.csv"
sales = pd.read_csv(main_data, encoding="latin-1")
main = pd.read_csv(original_data, encoding="latin-1")

# ::::::::::::::::::::::::::::::::::::::::::::::: Variables :::::::::::::::::::::::::::::::::::::::::::::::
root = {
    "text" : "#94d5f7",
    "text2" : "#007bff",
    "text3" : "#e8f5fc",
    "background1" : "#070e12",
    "background2" : "#333333",
    "primary" : "#9ebfd6",
    "secondary" : "#9ebfd6",
    "accent" : "#2ea2dc"
}

total_revenue = sales["Total_sales"].sum().round(2)
total_profit = sales["Profit"].sum().round(2)
total_units_sold = sales["Quantity"].sum().round(2)
avg_discount = (main["Discount"].mean() * 100).round(2)
total_orders = sales["Order Date"].count()
avg_shipping_time = sales["Shipping Time (Days)"].mean().round(2)

fig1_DataPickerRange = dcc.DatePickerRange(
                            id='fig1_DataPickerRange',
                            start_date=sales['Order Date'].min(),
                            end_date=sales['Order Date'].max(),
                            display_format='YYYY-MM-DD', 
                            className="fig1_DataPickerRange"
                        )
fig1_Dropdown = dcc.Dropdown(
                    id='fig1_Dropdown',
                    options=[
                        {'label': 'Sales', 'value': 'Sales'},
                        {'label': 'Profit', 'value': 'Profit'}
                    ],
                    value='Sales', 
                    className="fig1_Dropdown"
                )
fig1_Slider = dcc.Slider(
                id='fig1_Slider',
                min=7,
                max=30,
                step=7,
                marks={7: '7D', 14: '14D', 30: '30D'},
                value=7,
                className="fig1_Slider"
            )
fig1 = dcc.Graph(id='fig1', className="fig1")
region_dropdown = dcc.Dropdown(
    id="region_dropdown",
    options=[
        {"label": "Region", "value": "Region"},
        {"label": "Market", "value": "Market"},
    ],
    value="Region",  # Default selection
    className="region_dropdown"
)

sales_profit_toggle = dcc.RadioItems(
    id="sales_profit_toggle",
    options=[
        {"label": "Sales", "value": "Total_sales"},
        {"label": "Profit", "value": "Profit"},
    ],
    value="Total_sales",
    className="sales_profit_toggle",
    inline=True
)

fig2 = dcc.Graph(id="fig2", className="fig2")


# ::::::::::::::::::::::::::::::::::::::::::::::: Functions :::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::: App Layout ::::::::::::::::::::::::::::::::::::::::::::::
app = Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    html.H1("Sales Dashboard", className="title"),
    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Revenue" , className = "s_h3"),
                html.H2([html.Span("$"), f"{total_revenue}"])
            ], className="summary_div"),
            html.Div([
                html.H3("Total Profit" , className = "s_h3"),
                html.H2([html.Span("$"), f"{total_profit}"])
            ], className="summary_div"),
            html.Div([
                html.H3("Total Units Sold" , className = "s_h3"),
                html.H2([html.Span("$"), f"{total_units_sold}"])
            ], className="summary_div"),
        ], className="mini_container"),
        html.Div([
            html.Div([
                html.H3("Average Discount" , className = "s_h3"),
                html.H2([html.Span("%"), f"{avg_discount}"])
            ], className="summary_div"),
            html.Div([
                html.H3("Total Orders" , className = "s_h3"),
                html.H2([f"{total_orders}", html.Span("order")])
            ], className="summary_div"),
            html.Div([
                html.H3("Average Shipping Time" , className = "s_h3"),
                html.H2([f"{avg_shipping_time}", html.Span("days")])
            ], className="summary_div")
        ], className="mini_container")
    ], id="first_row"),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Div([
        html.Div([
            html.Div([
                html.H2("Sales & Profit Over Time"),
                html.Div([fig1_DataPickerRange, fig1_Dropdown], className="fig1_mini_div"),
                fig1_Slider,
                fig1
            ], id="first_column"),

            html.Div([
                html.H2("Sales by Region or Market"),
                html.Div([region_dropdown, sales_profit_toggle], className="fig2_controls"),
                fig2
            ], id="secound_column_new")
        ], id="secound_row_new"),
        html.Div([
            html.H2("Sales by Region or Market")
        ], id="secound_column")
    ], id="secound_row")
], id="body")

# :::::::::::::::::::::::::::::::::::::::::::::: Callbacks ::::::::::::::::::::::::::::::::::::::::::::::
@callback(
    Output('fig1', 'figure'),
    [Input('fig1_DataPickerRange', 'start_date'),
    Input('fig1_DataPickerRange', 'end_date'),
    Input('fig1_Slider', 'value'),
    Input('fig1_Dropdown', 'value')]
)
def update_graph(start_date, end_date, ma_window, measure):
    filtered_df = sales[(sales['Order Date'] >= start_date) & (sales['Order Date'] <= end_date)]
    filtered_df = filtered_df.sort_values('Order Date')
    filtered_df['Moving_Avg'] = filtered_df[measure].rolling(window=ma_window).mean()
    
    fig1 = px.line(filtered_df, x='Order Date', y='Moving_Avg', title=f'{measure} Over Time')

    fig1.update_layout(
        plot_bgcolor = root['background1'],
        paper_bgcolor = root['background2'],
        font_color = root['text'],
        xaxis_title='Order Date',
        yaxis_title=measure,
        template='plotly_dark',
        hovermode='x unified',
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig1


@callback(
    Output("fig2", "figure"),
    [Input("region_dropdown", "value"), Input("sales_profit_toggle", "value")]
)
def update_sales_by_region(selected_category, selected_metric):
    # Grouping Data
    grouped_df = sales.groupby(selected_category)[selected_metric].sum().reset_index()

    # Creating the Bar Chart
    fig2 = px.bar(grouped_df, x=selected_category, y=selected_metric,
                  title=f"{selected_metric} by {selected_category}",
                  color=selected_category, text_auto=True)

    # Updating Style
    fig2.update_layout(
        plot_bgcolor=root["background1"],
        paper_bgcolor=root["background2"],
        font_color=root["text"],
        xaxis_title=selected_category,
        yaxis_title=selected_metric,
        template="plotly_dark",
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return fig2


# ::::::::::::::::::::::::::::::::::::::::::::::: Run App :::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == "__main__":
    app.run(debug=True)