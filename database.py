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
    conn.close()

# Adicionar nova matéria
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

# Atualizar matéria existente
def update_materia(id, nome, media_minima, media_atual, nota_necessaria):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            UPDATE materias
            SET nome = ?, media_minima = ?, media_atual = ?, nota_necessaria = ?
            WHERE id = ?
        """, (nome, media_minima, media_atual, nota_necessaria, id))
    conn.close()

# Deletar matéria
def delete_materia(id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM materias WHERE id = ?", (id,))
    conn.close()

# Obter todas as matérias
def get_all_materias():
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materias")
        materias = cursor.fetchall()
    conn.close()
    return materias

# Obter uma matéria específica
def get_materia(id):
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM materias WHERE id = ?", (id,))
        materia = cursor.fetchone()
    conn.close()
    return materia

# Adicionar nota para uma matéria
def add_nota(materia_id, nota, peso):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("""
            INSERT INTO notas (materia_id, nota, peso)
            VALUES (?, ?, ?)
        """, (materia_id, nota, peso))
    conn.close()

# Obter notas por matéria
def get_notas_by_materia(materia_id):
    conn = sqlite3.connect("notas.db")
    with conn:
        cursor = conn.cursor()
        cursor.execute("SELECT nota, peso FROM notas WHERE materia_id = ?", (materia_id,))
        notas = cursor.fetchall()
    conn.close()
    return notas

# Deletar notas por matéria
def delete_notas_by_materia(materia_id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM notas WHERE materia_id = ?", (materia_id,))
    conn.close()
