"""Laboratório didático local de SQL Injection. Não usar em produção."""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs
from pathlib import Path
import json
import sqlite3

DB_PATH = Path(__file__).resolve().parent / "lab.sqlite3"

PAGE = """<!doctype html><html lang="pt-br"><head><meta charset="utf-8">
<title>Laboratório SQLi — DIO Agent</title>
<style>body{font:16px system-ui;max-width:760px;margin:40px auto;padding:0 18px;color:#222}
form{border:1px solid #ddd;border-radius:10px;padding:18px;margin:18px 0}
label{display:block;margin:10px 0 4px}input,button{font:inherit;padding:8px;width:100%;box-sizing:border-box}
button{margin-top:14px;cursor:pointer}.notice{background:#fff3cd;padding:12px;border-radius:8px}</style></head>
<body><h1>Laboratório local: SQL Injection</h1>
<p class="notice"><strong>Ambiente educacional local.</strong> Não use credenciais reais nem exponha este servidor à rede/internet.</p>
<p>Conta fictícia: <code>aluno</code> / <code>dio123</code></p>
<form method="post" action="/login-vulnerable"><h2>1. Login vulnerável (demonstração)</h2>
<label>Usuário</label><input name="username" autocomplete="off"><label>Senha</label>
<input name="password" type="password"><button>Testar endpoint vulnerável</button></form>
<form method="post" action="/login-secure"><h2>2. Login corrigido (consulta parametrizada)</h2>
<label>Usuário</label><input name="username" autocomplete="off"><label>Senha</label>
<input name="password" type="password"><button>Testar endpoint seguro</button></form></body></html>"""

def initialize_database(db_path=DB_PATH):
    with sqlite3.connect(db_path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL)""")
        conn.execute("INSERT OR IGNORE INTO users(username,password) VALUES (?,?)", ("aluno","dio123"))

def authenticate_vulnerable(username, password, db_path=DB_PATH):
    # INTENCIONALMENTE VULNERÁVEL: exclusivamente para demonstrar SQLi em localhost.
    sql = "SELECT id FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
    with sqlite3.connect(db_path) as conn:
        return conn.execute(sql).fetchone() is not None

def authenticate_secure(username, password, db_path=DB_PATH):
    # CORREÇÃO: os valores são parâmetros separados da estrutura SQL.
    with sqlite3.connect(db_path) as conn:
        return conn.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone() is not None

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_error(404)
            return
        body = PAGE.encode()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        routes = {
            "/login-vulnerable": ("vulnerable", authenticate_vulnerable),
            "/login-secure": ("secure", authenticate_secure),
        }
        if self.path not in routes:
            self.send_error(404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        form = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
        username = form.get("username", [""])[0]
        password = form.get("password", [""])[0]
        label, auth_fn = routes[self.path]
        try:
            accepted = auth_fn(username, password)
            status = 200 if accepted else 401
            result = {"authenticated": accepted, "endpoint": label,
                      "message": "Autenticação aceita (laboratório)" if accepted else "Credenciais inválidas"}
        except sqlite3.Error:
            status = 400
            result = {"authenticated": False, "endpoint": label, "message": "Erro na consulta SQL (laboratório)"}
        body = json.dumps(result, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, fmt, *args):
        # Evita registrar entradas potencialmente sensíveis no terminal.
        return

if __name__ == "__main__":
    initialize_database()
    print("Laboratório em http://127.0.0.1:5000 (somente acesso local)")
    HTTPServer(("127.0.0.1", 5000), Handler).serve_forever()
