# ::::::::::::::::::::::::::::::::::::::::::::::: Libraries :::::::::::::::::::::::::::::::::::::::::::::::

import numpy as np
import pandas as pd
import plotly.express as px
from dash import dcc, html, Dash, Input, Output, callback

external_stylesheets = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css"]

# :::::::::::::::::::::::::::::::::::::::::::::: Loading Data :::::::::::::::::::::::::::::::::::::::::::::
main_data = "Data/Data After Milestone 1.csv"
original_data = "Data/Original Data.csv"
sales = pd.read_csv(main_data, encoding="latin-1")
main = pd.read_csv(original_data, encoding="latin-1")

# ::::::::::::::::::::::::::::::::::::::::::::::: Variables :::::::::::::::::::::::::::::::::::::::::::::::
root = {
    "text"        : "#94d5f7",
    "text2"       : "#007bff",
    "text3"       : "#e8f5fc",
    "background1" : "#070e12",
    "background2" : "#333333",
    "primary"     : "#9ebfd6",
    "secondary"   : "#9ebfd6",
    "accent"      : "#2ea2dc"
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

fig2_Dropdown = dcc.Dropdown(
    id="fig2_Dropdown",
    options=[
        {"label": "Region", "value": "Region"},
        {"label": "Market", "value": "Market"},
        {"label": "Country", "value": "Country"}
    ],
    value="Region",  # Default selection
    className="fig2_Dropdown"
)
fig2_Radioitems = dcc.RadioItems(
    id="fig2_Radioitems",
    options=[
        {"label": "Sales", "value": "Total_sales"},
        {"label": "Profit", "value": "Profit"},
    ],
    value="Total_sales",
    className="fig2_Radioitems",
    inline=True
)
fig2 = dcc.Graph(id="fig2", className="fig2")

fig3_Dropdown1 = dcc.Dropdown(
    id='fig3_Dropdown1',
    options=[
        {'label': 'Horizontal Bar Chart', 'value': 'bar'},
        {'label': 'Treemap', 'value': 'treemap'}
    ],
    value='bar',
    clearable=False,
    className='fig3_Dropdown1'
)
fig3_DropDown = dcc.Dropdown(
    id= 'fig3_DropDown',
    options=[
        {'label':'Sales' ,'value':'Sales'},
        {'label':'Profit' ,'value':'Profit'},
        {'label':'Quantity' ,'value':'Quantity'}
    ],
    value='Sales',
    className='fig3_Dropdown'
)
fig3_checkList = dcc.Checklist(
    id='fig3_checkList',
    options=[{'label': cat, 'value': cat} for cat in sales['Category'].unique()],
    value=["Technology", "Furniture", "Office Supplies"],
    className='fig3_checkList',
    inputStyle={"margin-right": "5px", "margin-left": "5px"},
    labelStyle={"display": "block"}
)
fig3 = dcc.Graph(id='fig3', className="fig3")

# ::::::::::::::::::::::::::::::::::::::::::::::: Functions :::::::::::::::::::::::::::::::::::::::::::::::


# ::::::::::::::::::::::::::::::::::::::::::::::: App Layout ::::::::::::::::::::::::::::::::::::::::::::::
app = Dash(__name__, external_stylesheets = external_stylesheets)

app.layout = html.Div([
    html.H1("Sales Dashboard", className="title"),
    html.Div([
        html.Div([
            html.Div([
                html.H3("Total Revenue", className="s_h3"),
                html.H2([html.Span("$"), f"{total_revenue}"])
            ], className="summary_div"),
            html.Div([
                html.H3("Total Profit", className="s_h3"),
                html.H2([html.Span("$"), f"{total_profit}"])
            ], className="summary_div"),
            html.Div([
                html.H3("Total Units Sold", className="s_h3"),
                html.H2([html.Span("$"), f"{total_units_sold}"])
            ], className="summary_div"),
        ], className="mini_container"),
        html.Div([
            html.Div([
                html.H3("Average Discount", className="s_h3"),
                html.H2([html.Span("%"), f"{avg_discount}"])
            ], className="summary_div"),
            html.Div([
                html.H3("Total Orders", className="s_h3"),
                html.H2([f"{total_orders}", html.Span("order")])
            ], className="summary_div"),
            html.Div([
                html.H3("Average Shipping Time", className="s_h3"),
                html.H2([f"{avg_shipping_time}", html.Span("days")])
            ], className="summary_div")
        ], className="mini_container")
    ], id="first_row"),
    html.Br(),
    html.Hr(),
    html.Br(),
    html.Div([
        html.Div([
            html.H2("Sales & Profit Over Time"),
            html.Div([
                fig1_DataPickerRange,
                fig1_Dropdown
            ], className="fig1_mini_div"),
            fig1_Slider,
            fig1
        ], className="first_column"),
        html.Div([
            html.H2("Sales by Region or Market"),
            html.Div([
                fig2_Dropdown, 
                fig2_Radioitems
            ], className="fig2_mini_div"),
            fig2
        ], className="second_column")
    ], id="second_row"),
    html.Br(),
    html.Br(),
    html.Div([
        html.Div([
            html.H2("Top Performing Products and Categories"),
            html.Div([
                fig3_Dropdown1,
                fig3_DropDown
            ], className="fig3_mini_div"),
            fig3_checkList,
            fig3
        ], className="first_column"),
        html.Div([

        ], className="second_column")
    ], id="third_row")
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
    [Input("fig2_Dropdown", "value"), 
    Input("fig2_Radioitems", "value")]
)
def update_sales_by_region(selected_category, selected_metric):
    if selected_category == "Country":
        # Create a Choropleth Map when 'Country' is selected
        grouped_df = sales.groupby("Country")[selected_metric].sum().reset_index()

        fig2 = px.choropleth(
            grouped_df,
            locations="Country",
            locationmode="country names",
            color=selected_metric,
            title=f"{selected_metric} by Country",
            color_continuous_scale="viridis"  # Change to 'viridis' or other themes if needed
        )
    else:
        # Create a Bar Chart for Region or Market
        grouped_df = sales.groupby(selected_category)[selected_metric].sum().reset_index()

        fig2 = px.bar(
            grouped_df,
            x=selected_category,
            y=selected_metric,
            title=f"{selected_metric} by {selected_category}",
            color=selected_category,
            text_auto=True
        )
    # Apply the same dashboard styling
    fig2.update_layout(
        plot_bgcolor=root["background1"],
        paper_bgcolor=root["background2"],
        font_color=root["text"],
        xaxis_title=selected_category if selected_category != "Country" else "Country",
        yaxis_title=selected_metric,
        template="plotly_dark",
        title_x=0.5,
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig2

@callback(
    Output("fig3", "figure"),
    [
        Input("fig3_Dropdown1", "value"),
        Input("fig3_DropDown", "value"),
        Input("fig3_checkList", "value")
    ]
)
def update_graph3(chart_type, measure, selected_categories):
    # Filter data to selected categories
    filtered_df = sales[sales['Category'].isin(selected_categories)]

    # Group by Category and Sub-Category
    grouped_df = filtered_df.groupby(['Category', 'Sub-Category'])[measure].sum().reset_index()

    # Create the chart
    if chart_type == 'treemap':
        fig = px.treemap(
            grouped_df,
            path=['Category', 'Sub-Category'],
            values=measure,
            color=measure,
            title=f'{measure} by Category and Sub-Category'
        )
    else:
        fig = px.bar(
            grouped_df,
            x=measure,
            y='Sub-Category',
            orientation='h',
            color='Category',
            text_auto=True,
            title=f'{measure} by Category and Sub-Category'
        )

    fig.update_layout(
        plot_bgcolor=root['background1'],
        paper_bgcolor=root['background2'],
        font_color=root['text'],
        template='plotly_dark',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    
    return fig

# ::::::::::::::::::::::::::::::::::::::::::::::: Run App :::::::::::::::::::::::::::::::::::::::::::::::
if __name__ == "__main__":
    app.run(debug=True)