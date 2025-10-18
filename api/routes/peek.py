# peek.py
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine("sqlite:///zombis.db")

print("\n== Usuarios ==")
df_users = pd.read_sql("SELECT * FROM Usuarios", engine)
print(df_users.to_string(index=False))

print("\n== AlertasEmitidas ==")
df_alerts = pd.read_sql("""
    SELECT
        IBAN,
        Cod_Transaccion AS codigo_transaccion,
        Importe        AS importe,
        Umbral_probabilistico AS score,
        IBAN_Empresa_cobradora AS empresa
    FROM AlertasEmitidas
    ORDER BY rowid DESC
""", engine)
print(df_alerts.to_string(index=False))
