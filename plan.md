# Plotly Dash App Plan: Discogs Collection Analytics

## Goal
Build an interactive Plotly Dash web application that visualizes Discogs collection data with the 13 key analytical sections extracted from the Python script, enabling users to filter, explore, and export insights about their record collection.

## Current Context / Assumptions
- **Data source**: CSV file at `data/discogs_data.csv` (raw) or `output/discogs_clean_data.csv` (processed)
- **Existing code**: `src/discogs_analysis.py` contains the analysis logic (1365 lines, Jupyter-style notebook converted to script)
- **Dependencies**: pandas, numpy, matplotlib, seaborn, plotly, ydata-profiling (from `requirements.txt`)
- **Target audience**: Collection owners who want to explore their data interactively without running Python notebooks
- **User experience goal**: Zero-context implementation - someone reading this plan should be able to build it without prior knowledge of the codebase

## Architecture / Proposed Approach

**Backend**: Single Dash `Dash` app with modular callback functions organized by section. Data loading happens at startup with caching via `dash_cache_data` or `json` module to avoid re-reading CSV on each refresh.

**Frontend**: Dash `html.Div` and `dash_core_components` layout with a sidebar navigation (tabs) for each of the 13 sections, a main content area with dynamic plots, and a shared header with global filters (artist, genre, subgenre, year, price range).

**Data pipeline**: 
1. Load CSV at app startup → store in global `df` variable
2. Pre-aggregate key metrics in background (top artists, label counts, genre distribution) using `df.groupby().agg()` 
3. Expose these aggregates as Dash `dcc.Store` data for quick access in callbacks
4. Use `dash.dependencies.callback` with `Input` parameters for filters, `Output` for plot updates

**Plot strategy**: Reuse existing plot code from `discogs_analysis.py` but convert Matplotlib figures to Plotly objects where possible. For quick wins, use Dash's built-in `dcc.Graph` with Plotly JSON specs. Complex 3D/animation plots may need to render as static HTML or use `plotly.express` directly.

## Step-by-Step Tasks

### Task 1: Project Setup (5 minutes)
**File**: `app.py`
```python
import dash
from dash import html, dcc, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Initialize app
app = dash.Dash(__name__, title='Discogs Collection Analytics')
app.layout = html.Div([
    html.H1('Discogs Collection Analytics', style={'textAlign': 'center'}),
    html.Div(id='placeholder')
])

# Global data loading (to be implemented)
df = None
```
**Command**: `python app.py`
**Expected**: App runs on `http://127.0.0.1:8050/` (or configured port)

### Task 2: Add Sidebar Navigation (10 minutes)
**File**: `app.py`
**Add to `app.layout`**:
```python
sidebar = html.Div([
    html.Ul([
        html.Li(html.A('Profile', id='nav-profile', className='nav-item')),
        html.Li(html.A('Most/Least Expensive', id='nav-expensive', className='nav-item')),
        html.Li(html.A('Top Artists', id='nav-artists', className='nav-item')),
        html.Li(html.A('Labels', id='nav-labels', className='nav-item')),
        html.Li(html.A('Time Series', id='nav-time', className='nav-item')),
        html.Li(html.A('Formats', id='nav-formats', className='nav-item')),
        html.Li(html.A('Autographed', id='nav-auto', className='nav-item')),
        html.Li(html.A('Genres', id='nav-genres', className='nav-item')),
        html.Li(html.A('Subgenres', id='nav-subgenres', className='nav-item')),
    ])
], style={'width': '250px', 'height': '100vh', 'background': '#f8f9fa', 'padding': '10px'})

main_content = html.Div(id='content-area', style={'flex': '1', 'padding': '20px'})

app.layout = html.Div([
    html.H1('Discogs Collection Analytics', style={'textAlign': 'center'}),
    dcc.Tabs(id='tabs', value='profile', children=[
        dcc.Tab(label='Profile', value='profile', id='tab-profile'),
        dcc.Tab(label='Most/Least Expensive', value='expensive', id='tab-expensive'),
        dcc.Tab(label='Top Artists', value='artists', id='tab-artists'),
        dcc.Tab(label='Labels', value='labels', id='tab-labels'),
        dcc.Tab(label='Time Series', value='time', id='tab-time'),
        dcc.Tab(label='Formats', value='formats', id='tab-formats'),
        dcc.Tab(label='Autographed', value='auto', id='tab-auto'),
        dcc.Tab(label='Genres', value='genres', id='tab-genres'),
        dcc.Tab(label='Subgenres', value='subgenres', id='tab-subgenres'),
    ]),
    html.Div([
        sidebar,
        html.Div([
            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
            dcc.Store(id='data-store')
        ], style={'display': 'flex', 'flexDirection': 'row', 'height': '100%'})
    ])
])
```

### Task 3: Add Global Filters (10 minutes)
**File**: `app.py`
**Add to main content area**:
```python
filters = html.Div([
    html.Label('Artist Filter:'),
    dcc.Dropdown(id='filter-artist', options=[], value=None, placeholder='Select all'),
    html.Label('Genre Filter:'),
    dcc.Dropdown(id='filter-genre', options=[], value=None, placeholder='Select all'),
    html.Label('Subgenre Filter:'),
    dcc.Dropdown(id='filter-subgenre', options=[], value=None, placeholder='Select all'),
    html.Label('Min Price:'),
    dcc.Input(id='min-price', type='number', value=None, placeholder='0'),
    html.Label('Max Price:'),
    dcc.Input(id='max-price', type='number', value=None, placeholder='1000'),
    html.Button('Apply Filters', id='btn-filter'),
])

# Update app.layout to include filters before page-content
```

### Task 4: Task 4a: Profile Section - Load Data and Show Aggregates (15 minutes)
**File**: `app.py`
**Add callbacks**:
```python
@callback(Output('data-store', 'data'),
          [Input('btn-filter', 'n_clicks')])
def load_data(n_clicks):
    """Load CSV and compute aggregates at startup."""
    import pandas as pd
    
    if n_clicks is not None and n_clicks > 0:
        # Load cleaned data
        df = pd.read_csv('output/discogs_clean_data.csv')
        
        # Compute aggregates
        profile_summary = {
            'total_records': len(df),
            'unique_artists': len(df['Artist2'].unique()),
            'distinct_albums': len(df['Title'].unique()),
            'top_artists': df.groupby('Artist2').size().nlargest(5).to_dict(),
            'format_breakdown': df['Format'].value_counts().to_dict(),
            'genre_distribution': df['Genre'].value_counts().to_dict(),
            'subgenre_distribution': df['Subgenre'].value_counts().to_dict(),
            'avg_price': df['Collection_Cost'].mean()
        }
        
        return profile_summary
    
    return None

@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'profile':
        return html.Div([
            html.H2('Collection Profile'),
            html.P(f"Total Records: {html.Span(id='profile-total', children='Loading...')}", className='text-muted'),
            html.P(f"Unique Artists: {html.Span(id='profile-artists', children='Loading...')}", className='text-muted'),
            html.P(f"Distinct Albums: {html.Span(id='profile-albums', children='Loading...')}", className='text-muted'),
            dcc.Graph(id='genre-pie'),
            dcc.Graph(id='format-pie'),
        ])
```

### Task 5: Task 5a: Most/Least Expensive Section (15 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'expensive':
        return html.Div([
            html.H2('Most/Least Expensive Records'),
            html.H3('Most Expensive'),
            dcc.Graph(id='most-expensive-bar'),
            html.H3('Least Expensive'),
            dcc.Graph(id='least-expensive-bar'),
        ])

@callback(Output('most-expensive-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_most_expensive(data, n_clicks):
    df = data  # data is the loaded df from Task 4
    # Top 10 by max value
    top10 = df.nlargest(10, '_Max_')
    fig = px.bar(top10, x='Record', y='_Max_', title='Top 10 Most Valuable Records')
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig

@callback(Output('least-expensive-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_least_expensive(data, n_clicks):
    df = data
    # Free or cheapest
    free = df[df['Collection_Cost'] == 0]
    if len(free) == 0:
        cheapest = df.nsmallest(1, 'Collection_Cost')
        fig = px.bar(cheapest, x='Record', y='Collection_Cost', title='Cheapest Purchase')
    else:
        fig = px.bar(free, x='Record', y='Collection_Cost', title='Free Records')
    return fig
```

### Task 6: Task 6a: Top Artists Section (15 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'artists':
        return html.Div([
            html.H2('Top Artists by Spending'),
            dcc.Graph(id='artist-spending-bar'),
            dcc.Graph(id='artist-count-bar'),
        ])

@callback(Output('artist-spending-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_artist_spending(data, n_clicks):
    df = data
    # Group by artist2, sum costs
    artist_agg = df.groupby('Artist2').agg({
        'Title': 'count',
        'Collection_Cost': 'sum',
        '_Max_': 'sum',
        '_Median_': 'sum'
    }).reset_index()
    artist_agg = artist_agg.nlargest(10, 'Collection_Cost')
    fig = px.bar(artist_agg, x='Artist2', y='Collection_Cost', title='Top 10 Artists by Total Spending')
    fig.update_layout(xaxis={'categoryorder': 'total descending'})
    return fig
```

### Task 7: Task 7a: Labels Section (10 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'labels':
        return html.Div([
            html.H2('Record Label Analysis'),
            dcc.Graph(id='label-count-bar'),
            dcc.Graph(id='label-spending-bar'),
        ])

@callback(Output('label-count-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_label_count(data, n_clicks):
    df = data
    label_counts = df['Label'].value_counts().head(10)
    fig = px.bar(label_counts, x=label_counts.index, y=label_counts.values, title='Top 10 Labels by Count')
    return fig

@callback(Output('label-spending-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_label_spending(data, n_clicks):
    df = data
    label_agg = df.groupby('Label').agg({
        'Title': 'count',
        'Collection_Cost': 'sum'
    }).reset_index()
    label_agg = label_agg.nlargest(10, 'Collection_Cost')
    fig = px.bar(label_agg, x='Label', y='Collection_Cost', title='Top 10 Labels by Spending')
    return fig
```

### Task 8: Task 8a: Time Series Section (15 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'time':
        return html.Div([
            html.H2('Time Series Analysis'),
            html.P('Track collection additions and spending over time.'),
            dcc.Graph(id='yearly-additions-bar'),
            dcc.Graph(id='yearly-spending-bar'),
            dcc.Graph(id='yearly-value-bar'),
        ])

@callback(Output('yearly-additions-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_yearly_additions(data, n_clicks):
    df = data
    df['Date_Added'] = pd.to_datetime(df['Date_Added'])
    yearly = df.groupby('Date_Added').size().reset_index(name='count')
    fig = px.bar(yearly, x='Date_Added', y='count', title='Records Added by Date')
    return fig

@callback(Output('yearly-spending-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_yearly_spending(data, n_clicks):
    df = data
    df['Date_Added'] = pd.to_datetime(df['Date_Added'])
    yearly = df.groupby('Date_Added').agg({
        'Collection_Cost': 'sum',
        'Title': 'count'
    }).reset_index()
    yearly.columns = ['Date_Added', 'Spending', 'Count']
    fig = px.bar(yearly, x='Date_Added', y='Spending', title='Total Spending by Year')
    return fig
```

### Task 9: Task 9a: Formats Section (15 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'formats':
        return html.Div([
            html.H2('Format Analysis'),
            html.P('Compare vinyl, CD, and tape formats.'),
            dcc.Graph(id='format-distribution-dist'),
            html.P('Distribution of costs by format.'),
            dcc.Graph(id='format-boxplot'),
        ])

@callback(Output('format-distribution-dist', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_format_distribution(data, n_clicks):
    df = data
    fig = px.histogram(df, x='Collection_Cost', color='Format', 
                       title='Cost Distribution by Format', bins=50)
    return fig

@callback(Output('format-boxplot', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_format_boxplot(data, n_clicks):
    df = data
    fig = px.box(df, x='Format', y='Collection_Cost', 
                 title='Cost Boxplots by Format')
    return fig
```

### Task 10: Task 10a: Autographed Section (15 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'auto':
        return html.Div([
            html.H2('Autographed Records Analysis'),
            html.P('Compare autographed vs non-autographed items.'),
            dcc.Graph(id='autograph-distribution-dist'),
            dcc.Graph(id='autograph-boxplot'),
        ])

@callback(Output('autograph-distribution-dist', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_autograph_distribution(data, n_clicks):
    df = data
    fig = px.histogram(df, x='Collection_Cost', color='Collection_Autographed',
                       title='Cost Distribution by Autograph Status', bins=50)
    return fig

@callback(Output('autograph-boxplot', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_autograph_boxplot(data, n_clicks):
    df = data
    fig = px.box(df, x='Collection_Autographed', y='Collection_Cost',
                 title='Cost Boxplots by Autograph Status')
    return fig
```

### Task 11: Task 11a: Genres Section (20 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'genres':
        return html.Div([
            html.H2('Genre Analysis'),
            html.P('Boxplots comparing costs across genres.'),
            dcc.Graph(id='genre-boxplot-cost'),
            dcc.Graph(id='genre-boxplot-min'),
            dcc.Graph(id='genre-boxplot-median'),
            dcc.Graph(id='genre-boxplot-max'),
        ])

@callback(Output('genre-boxplot-cost', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_genre_boxplot_cost(data, n_clicks):
    df = data
    fig = px.box(df, x='Genre', y='Collection_Cost',
                 title='Cost Boxplots by Genre')
    return fig

@callback(Output('genre-boxplot-min', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_genre_boxplot_min(data, n_clicks):
    df = data
    fig = px.box(df, x='Genre', y='_Min_',
                 title='Min Value Boxplots by Genre')
    return fig

@callback(Output('genre-boxplot-median', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_genre_boxplot_median(data, n_clicks):
    df = data
    fig = px.box(df, x='Genre', y='_Median_',
                 title='Median Value Boxplots by Genre')
    return fig

@callback(Output('genre-boxplot-max', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_genre_boxplot_max(data, n_clicks):
    df = data
    fig = px.box(df, x='Genre', y='_Max_',
                 title='Max Value Boxplots by Genre')
    return fig
```

### Task 12: Task 12a: Subgenres Section (30 minutes)
**File**: `app.py`
```python
@callback(Output('page-content', 'children'),
          [Input('tabs', 'value')])
def display_content(tab):
    if tab == 'subgenres':
        return html.Div([
            html.H2('Subgenre Analysis'),
            html.P('Detailed breakdown by subgenre.'),
            dcc.Graph(id='subgenre-3d-scatter'),
            dcc.Graph(id='subgenre-cumulative-bar'),
            dcc.Graph(id='subgenre-pairplot'),
        ])

@callback(Output('subgenre-3d-scatter', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_subgenre_3d(data, n_clicks):
    # Filter for cheaper items first (matching original script)
    df = data[data['Collection_Cost'] < 200]
    fig = px.scatter_3d(df, x='Collection_Cost', y='_Median_', z='_Max_', 
                        color='Subgenre', title='3D Scatter: Cost vs Median vs Max')
    return fig

@callback(Output('subgenre-cumulative-bar', 'figure'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def show_subgenre_cumulative(data, n_clicks):
    df = data[data['Collection_Cost'] < 200]
    # Group by year and subgenre
    yearly_sub = df.groupby(['Released', 'Subgenre']).agg({
        'Title': 'count',
        'Collection_Cost': 'sum'
    }).reset_index()
    yearly_sub = yearly_sub.groupby('Subgenre').cumsum().reset_index()
    fig = px.bar(yearly_sub, x='Collection_Cost', y='Released', color='Subgenre',
                 orientation='h', title='Cumulative Spending by Subgenre Over Years')
    return fig
```

### Task 13: Task 13a: Data Export Feature (10 minutes)
**File**: `app.py`
```python
@callback(Output('btn-export', 'n_clicks'),
          [Input('btn-download', 'n_clicks')])
def handle_download(btn_clicks):
    # Simple file download
    pass

@callback(Output('download-link', 'children'),
          [Input('data-store', 'data'), Input('btn-filter', 'n_clicks')])
def setup_download(data, n_clicks):
    if data is not None:
        return html.A('Download Data (CSV)', href='#',
                      download=True,
                      id='download-btn')
    return None
```

## Tests / Validation

### Test 1: App Startup (5 minutes)
**Test**: App loads without errors
```bash
cd /Users/A4Q6026/Documents/discogs_analytics
python app.py
```
**Expected output**: Server starts on configured port with no tracebacks

### Test 2: Profile Section Data Load (5 minutes)
**Test**: Profile section shows correct aggregates
**Steps**:
1. Navigate to "Profile" tab
2. Verify "Total Records" displays a number > 0
3. Verify "Unique Artists" displays a number > 0
4. Verify genre pie chart renders
5. Verify format pie chart renders

**Expected**: All metrics match `discogs_clean_data.csv` row counts

### Test 3: Most/Least Expensive Charts (5 minutes)
**Test**: Charts display top 10 and bottom records correctly
**Steps**:
1. Navigate to "Most/Least Expensive" tab
2. Verify bar chart shows 10 records
3. Verify most expensive record matches script findings (Meshuggah boxset)
4. Verify least expensive shows $0.50 Wyclef Jean

**Expected**: Data matches `discogs_analysis.py` output

### Test 4: Filter Functionality (10 minutes)
**Test**: Global filters update all charts
**Steps**:
1. Apply "Opeth" filter in artist dropdown
2. Navigate to any chart
3. Verify only Opeth records appear
4. Clear filter
5. Verify all records appear again

**Expected**: Charts update without page reload

### Test 5: Navigation Between Tabs (5 minutes)
**Test**: Tab navigation works seamlessly
**Steps**:
1. Click each of 9 tabs
2. Verify corresponding content loads
3. Verify no JavaScript errors in browser console
4. Verify charts render correctly on each tab

**Expected**: Smooth single-page app experience

## Risks, Tradeoffs, and Open Questions

### Risk 1: Data Loading Performance
**Issue**: Loading 408 records on every refresh could be slow
**Mitigation**: 
- Implement data caching in `dash_cache_data` after first load
- Pre-compute aggregates at startup and store in `dcc.Store`
- Add loading spinner during initial load

**Tradeoff**: Caching means stale data until refresh; acceptable for this use case

### Risk 2: Complex Plotly Conversions
**Issue**: Some 3D plots and animations in original script may not render well in Dash
**Mitigation**: 
- Use Plotly's native 3D scatter instead of complex custom layouts
- Convert Matplotlib boxplots to Plotly equivalents (already done in Task 11)
- For cumulative plots, use Plotly bar charts instead of animated versions

**Tradeoff**: Loss of animation interactivity; gain in stability and performance

### Risk 3: File Path Issues
**Issue**: `output/discogs_clean_data.csv` may not exist or be in wrong location
**Mitigation**: 
- Add error handling with try/except
- Fall back to `data/discogs_data.csv` if cleaned file missing
- Add user-friendly error message in UI if data not found

**Tradeoff**: Extra code complexity; worth it for robustness

### Risk 4: Label Column Ambiguity
**Issue**: Original script splits "Label" into Label1, Label2, etc. Dash may need single label
**Mitigation**: 
- Use first label (Label1) for most analyses
- Add dropdown to select which label column to use
- Document this in app UI

**Tradeoff**: User choice vs simplicity; prefer simplicity for MVP

### Open Questions
1. **Authentication**: Should users need to log in to access their private data?
   - Recommendation: No for MVP; add auth later if needed

2. **Data Export Format**: Should users download individual charts or raw data?
   - Recommendation: Add CSV download of filtered dataset; charts are auto-rendered

3. **Responsive Design**: Should the app work on mobile?
   - Recommendation: Yes, use Dash Bootstrap Template for mobile compatibility

4. **Multiple Datasets**: Should users upload their own CSV?
   - Recommendation: No for MVP; focus on Discogs data first

5. **Plot Customization**: Should users customize plot colors/styles?
   - Recommendation: No for MVP; keep consistent styling

6. **Real-time Updates**: Should data update when external prices change?
   - Recommendation: No; this is a snapshot analysis tool

## Implementation Notes

### Code Style
- Follow PEP 8 for Python
- Use type hints for all function signatures
- Add docstrings to all callback functions
- Keep callback functions focused on single visualizations

### Error Handling
- Wrap CSV loading in try/except
- Show user-friendly error messages for missing files
- Log errors to console for debugging

### Performance
- Set `dash.config.update(title=True)` for performance optimization
- Use `dash.dependencies.CacheManager` for data caching
- Lazy-load heavy plots on tab navigation

### Accessibility
- Add ARIA labels to all interactive elements
- Ensure color contrast meets WCAG 2.1 standards
- Provide keyboard navigation support

### Documentation
- Add inline comments explaining complex logic
- Create README with usage instructions
- Document API endpoints if exposed

## Next Steps After Implementation

1. **User Testing**: Have 3-5 users test the app and report issues
2. **Performance Audit**: Measure load times and optimize bottlenecks
3. **Feature Expansion**: Add missing visualizations from original script
4. **Deployment**: Deploy to Heroku/PythonAnywhere for public access
5. **Documentation**: Expand README with screenshots and examples
