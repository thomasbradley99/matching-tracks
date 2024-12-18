import pandas as pd
import plotly.graph_objects as go
import os

def load_data(file_path):
    """Load CSV data."""
    return pd.read_csv(file_path)

def plot_tracks(left_data, right_data, z_offset=0):
    """Plot player tracks with adjustable time offset."""
    fig = go.Figure()

    # Define colors for teams
    team_colors = {
        1: 'blue',    # Team 1
        2: 'yellow',  # Team 2
        3: 'green',   # Team 3
        # Add more teams and colors as needed
    }

    # Plot left camera data
    for track_id in left_data['tracking_id'].unique():
        track = left_data[left_data['tracking_id'] == track_id]
        team_id = track['team_id'].iloc[0]  # Assuming 'team_id' column exists
        color = team_colors.get(team_id, 'gray')  # Default to gray if team not found
        fig.add_trace(
            go.Scatter3d(
                x=track['pitch_x'],
                y=track['pitch_y'],
                z=track['frame'],
                mode='lines',
                name=f'Left {track_id}',
                line=dict(color=color),
                opacity=0.6
            )
        )

    # Plot right camera data with offset
    for track_id in right_data['tracking_id'].unique():
        track = right_data[right_data['tracking_id'] == track_id].copy()
        track['frame'] = track['frame'] - z_offset  # Apply the offset
        team_id = track['team_id'].iloc[0]  # Assuming 'team_id' column exists
        color = team_colors.get(team_id, 'gray')  # Default to gray if team not found
        fig.add_trace(
            go.Scatter3d(
                x=track['pitch_x'],
                y=track['pitch_y'],
                z=track['frame'],
                mode='lines',
                name=f'Right {track_id}',
                line=dict(color=color),
                opacity=0.6
            )
        )

    fig.update_layout(
        title=f"Synchronized Tracks (offset: {z_offset} frames)",
        scene=dict(
            xaxis_title='Pitch X',
            yaxis_title='Pitch Y',
            zaxis_title='Frame'
        ),
        showlegend=True,
        paper_bgcolor='black',
        plot_bgcolor='black',
        font=dict(color='white')
    )

    fig.show()

if __name__ == "__main__":
    # Get absolute paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'stadium_data')

    left_path = os.path.join(data_dir, 'camL_1.csv')
    right_path = os.path.join(data_dir, 'camR_1.csv')

    print("Loading data...")
    left_data = load_data(left_path)
    right_data = load_data(right_path)

    # Adjust the z_offset as needed
    z_offset = 0  # Change this value to adjust synchronization

    print("Creating visualization...")
    plot_tracks(left_data, right_data, z_offset) 