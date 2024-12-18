from flask import Flask, render_template_string
import pandas as pd
import os
import plotly.graph_objects as go
from plotly.subplots import make_subplots

app = Flask(__name__)

def analyze_csv(file_path):
    data = pd.read_csv(file_path)
    total_entries = len(data)
    unique_tracks = data['tracking_id'].nunique()
    total_frames = data['frame'].nunique()
    teams = sorted(data['team_id'].unique())
    
    return {
        "file_name": os.path.basename(file_path),
        "total_entries": total_entries,
        "unique_tracks": unique_tracks,
        "total_frames": total_frames,
        "teams": teams
    }

def create_3d_visualization():
    data_dir = '../stadium_data'
    files = ['camL_1.csv', 'camM_1.csv', 'camR_1.csv']
    colors = {'camL_1.csv': 'blue', 'camM_1.csv': 'red', 'camR_1.csv': 'green'}
    
    fig = make_subplots(
        rows=1, cols=1,
        specs=[[{"type": "scene"}]],
        subplot_titles=('3D Trajectories',)
    )
    
    for file in files:
        file_path = os.path.join(data_dir, file)
        data = pd.read_csv(file_path)
        color = colors[file]
        
        for track_id in data['tracking_id'].unique():
            track_data = data[data['tracking_id'] == track_id]
            fig.add_trace(
                go.Scatter3d(
                    x=track_data['pitch_x'],
                    y=track_data['pitch_y'],
                    z=track_data['frame'],
                    mode='lines',
                    line=dict(color=color, width=2),
                    opacity=0.6
                )
            )
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(title='X'),
            yaxis=dict(title='Y'),
            zaxis=dict(title='Frame')
        ),
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white')
    )
    
    return fig.to_html(full_html=False)

@app.route('/')
def index():
    data_dir = '../stadium_data'
    files = ['camL_1.csv', 'camM_1.csv', 'camR_1.csv']
    analyses = [analyze_csv(os.path.join(data_dir, file)) for file in files]
    plot_html = create_3d_visualization()
    
    html = """
    <style>
        body {
            background-color: black;
            color: white;
        }
    </style>
    <h1>CSV Analysis</h1>
    {% for analysis in analyses %}
        <h2>{{ analysis.file_name }}</h2>
        <ul>
            <li>Total Entries: {{ analysis.total_entries }}</li>
            <li>Unique Tracks: {{ analysis.unique_tracks }}</li>
            <li>Total Frames: {{ analysis.total_frames }}</li>
            <li>Teams: {{ analysis.teams }}</li>
        </ul>
    {% endfor %}
    <div>{{ plot_html|safe }}</div>
    """
    
    return render_template_string(html, analyses=analyses, plot_html=plot_html)

if __name__ == '__main__':
    app.run(debug=True)