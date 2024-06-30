import os


def create(payload, url, port, path):
    template = f'''<html>
        <head>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        </head>
        <body>
        <button type="submit" id="start">Click me!</button>
            <script>
            $(document).ready(function(){{
    let websocket = new WebSocket("ws://{url}:{port}/{path}");

    websocket.onopen = function(ev)
    {{
    console.log('Connected to server');
    }}

    websocket.onclose = function(ev)
    {{
        console.log('Disconnected from server');
    }};

    websocket.onmessage = function(ev)
    {{
        console.log('Message: '+ev.data);
    }};

    websocket.onerror = function(ev)
    {{
        console.log('Error: '+ev.data);
    }};
    $('#start').click(function() {{
        var payload = \'{payload}\';
        websocket.send(payload);
    }});
    }});

            </script>
        </body>
    </html>
    '''
    if not os.path.exists('templates'):
        os.makedirs('templates')
    with open('templates/index.html', 'w') as data_file:
        data_file.write(template)


def run():
    os.system('fastapi dev server.py')
