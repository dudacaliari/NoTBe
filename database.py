import sqlite3

# Criação das tabelas se não existirem
def create_tables():
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS materias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                media_minima REAL NOT NULL,
                media_atual REAL NOT NULL,
                nota_necessaria REAL NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                materia_id INTEGER NOT NULL,
                nota REAL NOT NULL,
                peso REAL NOT NULL,
                FOREIGN KEY (materia_id) REFERENCES materias (id) ON DELETE CASCADE
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL,
                descricao TEXT NOT NULL
            )
        """)
    conn.close()

# Funções de Materias
def add_materia(nome, media_minima, media_atual, nota_necessaria):
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO materias (nome, media_minima, media_atual, nota_necessaria)
            VALUES (?, ?, ?, ?)
        """, (nome, media_minima, media_atual, nota_necessaria))
        materia_id = cursor.lastrowid
    conn.close()
    return materia_id

def update_materia(id, nome, media_minima, media_atual, nota_necessaria):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            UPDATE materias
            SET nome = ?, media_minima = ?, media_atual = ?, nota_necessaria = ?
            WHERE id = ?
        """, (nome, media_minima, media_atual, nota_necessaria, id))
    conn.close()

def delete_materia(id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM materias WHERE id = ?", (id,))
    conn.close()

def get_all_materias():
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materias")
        materias = cursor.fetchall()
    conn.close()
    return materias

def get_materia(id):
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materias WHERE id = ?", (id,))
        materia = cursor.fetchone()
    conn.close()
    return materia

def add_nota(materia_id, nota, peso):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            INSERT INTO notas (materia_id, nota, peso)
            VALUES (?, ?, ?)
        """, (materia_id, nota, peso))
    conn.close()

def get_notas_by_materia(materia_id):
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nota, peso FROM notas WHERE materia_id = ?", (materia_id,))
        notas = cursor.fetchall()
    conn.close()
    return notas

def delete_notas_by_materia(materia_id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM notas WHERE materia_id = ?", (materia_id,))
    conn.close()

# Funções de Eventos
def add_evento(data, descricao):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            INSERT INTO eventos (data, descricao)
            VALUES (?, ?)
        """, (data, descricao))
    conn.close()

def update_evento(id, data, descricao):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            UPDATE eventos
            SET data = ?, descricao = ?
            WHERE id = ?
        """, (data, descricao, id))
    conn.close()

def delete_evento(id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM eventos WHERE id = ?", (id,))
    conn.close()

def get_eventos_by_data(data):
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id, descricao FROM eventos WHERE data = ?", (data,))
        eventos = cursor.fetchall()
    conn.close()
    return eventos

def get_all_eventos():
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT data, descricao FROM eventos ORDER BY data")
        eventos = cursor.fetchall()
    conn.close()
    return eventos
