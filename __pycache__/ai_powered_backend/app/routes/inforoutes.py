from app.models.course import Assignment, Course
from app.models.user import User
from flask import Blueprint, jsonify
import plotly.graph_objs as go
from app import db
import requests



info = Blueprint('info', __name__, url_prefix='/info')

@info.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        user_count = db.session.query(User).count()
        assignment_count = db.session.query(Assignment).count()
        course_count = db.session.query(Course).count()

        stats = {
            'user_count': user_count,
            'assignment_count': assignment_count,
            'course_count': course_count
        }

        return jsonify(stats), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@info.route('/chart')
def generate_chart():
    # Fetch data from the API
    try:
        response = requests.get('http://127.0.0.1:8080/info/api/stats')
        data = response.json()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    key_mapping = {
      "assignment_count": "Total Assignments",
      "course_count": "Courses",
      "user_count": "Total users"
    }

    labels = [key_mapping.get(key, key) for key in data.keys()]
    values = list(data.values())

    colors = [
      'rgb(235, 64, 52)',  # a richer shade of red
      'rgb(52, 235, 78)',  # a vibrant, lighter green
      'rgb(52, 115, 235)'  # a soft, pleasing blue
    ]

    fig = go.Figure(data=[go.Bar(x=labels, y=values, marker=dict(color=colors))])
    fig.update_layout(
      title='Data Overview',
      xaxis=dict(title='Categories'),
      yaxis=dict(title='Count'),
      # Add animation settings
      updatemenus=[dict(
        type='buttons',
        showactive=False,
        buttons=[dict(label='Play',
                      method='animate',
                      args=[None, dict(frame=dict(duration=500, redraw=True), fromcurrent=True)])]
      )]
    )
    # Add frames for animation
    fig.frames = [go.Frame(data=[go.Bar(x=labels[:i + 1], y=values[:i + 1], marker=dict(color=colors[:i + 1]))],
                           name=f'frame_{i + 1}') for i in range(len(labels))]

    # Convert Plotly figure to JSON
    chart_json = fig.to_json()

    return jsonify({'chart': chart_json})