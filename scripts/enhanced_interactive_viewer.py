import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def create_enhanced_view(left_data, right_data):
    # Create figure with subplots
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"type": "scene", "rowspan": 2}, {"type": "xy"}],
               [None, {"type": "xy"}]],
        subplot_titles=('3D Trajectories', 'Track Length Distribution', 'Active Tracks')
    )
    
    # Store original frame numbers for later use
    left_frames = {}
    right_frames = {}
    
    # Add 3D tracks
    for track_id in left_data['tracking_id'].unique():
        track = left_data[left_data['tracking_id'] == track_id]
        left_frames[track_id] = track['frame'].values
        fig.add_trace(
            go.Scatter3d(
                x=track['pitch_x'],
                y=track['pitch_y'],
                z=track['frame'],
                mode='lines',
                name=f'Left {track_id}',
                line=dict(color='blue'),
                opacity=0.6,
                visible=True
            ),
            row=1, col=1
        )
    
    # Add right camera tracks
    initial_offset = 1885
    for track_id in right_data['tracking_id'].unique():
        track = right_data[right_data['tracking_id'] == track_id]
        right_frames[track_id] = track['frame'].values
        fig.add_trace(
            go.Scatter3d(
                x=track['pitch_x'],
                y=track['pitch_y'],
                z=track['frame'] - initial_offset,
                mode='lines',
                name=f'Right {track_id}',
                line=dict(color='red'),
                opacity=0.6,
                visible=True
            ),
            row=1, col=1
        )
    
    # Add track length distributions
    left_lengths = left_data.groupby('tracking_id').size()
    right_lengths = right_data.groupby('tracking_id').size()
    
    fig.add_trace(
        go.Histogram(x=left_lengths, name='Left tracks', opacity=0.7, marker_color='blue'),
        row=1, col=2
    )
    fig.add_trace(
        go.Histogram(x=right_lengths, name='Right tracks', opacity=0.7, marker_color='red'),
        row=1, col=2
    )
    
    # Add active tracks over time
    left_active = left_data.groupby('frame')['tracking_id'].nunique()
    right_active = right_data.groupby('frame')['tracking_id'].nunique()
    
    fig.add_trace(
        go.Scatter(x=left_active.index, y=left_active.values, name='Left active', line=dict(color='blue')),
        row=2, col=2
    )
    fig.add_trace(
        go.Scatter(x=right_active.index, y=right_active.values, name='Right active', line=dict(color='red')),
        row=2, col=2
    )
    
    # Update layout with sliders
    fig.update_layout(
        title="Enhanced Track Explorer",
        scene=dict(
            bgcolor='black',
            xaxis=dict(title='Pitch X', gridcolor='gray', range=[0, 1000]),
            yaxis=dict(title='Pitch Y', gridcolor='gray', range=[0, 1000]),
            zaxis=dict(title='Frame', gridcolor='gray'),
            camera=dict(
                up=dict(x=0, y=0, z=1),
                center=dict(x=0, y=0, z=0),
                eye=dict(x=1.5, y=1.5, z=1.5)
            )
        ),
        showlegend=True,
        sliders=[
            # X-range slider
            dict(
                active=0,
                currentvalue={"prefix": "X Range: "},
                pad={"t": 50},
                steps=[
                    dict(
                        method="relayout",
                        args=[{"scene.xaxis.range": [x, x+200]}],
                        label=str(x)
                    )
                    for x in range(0, 801, 100)
                ]
            ),
            # Frame range slider
            dict(
                active=0,
                currentvalue={"prefix": "Frame Range: "},
                pad={"t": 100},
                steps=[
                    dict(
                        method="relayout",
                        args=[{"scene.zaxis.range": [f, f+5000]}],
                        label=str(f)
                    )
                    for f in range(0, 180000, 5000)
                ]
            ),
            # Z-offset slider
            dict(
                active=0,
                currentvalue={"prefix": "Z Offset: "},
                pad={"t": 150},
                steps=[
                    dict(
                        method="update",
                        args=[{
                            "z": [
                                frames if i < len(left_frames) 
                                else frames - offset 
                                for i, frames in enumerate(fig.data)
                            ]
                        }],
                        label=str(offset)
                    )
                    for offset in range(1800, 2000, 5)
                ]
            )
        ]
    )
    
    return fig

if __name__ == "__main__":
    # Load data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    
    left_path = os.path.join(data_dir, 'camL_1.csv')
    right_path = os.path.join(data_dir, 'camR_1.csv')
    
    print("Loading data...")
    left_data = pd.read_csv(left_path)
    right_data = pd.read_csv(right_path)
    
    print("Creating enhanced interactive visualization...")
    fig = create_enhanced_view(left_data, right_data)
    
    print("Opening in browser...")
    fig.show() 