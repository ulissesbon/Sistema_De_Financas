import sqlite3


conn = sqlite3.connect('financas.db')
cursor = conn.cursor()

def iniciar_dados():

     cursor.execute('''CREATE TABLE IF NOT EXISTS categorias (

                         id INTEGER PRIMARY KEY,

                         nome TEXT NOT NULL
                    )''')


     cursor.execute('''CREATE TABLE IF NOT EXISTS ganhos (

                         id INTEGER PRIMARY KEY,
                    
                         descricao TEXT NOT NULL,

                         valor REAL NOT NULL,
                    
                         categoria_id INTEGER,
                    
                         data DATE,
                    
                         FOREIGN KEY (categoria_id) REFERENCES categorias(id)
                    )''')


     cursor.execute('''CREATE TABLE IF NOT EXISTS gastos (

                         id INTEGER PRIMARY KEY,
                    
                         descricao TEXT NOT NULL,

                         valor REAL NOT NULL,
                    
                         categoria_id INTEGER,
                    
                         data DATE,
                    
                         FOREIGN KEY (categoria_id) REFERENCES categorias(id)
                    )''')


     conn.commit()

     conn.close()