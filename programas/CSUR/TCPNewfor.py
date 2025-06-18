from flask import Flask, render_template_string
import psutil

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>TCPView Web</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2em; background: #f9f9f9; }
        table { border-collapse: collapse; width: 100%; background: white; }
        th, td { border: 1px solid #ccc; padding: 8px; text-align: left; }
        th { background-color: #f0f0f0; }
        tr:hover { background-color: #f1f9ff; }
        h1 { color: #333; }
    </style>
</head>
<body>
    <h1>Conexiones TCP Activas</h1>
    <table>
        <tr>
            <th>PID</th>
            <th>Proceso</th>
            <th>Local</th>
            <th>Remoto</th>
            <th>Estado</th>
        </tr>
        {% for conn in conns %}
        <tr>
            <td>{{ conn.pid }}</td>
            <td>{{ conn.name }}</td>
            <td>{{ conn.laddr }}</td>
            <td>{{ conn.raddr }}</td>
            <td>{{ conn.status }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
"""

def get_tcp_connections():
    conns = []
    for c in psutil.net_connections(kind='tcp'):
        if not c.raddr:  # Skip if there's no remote address
            continue
        try:
            pname = psutil.Process(c.pid).name() if c.pid else ""
        except psutil.NoSuchProcess:
            pname = "<unknown>"
        conns.append({
            'pid': c.pid,
            'name': pname,
            'laddr': f"{c.laddr.ip}:{c.laddr.port}" if c.laddr else "",
            'raddr': f"{c.raddr.ip}:{c.raddr.port}" if c.raddr else "",
            'status': c.status
        })
    return conns

@app.route("/")
def index():
    conns = get_tcp_connections()
    return render_template_string(HTML_TEMPLATE, conns=conns)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)