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
        conn.execute("""
            INSERT INTO materias (nome, media_minima, media_atual, nota_necessaria)
            VALUES (?, ?, ?, ?)
        """, (nome, media_minima, media_atual, nota_necessaria))
    conn.close()

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

# Excluir matéria
def delete_materia(id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM materias WHERE id = ?", (id,))
    conn.close()

# Obter todas as matérias
def get_all_materias():
    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materias")
    materias = cursor.fetchall()
    conn.close()
    return materias

# Obter uma única matéria
def get_materia(materia_id):
    conn = sqlite3.connect("notas.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM materias WHERE id = ?", (materia_id,))
    materia = cursor.fetchone()
    conn.close()
    return materia  # Retorna uma única linha

# Adicionar nota
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
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM notas WHERE materia_id = ?", (materia_id,))
    notas = cursor.fetchall()
    conn.close()
    return notas

# Excluir nota
def delete_nota(nota_id):
    conn = sqlite3.connect("notas.db")
    with conn:
        conn.execute("DELETE FROM notas WHERE id = ?", (nota_id,))
    conn.close()

# Calcular nota necessária
def calcular_nota_necessaria(media_minima, soma_pesos, soma_ponderada):
    return (media_minima * (soma_pesos + 1) - soma_ponderada) / 1

# Criar tabelas ao iniciar o banco de dados
create_tables()