# seed_one.py
from datetime import datetime
from app import app, db, Usuarios, UmbralEnum

with app.app_context():
    uid = "user_demo_1"  # mantener siempre el mismo id para tener 1 fila
    u = Usuarios.query.get(uid)
    if u is None:
        u = Usuarios(
            id=uid,
            token_acceso="tok_123",
            valido_hasta=datetime.fromisoformat("2026-12-31T23:59:59"),
            iban="ES6621000418401234567891",
            notificaciones=True,
            umbral=UmbralEnum.medio
        )
        db.session.add(u)
        db.session.commit()
        print("✅ Fila creada:", u.id)
    else:
        print("ℹ️ Ya existía esa fila. No se crean duplicados.")
