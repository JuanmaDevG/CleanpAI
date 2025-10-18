import sqlite3
import random
import string
from datetime import datetime, timedelta

DB_NAME = "data.db"


def database_exists():
    if not os.path.exists(DB_NAME)
        return False
    
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()
    
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Usuarios'")
        tabla_usuarios = cursor.fetchone()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='AlertasEmitidas'")
        tabla_alertas = cursor.fetchone()
        
        conexion.close()
        return tabla_usuarios is not None and tabla_alertas is not None
            
    except sqlite3.Error:
        conexion.close()
        return False


def delete_database():
    if not os.path.exists(DB_NAME)
        return True
    try:
        os.remove(DB_NAME)
        return True
    except OSError:
        return False


def create_database():
    conexion = sqlite3.connect(DB_NAME)
    cursor = conexion.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Usuarios (
        id_usuario_anonim TEXT PRIMARY KEY,
        token_acceso TEXT NOT NULL,
        valido_hasta TIMESTAMP NOT NULL,
        iban TEXT NOT NULL,
        notificaciones BOOLEAN NOT NULL,
        umbral TEXT CHECK(umbral IN ('alto', 'medio', 'bajo')) NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS AlertasEmitidas (
       id_alerta INTEGER PRIMARY KEY AUTOINCREMENT,
        iban TEXT NOT NULL,
        cod_transaccion TEXT NOT NULL,
        importe REAL NOT NULL,
        umbral_probabilistico REAL NOT NULL,
        iban_empresa_cobradora TEXT NOT NULL,
        fecha_alerta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (iban) REFERENCES Usuarios (iban)
    )
    ''')
    conexion.commit()

    print("LOG: Base de datos creada exitosamente!")
    print("LOG: Tabla 'Usuarios' creada")
    print("LOG: Tabla 'AlertasEmitidas' creada")

    print("\n--- Estructura de la tabla Usuarios ---")
    cursor.execute("PRAGMA table_info(Usuarios)")
    for columna in cursor.fetchall():
        print(f"Columna: {columna[1]}, Tipo: {columna[2]}, PK: {columna[5]}")
    
    print("\n--- Estructura de la tabla AlertasEmitidas ---")
    cursor.execute("PRAGMA table_info(AlertasEmitidas)")
    for columna in cursor.fetchall():
        print(f"Columna: {columna[1]}, Tipo: {columna[2]}, PK: {columna[5]}")
    conexion.close()


def insert_examples(quantity=1000):
    try:
        conexion = sqlite3.connect()
        cursor = conexion.cursor()
        
        usuarios_insertados = 0
        
        for i in range(1, quantity + 1):
            id_usuario = f"USER_{random.randint(1000, 9999)}_{i:05d}"
            parte1 = ''.join(random.choices(string.ascii_uppercase, k=5))
            parte2 = ''.join(random.choices(string.digits, k=5))
            parte3 = ''.join(random.choices(string.ascii_lowercase, k=5))
            token = f"{parte1}_{parte2}_{parte3}"
            
            if i % 10 == 0:  # 10% expiran pronto (1-15 días)
                dias_validez = random.randint(1, 15)
            else:  # 90% válidos por más tiempo
                dias_validez = random.randint(30, 730)  # 1 mes a 2 años
            
            valido_hasta = (datetime.now() + timedelta(days=dias_validez)).strftime("%Y-%m-%d %H:%M:%S")
            
            bancos_espanoles = ['01', '02', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16']
            banco = random.choice(bancos_espanoles)
            sucursal = f"{random.randint(1000, 9999):04d}"
            dc = f"{random.randint(10, 99):02d}"
            cuenta = f"{random.randint(1000000000, 9999999999):010d}"
            iban = f"ES{banco}{sucursal}{dc}{cuenta}"
            
            umbral = random.choices(['alto', 'medio', 'bajo'], weights=[30, 50, 20])[0]
            
            if umbral == 'alto':
                notificaciones = random.random() < 0.9  # 90% True
            elif umbral == 'medio':
                notificaciones = random.random() < 0.7  # 70% True
            else:
                notificaciones = random.random() < 0.4  # 40% True

            try:
                cursor.execute('''
                INSERT OR IGNORE INTO Usuarios 
                (id_usuario_anonim, token_acceso, valido_hasta, iban, notificaciones, umbral)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (id_usuario, token, valido_hasta, iban, notificaciones, umbral))
                
                if cursor.rowcount > 0:
                    usuarios_insertados += 1
                    
            except sqlite3.IntegrityError:
                continue
        
        conexion.commit()
        conexion.close()
        
        return {
            'exito': True,
            'usuarios_generados': quantity,
            'usuarios_insertados': usuarios_insertados
        }
        
    except sqlite3.Error as e:
        return {
            'exito': False,
            'error': f'Error de base de datos: {str(e)}'
        }
