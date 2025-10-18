-- schema.sql
PRAGMA foreign_keys = ON;

-- =====================================================
-- Tabla: Usuarios
-- Campos según contrato:
--  Id_usuario_anonim (PK)
--  Token_acceso
--  Valido_hasta (ISO-8601 -> almacenado como TEXT o DATETIME)
--  IBAN
--  Notificaciones (BOOLEAN 0/1)
--  Umbral (alto|medio|bajo|NULL)
-- =====================================================
CREATE TABLE IF NOT EXISTS Usuarios (
    Id_usuario_anonim       TEXT PRIMARY KEY,
    Token_acceso            TEXT NOT NULL,
    Valido_hasta            TEXT NOT NULL,                 -- usar ISO 8601: YYYY-MM-DDTHH:MM:SS
    IBAN                    TEXT NOT NULL,
    Notificaciones          INTEGER NOT NULL DEFAULT 1,    -- 1=True, 0=False
    Umbral                  TEXT CHECK (Umbral IN ('alto','medio','bajo') OR Umbral IS NULL)
);

-- Índices útiles
CREATE INDEX IF NOT EXISTS idx_Usuarios_IBAN ON Usuarios (IBAN);
CREATE INDEX IF NOT EXISTS idx_Usuarios_ValidoHasta ON Usuarios (Valido_hasta);

-- =====================================================
-- Tabla: AlertasEmitidas
-- Campos mínimos de salida/contrato:
--  IBAN
--  Cod_Transaccion
--  Importe
--  Umbral_probabilistico
--  IBAN_Empresa_cobradora
-- =====================================================
CREATE TABLE IF NOT EXISTS AlertasEmitidas (
    id                          INTEGER PRIMARY KEY AUTOINCREMENT,
    IBAN                        TEXT NOT NULL,
    Cod_Transaccion             TEXT NOT NULL,
    Importe                     REAL NOT NULL,
    Umbral_probabilistico       REAL NOT NULL,             -- 0..1
    IBAN_Empresa_cobradora      TEXT
    -- Si quisieras forzar relación con Usuarios por IBAN:
    -- ,FOREIGN KEY (IBAN) REFERENCES Usuarios (IBAN) ON DELETE SET NULL
);

-- Índices útiles para consumo / filtros
CREATE INDEX IF NOT EXISTS idx_Alertas_IBAN ON AlertasEmitidas (IBAN);
CREATE INDEX IF NOT EXISTS idx_Alertas_Score ON AlertasEmitidas (Umbral_probabilistico);
CREATE INDEX IF NOT EXISTS idx_Alertas_Tx ON AlertasEmitidas (Cod_Transaccion);

-- (Opcional) Semillas de prueba
-- INSERT INTO Usuarios (Id_usuario_anonim, Token_acceso, Valido_hasta, IBAN, Notificaciones, Umbral)
-- VALUES ('user_demo','tok_demo','2026-12-31T23:59:59','ES9820385778983000760236',1,'medio');
