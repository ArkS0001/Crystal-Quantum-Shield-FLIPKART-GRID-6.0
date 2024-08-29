import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the data from CSV file
log_file_path = 'request_log.csv'
df = pd.read_csv(log_file_path, names=['Request_ID', 'Status_Code', 'Elapsed_Time'], header=None)

# Create Dash application
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Request Metrics Dashboard"),
    dcc.Graph(id='request-rate'),
    dcc.Graph(id='status-code-over-time'),
    dcc.Graph(id='latency'),
    dcc.Graph(id='error-rate'),
    dcc.Graph(id='scrambled-tokens')
])

@app.callback(
    Output('request-rate', 'figure'),
    Output('status-code-over-time', 'figure'),
    Output('latency', 'figure'),
    Output('error-rate', 'figure'),
    Output('scrambled-tokens', 'figure'),
    [Input('request-rate', 'id')]
)
def update_graphs(_):
    # Request Rate
    request_rate = df.groupby('Status_Code').size().reset_index(name='Count')
    request_rate_fig = px.bar(request_rate, x='Status_Code', y='Count', title='Request Rate')

    # Status Code Over Time
    df['Timestamp'] = pd.to_datetime(df['Request_ID'])
    status_code_over_time = df.groupby(df['Timestamp'].dt.hour).size().reset_index(name='Count')
    status_code_over_time_fig = px.line(status_code_over_time, x='Timestamp', y='Count', title='Status Code Over Time')

    # Latency
    latency_fig = px.histogram(df, x='Elapsed_Time', title='Request Latency')

    # Error Rate
    error_rate = df[df['Status_Code'] == 503].shape[0] / df.shape[0]
    error_rate_fig = px.pie(values=[1 - error_rate, error_rate], names=['Success', 'Error'], title='Error Rate')

    # Correctly Scrambled Tokens
    # For demo purposes, we assume scrambled tokens are correctly counted
    # In practice, you'd need a separate CSV or metric for this
    scrambled_tokens_count = df['Status_Code'].value_counts().get(200, 0)
    scrambled_tokens_fig = go.Figure(data=[go.Pie(labels=['Scrambled Tokens'], values=[scrambled_tokens_count])])
    scrambled_tokens_fig.update_layout(title='Correctly Scrambled Tokens')

    return request_rate_fig, status_code_over_time_fig, latency_fig, error_rate_fig, scrambled_tokens_fig

if __name__ == '__main__':
    app.run_server(debug=True)



# import pandas as pd
# import plotly.express as px
# import dash
# from dash import dcc
# from dash import html
# from dash.dependencies import Input, Output

# # Load the data from CSV file
# log_file_path = 'request_log.csv'
# df = pd.read_csv(log_file_path, names=['Request_ID', 'Status_Code', 'Elapsed_Time'], header=None)

# # Ensure Elapsed_Time is numeric
# df['Elapsed_Time'] = pd.to_numeric(df['Elapsed_Time'], errors='coerce')

# # Simulate timestamps if not present; adjust as needed for actual timestamps
# df['Timestamp'] = pd.date_range(start='2023-01-01', periods=len(df), freq='T')

# # Create Dash application
# app = dash.Dash(__name__)

# app.layout = html.Div([
#     html.H1("Request Metrics Dashboard"),
#     dcc.Graph(id='request-rate'),
#     dcc.Graph(id='status-code-over-time'),
#     dcc.Graph(id='latency'),
#     dcc.Graph(id='error-rate'),
#     dcc.Graph(id='scrambled-tokens')
# ])

# @app.callback(
#     Output('request-rate', 'figure'),
#     Output('status-code-over-time', 'figure'),
#     Output('latency', 'figure'),
#     Output('error-rate', 'figure'),
#     Output('scrambled-tokens', 'figure'),
#     [Input('request-rate', 'id')]
# )
# def update_graphs(_):
#     # Request Rate
#     request_rate = df.groupby('Status_Code').size().reset_index(name='Count')
#     request_rate_fig = px.bar(request_rate, x='Status_Code', y='Count', title='Request Rate')

#     # Status Code Over Time
#     status_code_over_time = df.groupby(df['Timestamp'].dt.floor('H')).size().reset_index(name='Count')
#     status_code_over_time_fig = px.line(status_code_over_time, x='Timestamp', y='Count', title='Status Code Over Time')

#     # Latency
#     latency_fig = px.histogram(df, x='Elapsed_Time', title='Request Latency')

#     # Error Rate
#     error_rate = df[df['Status_Code'] == 503].shape[0] / df.shape[0]
#     error_rate_fig = px.pie(values=[1 - error_rate, error_rate], names=['Success', 'Error'], title='Error Rate')

#     # Correctly Scrambled Tokens
#     # For demo purposes, we assume scrambled tokens are correctly counted
#     # In practice, you'd need a separate CSV or metric for this
#     scrambled_tokens_count = df['Status_Code'].value_counts().get(200, 0)
#     scrambled_tokens_fig = go.Figure(data=[go.Pie(labels=['Scrambled Tokens'], values=[scrambled_tokens_count])])
#     scrambled_tokens_fig.update_layout(title='Correctly Scrambled Tokens')

#     return request_rate_fig, status_code_over_time_fig, latency_fig, error_rate_fig, scrambled_tokens_fig

# if __name__ == '__main__':
#     app.run_server(debug=True)





# from dash import dcc, html, Dash
# import plotly.graph_objects as go
# import pandas as pd
# from dash.dependencies import Output,Input

# app = Dash(__name__)
# app.config.suppress_callback_exceptions = True  # Suppress callback exceptions

# app.layout = html.Div([
#     dcc.Graph(id='request-rate'),
#     dcc.Graph(id='status-code-over-time'),
#     dcc.Graph(id='latency'),
#     dcc.Graph(id='error-rate'),
#     dcc.Graph(id='scrambled-tokens'),
#     dcc.Interval(
#         id='interval-component',
#         interval=1*1000,  # Refresh every second
#         n_intervals=0
#     )
# ])

# @app.callback(
#     [Output('request-rate', 'figure'),
#      Output('status-code-over-time', 'figure'),
#      Output('latency', 'figure'),
#      Output('error-rate', 'figure'),
#      Output('scrambled-tokens', 'figure')],
#     [Input('interval-component', 'n_intervals')]
# )
# def update_graphs(n_intervals):
#     # Dummy data for example
#     request_data = {'time': pd.date_range(start='1/1/2023', periods=100, freq='H'),
#                     'count': [i for i in range(100)]}
#     status_code_data = {'time': pd.date_range(start='1/1/2023', periods=100, freq='H'),
#                         'status_code_200': [i for i in range(50)],
#                         'status_code_503': [50 - i for i in range(50)]}
#     latency_data = {'time': pd.date_range(start='1/1/2023', periods=100, freq='H'),
#                     'latency': [i % 10 for i in range(100)]}
#     error_data = {'time': pd.date_range(start='1/1/2023', periods=100, freq='H'),
#                   'error_rate': [i % 5 for i in range(100)]}
#     scrambled_tokens_count = 123  # Dummy count

#     # Create figures
#     request_rate_fig = go.Figure(data=[go.Scatter(x=request_data['time'], y=request_data['count'], mode='lines+markers')])
#     status_code_fig = go.Figure(data=[
#         go.Scatter(x=status_code_data['time'], y=status_code_data['status_code_200'], mode='lines', name='200'),
#         go.Scatter(x=status_code_data['time'], y=status_code_data['status_code_503'], mode='lines', name='503')
#     ])
#     latency_fig = go.Figure(data=[go.Scatter(x=latency_data['time'], y=latency_data['latency'], mode='lines+markers')])
#     error_rate_fig = go.Figure(data=[go.Scatter(x=error_data['time'], y=error_data['error_rate'], mode='lines+markers')])
#     scrambled_tokens_fig = go.Figure(data=[go.Pie(labels=['Scrambled Tokens'], values=[scrambled_tokens_count])])

#     return request_rate_fig, status_code_fig, latency_fig, error_rate_fig, scrambled_tokens_fig

# if __name__ == '__main__':
#     app.run_server(debug=True)
