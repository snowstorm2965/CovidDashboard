"""
This script runs the CovidDashboard application using a development server.
"""

from os import environ
from CovidDashboard import app

if __name__ == '__main__':
    HOST = environ.get('SERVER_HOST', 'localhost')
    #HOST = environ.get('SERVER_HOST', '192.168.1.74')
    try:
        PORT = int(environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    #app.run(HOST, PORT)
    app.run(host='0.0.0.0', port=5555)

