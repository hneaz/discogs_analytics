import os
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, callback, Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

# --- 1. DATA LOADING AND PREPROCESSING FUNCTION ---
def load_and_clean_data(file_path='output/discogs_clean_data.csv'):
    try:
        df = pd.read_csv(file_path)
        
        print("🔧 Standardizing column names...")
        print(df.head())
        print(df.columns)
        
        # Method: Clean each column name manually
        def clean_column_name(col):
            if isinstance(col, str):
                # Remove leading/trailing whitespace
                cleaned = col.strip()
                
                # Replace any non-alphanumeric characters with underscores (except in numbers)
                import re
                # Split by space or special chars, strip each part, join with underscore
                parts = re.split(r'[^\w]', cleaned)  # Split on non-word characters
                parts = [part.strip() for part in parts if part.strip()]  # Remove empty strings
                cleaned = '_'.join(parts)
                
                # Lowercase
                # cleaned = cleaned.lower()
                
                # Remove any multiple underscores
                cleaned = re.sub(r'_+', '_', cleaned)  # Replace multiple _ with single _
                
                return cleaned
            else:
                return col
        
        df.columns = [clean_column_name(col) for col in df.columns]
        
        print(f"✅ Columns standardized: {len(df.columns)} columns")
        print(f"📊 Standardized columns: {df.columns.tolist()}")
        
        # Continue with rest of cleaning logic...
        print(df.head())
        print(df.columns)
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        raise
    
    return df


# --- 2. MAIN APP SETUP ---
def get_summary_stats(df):
    """Get summary statistics for dashboard KPIs."""
    stats = {
        'total_spent': round(df['Collection_Cost'].sum() if 'Collection_Cost' in df.columns else 0, 2),
        'median_value': round(df['Median'].sum() if 'Median' in df.columns else 0, 2),
        'avg_cost_per_record': round(df['Collection_Cost'].mean(), 2) if len(df) > 0 and 'Collection_Cost' in df.columns else 0,
        'total_records': len(df),
        'unique_artists': df['Artist'].nunique() if 'Artist' in df.columns else 0,
    }
    return stats

# --- 3. LAYOUT COMPONENTS ---
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load Data
DATA_PATH = './output/discogs_clean_data.csv'
try:
    df = load_and_clean_data(DATA_PATH)
except Exception as e:
    print(f"❌ Data loading error: {e}")
    raise

stats = get_summary_stats(df)

print(f"\n✅ Dashboard ready with:")
print(f"   📈 Records: {stats['total_records']}")
print(f"   💰 Total Spent: ${stats['total_spent']}")
print(f"   👥 Unique Artists: {stats['unique_artists']}")

kpi_grid = dbc.Container([
    html.Div([
        html.H4("Collection Summary", className="text-center mb-2"),
        html.P(f"Total Records: {stats['total_records']}", style={'textAlign': 'center'}),
        html.P(f"Total Spent: ${stats['total_spent']}")
    ], style={'textAlign': 'center', 'padding': '1rem'}),
], fluid=False)

# Tab 1: Overview & Top Artists
tab1_content = html.Div([
    dcc.Graph(id='genre-distribution', 
              figure=px.pie(df[df['Genre'].notna()], values='Genre', names='Title', 
                            title='Genre Distribution').update_layout(yaxis={'categoryorder': 'total descending'})),
    dbc.Row([
        dbc.Col(html.H4("Top 10 Artists by Total Spending"), width=6),
        dbc.Col(html.P(f"{stats['unique_artists']} unique artists tracked"), width=6)
    ], align='center'),
    dcc.Graph(id='artist-cost-bar'),
])

# Tab 2: Financials & Value
tab2_content = html.Div([
    dcc.Graph(id='cost-vs-value-scatter', 
              figure=px.scatter(df[df['Collection_Cost'].notna()], x='Collection_Cost', y='Median', 
                               title='Cost vs Market Value')),
    dbc.Tabs([
        dbc.Tab(dcc.Graph(id='label-spending-chart'), label="🏷️ Labels"),
        dbc.Tab(dcc.Graph(id='format-breakdown'), label="💿 Formats")
    ])
])

# Tab 3: Distribution & Autographs
tab3_content = html.Div([
    dcc.Graph(id='subgenre-boxplot'),
    dcc.Graph(id='autograph-comparison')
])

# Tab 4: Time Series
tab4_content = html.Div([
    dcc.Graph(id='time-series-records', 
              figure=px.line(df.groupby('Released').size().reset_index(name='Count'), 
                            markers=True, title='Records by Release Year')),
])

app.layout = dbc.Container(
    [
        html.H1("Discogs Collection Dashboard", className="text-center mb-3"),
        kpi_grid,
        
        dbc.Tabs([
            dbc.Tab(label="📊 Overview", id="tab-overview", children=tab1_content),
            dbc.Tab(label="💰 Financials & Value", id="tab-financial", children=tab2_content),
            dbc.Tab(label="🔍 Distribution", id="tab-dist", children=tab3_content),
            dbc.Tab(label="⏱️ Time Series", id="tab-time", children=tab4_content),
        ], id='my-tabs', active_tab="tab-overview")
    ], fluid=True, className="p-2")

# --- 4. CALLBACKS (UPDATED for Dash 2.x) ---

@callback(
    Output('artist-cost-bar', 'figure'),
    [Input('my-tabs', 'active_tab')],
    prevent_initial_call=False
)
def update_artist_chart(active_tab):
    if 'Artist' in df.columns:
        artist_data = df.groupby('Artist').agg({
            'Title': lambda x: x.notna().sum(),
            'Collection_Cost': 'sum'
        }).reset_index().sort_values(['Collection_Cost', 'Artist'], ascending=[False, True])
        
        top_10_artists = artist_data.head(10)
        
        fig = px.bar(top_10_artists, x='Artist', y='Collection_Cost', 
                     title="Top 10 Artists by Total Spending", 
                     labels={'Collection_Cost': 'Total Spend ($)', 'Title': 'Records'})
        return fig
    else:
        return go.Figure()

@callback(
    Output('label-spending-chart', 'figure'),
    [Input('my-tabs', 'active_tab')],
    prevent_initial_call=False
)
def update_label_chart(active_tab):
    if 'Label' in df.columns:
        label_data = df.groupby(['Label']).agg({
            'Title': 'count',
            'Collection_Cost': 'sum'
        }).reset_index().sort_values(by='Collection_Cost', ascending=False)
        
        top_labels = label_data.head(10)
        fig = px.bar(top_labels, x='Label', y='Collection_Cost', 
                     title="Top Labels by Spending", labels={'Title': 'Spend ($)'})
    else:
        # Fallback if Label column missing
        fig = go.Figure()
        fig.add_annotation(text="No Label data available")
    
    return fig

@callback(
    Output('format-breakdown', 'figure'),
    [Input('my-tabs', 'active_tab')],
    prevent_initial_call=False
)
def update_format_chart(active_tab):
    format_data = df[df['CollectionFolder'].notna()].groupby(['CollectionFolder']).size().reset_index(name='Count')
    fig = px.pie(format_data, values='Count', names='CollectionFolder', 
                 title="Format Breakdown", hole=0.4)
    return fig

@callback(
    Output('subgenre-boxplot', 'figure'),
    [Input('my-tabs', 'active_tab')],
    prevent_initial_call=False
)
def update_subgenre_boxplot(active_tab):
    filtered_df = df[(df['Collection_Cost'] < 200) & (df['Subgenre'].notna())]
    
    fig = px.box(filtered_df, x='Subgenre', y='Collection_Cost', 
                 title="Cost Distribution by Subgenre", 
                 points='all')
    return fig

@callback(
    Output('autograph-comparison', 'figure'),
    [Input('my-tabs', 'active_tab')],
    prevent_initial_call=False
)
def update_autograph_chart(active_tab):
    df_copy = df[['Collection_Cost', 'Collection_Autographed']].copy()
    
    fig = px.box(df_copy, x='Collection_Autographed', y='Collection_Cost', 
                 title="Autographed vs Non-Autographed Cost",
                 labels={'Collection_Cost': '$'})
    return fig

# Run the app
if __name__ == '__main__':
    port = 8050
    debug = True
    
    try:
        print(f"\n🚀 Starting Discogs Dashboard on http://127.0.0.1:{port}")
        app.run(debug=debug, port=port)
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        raise e
