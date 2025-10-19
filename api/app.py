from datetime import datetime, timedelta
from enum import Enum
from typing import List, Dict, Any
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # habilitar CORS para que no haya problemas al incorporar la API local desde un front-end
from sqlalchemy import Enum as SAEnum
from pathlib import Path
from ai.largeLanguageModel.queryLargeLanguageModel import queryLargeLanguageModel
from ai.machineLearning.queryMachineLearning import queryMachineLearning
import json
import os
DB_PATH = os.getenv("DB_PATH", "data.db")
MODEL_CACHE = os.getenv("MODEL_CACHE", "/models")
BASE_DIR = Path(__file__).resolve().parent  # carpeta donde está app.py


app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas
# elegir ruta de BD: primero DB_PATH (Docker), si no, tu zombis.db local
db_path = os.getenv("DB_PATH") or str((BASE_DIR / "zombis.db"))
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# -------------------------
# Modelos (tablas exactas)
# -------------------------

class UmbralEnum(str, Enum):
    alto = "alto"
    medio = "medio"
    bajo = "bajo"

class Usuarios(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column("Id_usuario_anonim", db.String, primary_key=True)  # id_usuario anonim
    token_acceso = db.Column("Token_acceso", db.String, nullable=False)
    valido_hasta = db.Column("Valido_hasta", db.DateTime, nullable=False)
    iban = db.Column("IBAN", db.String, nullable=False)
    notificaciones = db.Column("Notificaciones", db.Boolean, nullable=False, default=True)
    umbral = db.Column("Umbral", SAEnum(UmbralEnum), nullable=True)  # puede ser null

class AlertasEmitidas(db.Model):
    __tablename__ = "AlertasEmitidas"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    iban = db.Column("IBAN", db.String, nullable=False)
    codigo_transaccion = db.Column("Cod_Transaccion", db.String, nullable=False)
    importe = db.Column("Importe", db.Float, nullable=False)
    umbral_probabilistico = db.Column("Umbral_probabilistico", db.Float, nullable=False)
    iban_empresa_cobradora = db.Column("IBAN_Empresa_cobradora", db.String, nullable=True)

with app.app_context():
    db.create_all()

# -------------------------
# Helpers y mapping
# -------------------------

UMBRAL_SCORE = {
    "alto": 0.90,
    "medio": 0.70,
    "bajo": 0.50,
}

def resolve_user_threshold(user: Usuarios) -> float:
    """
    Regla de negocio: si user.umbral es null -> usar 'medio' por defecto.
    """
    effective = (user.umbral.value if isinstance(user.umbral, UmbralEnum) else user.umbral) or "medio"
    return UMBRAL_SCORE[effective]

# ===========================================
# ============ CONTRATOS API =================
# ===========================================

# 1) ALTA CLIENTE
@app.route("/users", methods=["POST"])
def alta_cliente():
    data = request.get_json(force=True)

    iban = data.get("iban")
    notificaciones = data.get("notificaciones")
    umbral = data.get("umbral")  # "alto"|"medio"|"bajo" o null
    id_usuario = data.get("id_usuario")
    token_acceso = data.get("token_acceso")
    valido_hasta = data.get("valido_hasta")

    if not all([iban, id_usuario, token_acceso, valido_hasta]):
        return jsonify({"error": "iban, id_usuario, token_acceso y valido_hasta son obligatorios"}), 400

    # Defaults de F1 / reglas de persistencia:
    # - notificaciones: por defecto ON (True) si no se envía
    # - umbral: si no se envía -> persistimos 'medio' (regla de sistema)
    if notificaciones is None:
        notificaciones = True
    umbral_value = None
    if umbral is not None:
        if umbral not in ("alto", "medio", "bajo"):
            return jsonify({"error": "umbral debe ser alto|medio|bajo o null"}), 400
        umbral_value = UmbralEnum(umbral)
    else:
        umbral_value = UmbralEnum.medio  # default sistema

    try:
        valido_dt = datetime.fromisoformat(valido_hasta)
    except Exception:
        return jsonify({"error": "valido_hasta debe ser ISO 8601, p.ej. 2025-12-31T23:59:59"}), 400

    # Upsert simple: si existe, lo reemplazamos según alta
    user = Usuarios.query.get(id_usuario)
    if user is None:
        user = Usuarios(
            id=id_usuario,
            token_acceso=token_acceso,
            valido_hasta=valido_dt,
            iban=iban,
            notificaciones=notificaciones,
            umbral=umbral_value,
        )
        db.session.add(user)
    else:
        user.token_acceso = token_acceso
        user.valido_hasta = valido_dt
        user.iban = iban
        user.notificaciones = notificaciones
        user.umbral = umbral_value

    db.session.commit()
    return jsonify({
        "id_usuario": user.id,
        "iban": user.iban,
        "notificaciones": user.notificaciones,
        "umbral": user.umbral.value if user.umbral else None,
        "valido_hasta": user.valido_hasta.isoformat(),
    }), 201

# 2) BAJA DE CLIENTE
@app.route("/users/<user_id>", methods=["DELETE"])
def baja_cliente(user_id: str):
    user = Usuarios.query.get(user_id)
    if not user:
        return jsonify({"error": "usuario no encontrado"}), 404

    # "desactiva procesamiento futuro y anula notificaciones"
    # Con el esquema dado (sin campo 'activo'), aplicamos:
    user.notificaciones = False
    user.valido_hasta = datetime.utcnow()  # expiramos el token ya TO-DO en un futuro deberemos de expirar el token de forma realista
    db.session.commit()

    return jsonify({"status": "ok", "id_usuario": user.id, "notificaciones": user.notificaciones, "valido_hasta": user.valido_hasta.isoformat()})

# 3) CONFIGURACIÓN DE CLIENTE
# Sustituye el decorador y función de config por esta versión
# Sustituye el decorador y función de config por esta versión
@app.route("/users/<user_id>/config", methods=["GET", "PUT"])
def config_cliente(user_id: str):
    user = Usuarios.query.get(user_id)
    if not user:
        return jsonify({"error": "usuario no encontrado"}), 404

    if request.method == "GET":
        # → Devuelve SOLO la configuración (lo que quieres probar)
        return jsonify({
            "id_usuario": user.id,
            "notificaciones": user.notificaciones,
            "umbral": user.umbral.value if user.umbral else None
        })

    # PUT (ya lo tenías)
    data = request.get_json(force=True)
    if "notificaciones" in data:
        if not isinstance(data["notificaciones"], bool):
            return jsonify({"error": "notificaciones debe ser booleano"}), 400
        user.notificaciones = data["notificaciones"]

    if "umbral" in data:
        umbral = data["umbral"]
        if umbral not in ("alto", "medio", "bajo"):
            return jsonify({"error": "umbral debe ser alto|medio|bajo"}), 400
        user.umbral = UmbralEnum(umbral)

    db.session.commit()
    return jsonify({
        "id_usuario": user.id,
        "notificaciones": user.notificaciones,
        "umbral": user.umbral.value if user.umbral else None
    })



# 4) SUBIDA DE ARCHIVO PROCESAMIENTO
@app.route("/processing/file", methods=["POST"])
def processing_file():
    """
    Espera JSON:
    {
      "transacciones": [
        {
          "IBAN": "string",
          "producto_map": "string",
          "empresa_cobradora_norm": "string",
          "valor": float,
          "fecha": "YYYY-MM-DD",
          "recurrente": bool,
          "primer_gasto_con_empresa": bool,
          "codigo_transaccion": "opcional_string"   # opcional: si no llega, generamos uno
        },
        ...
      ]
    }
    """
    body = request.get_json(force=True, silent=False)
    txs: List[Dict[str, Any]] = body.get("transacciones") if isinstance(body, dict) else None
    if not txs or not isinstance(txs, list):
        return jsonify({"error": "Se requiere 'transacciones' como lista"}), 400

    # >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    # ML_PIPELINE_ENTRYPOINT: AQUÍ ENLAZAMOS CON EL MÓDULO DE ML
    # Nombre inventado y claramente marcado para localizarlo:
    #
    #   forward_to_zombie_detector_ml(transacciones: List[dict]) -> List[dict]
    #
    # Debe devolver una lista con el mismo orden, cada item enriquecido con:
    #   "score" (float entre 0 y 1), "codigo_transaccion" (string)
    # <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

    enriched = forward_to_zombie_detector_ml(txs)

    # Persistimos alertas que superen el umbral del usuario y que tenga notificaciones ON
    created = 0
    for item in enriched:
        iban = item.get("IBAN")
        score = item.get("score")
        importe = float(item.get("valor", 0.0))
        cod_tx = item.get("codigo_transaccion") or f"TX-{int(datetime.utcnow().timestamp()*1000)}"
        empresa_norm = item.get("empresa_cobradora_norm")

        if not iban or score is None:
            continue

        user = Usuarios.query.filter_by(iban=iban).first()
        if not user or not user.notificaciones:
            continue

        threshold = resolve_user_threshold(user)
        if score >= threshold:
            alerta = AlertasEmitidas(
                iban=iban,
                codigo_transaccion=cod_tx,
                importe=importe,
                umbral_probabilistico=float(score),
                iban_empresa_cobradora=empresa_norm  # si no hay IBAN real, guardamos lo que venga normalizado
            )
            db.session.add(alerta)
            created += 1

    db.session.commit()
    return jsonify({"procesadas": len(enriched), "alertas_creadas": created}), 202

# 5) CONSUMO DE ALERTAS
@app.route("/alerts", methods=["GET"])
def get_alerts():
    """
    Opcionalmente admite filtros simples por querystring:
    - iban=ES...
    - min_score=0.7
    """
    q = AlertasEmitidas.query
    iban = request.args.get("iban")
    if iban:
        q = q.filter_by(iban=iban)

    min_score = request.args.get("min_score")
    if min_score:
        try:
            ms = float(min_score)
            q = q.filter(AlertasEmitidas.umbral_probabilistico >= ms)
        except Exception:
            return jsonify({"error": "min_score debe ser numérico"}), 400

    rows = q.order_by(AlertasEmitidas.id.desc()).all()
    out = []
    for r in rows:
        out.append({
            "IBAN": r.iban,
            "codigo_transaccion": r.codigo_transaccion,
            "importe": r.importe,
            "umbral_probabilistico": r.umbral_probabilistico,
            "IBAN_empresa_cobradora": r.iban_empresa_cobradora,
        })
    return jsonify(out)



def forward_to_zombie_detector_ml(transacciones: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Real integration with AI pipeline.
    Combines predictions from ML and LLM.
    """
    enriched = []

    # Load client history (optional, if needed by LLM)
    try:
        with open(AI_DIR / "cliente1_total.json", "r", encoding="utf-8") as f:
            historial_completo = json.load(f)
    except Exception:
        historial_completo = {"transactions": [], "user_profile": {}}

    for t in transacciones:
        tx_data = {
            'transaction_value': t.get('valor', 0.0),
            'is_recurring': t.get('recurrente', False),
            'is_first_purchase': t.get('primer_gasto_con_empresa', False),
            'product_category': t.get('producto_map', ''),
            'collector_company': t.get('empresa_cobradora_norm', ''),
            'iban_anonymized': t.get('IBAN', ''),
            'transaction_date': t.get('fecha', ''),
            'has_been_refunded': False  # no info in your schema, so default to False
        }

        try:
            riesgo_llm = queryLargeLanguageModel(tx_data, historial_completo)
        except Exception:
            riesgo_llm = 0.5

        try:
            riesgo_ml = queryMachineLearning(tx_data)
        except Exception:
            riesgo_ml = 0.5

        score_final = round((riesgo_llm + riesgo_ml) / 2, 3)

        enriched.append({
            **t,
            "codigo_transaccion": t.get("codigo_transaccion") or f"TX-{abs(hash((t.get('IBAN'), t.get('empresa_cobradora_norm'), t.get('fecha'))))%10_000_000}",
            "score": score_final,
        })

    return enriched

# -------------------------
# DEV: Seed / Reset de datos
# -------------------------

def _upsert_user(id_usuario: str, iban: str, umbral: str, notificaciones: bool, dias_validez: int = 90):
    user = Usuarios.query.get(id_usuario)
    if user is None:
        user = Usuarios(
            id=id_usuario,
            token_acceso=f"TOKEN-{id_usuario}",
            valido_hasta=datetime.utcnow() + timedelta(days=dias_validez),
            iban=iban,
            notificaciones=notificaciones,
            umbral=UmbralEnum(umbral),
        )
        db.session.add(user)
    else:
        user.token_acceso = f"TOKEN-{id_usuario}"
        user.valido_hasta = datetime.utcnow() + timedelta(days=dias_validez)
        user.iban = iban
        user.notificaciones = notificaciones
        user.umbral = UmbralEnum(umbral)
    return user

def _add_alerta(iban: str, cod_tx: str, importe: float, score: float, empresa: str = None):
    alerta = AlertasEmitidas(
        iban=iban,
        codigo_transaccion=cod_tx,
        importe=importe,
        umbral_probabilistico=score,
        iban_empresa_cobradora=empresa
    )
    db.session.add(alerta)
    return alerta

@app.route("/dev/seed", methods=["POST"])
def dev_seed():
    """
    Crea datos de prueba idempotentes.
    Body opcional:
    {
      "with_alerts": true   # por defecto true
    }
    """
    body = request.get_json(silent=True) or {}
    with_alerts = body.get("with_alerts", True)

    # --- Usuarios (3 perfiles distintos) ---
    u1 = _upsert_user(
        id_usuario="user_alfa",
        iban="ES9820385778983000760236",
        umbral="medio",          # 0.70
        notificaciones=True
    )
    u2 = _upsert_user(
        id_usuario="user_beta",
        iban="ES9121000418450200051332",
        umbral="bajo",           # 0.50
        notificaciones=True
    )
    u3 = _upsert_user(
        id_usuario="user_gamma",
        iban="ES1720852066781234567890",
        umbral="alto",           # 0.90
        notificaciones=False     # desactiva alertas
    )

    created_alerts = 0
    if with_alerts:
        # Limpieza ligera: no borra todo, pero evita duplicar por código de transacción
        existing_codes = {a.codigo_transaccion for a in AlertasEmitidas.query.all()}

        def safe_add(iban, cod, imp, sc, emp):
            nonlocal created_alerts
            if cod not in existing_codes:
                _add_alerta(iban, cod, imp, sc, emp)
                existing_codes.add(cod)
                created_alerts += 1

        # Para user_beta (umbral 0.50) → deberían aparecer muchas en /alerts
        safe_add(u2.iban, "TX-DEEZER-001", 12.99, 0.62, "DEEZER")
        safe_add(u2.iban, "TX-SUSCRIP-ANTIGUA-002", 7.99, 0.55, "SERVICIO_OLVIDADO")
        safe_add(u2.iban, "TX-GYM-003", 29.90, 0.48, "URBAN_GYM")           # por debajo del umbral → no se filtrará si usas min_score >= 0.50
        safe_add(u2.iban, "TX-STREAM-004", 15.99, 0.73, "STREAMFLIX")

        # Para user_alfa (umbral 0.70) → solo algunas
        safe_add(u1.iban, "TX-JUEGOS-005", 9.99, 0.71, "GAMECLOUD")
        safe_add(u1.iban, "TX-APP-006", 3.49, 0.65, "APPSTORE")             # por debajo del umbral
        safe_add(u1.iban, "TX-CRYPTO-007", 250.00, 0.91, "CRYPTOEX")

        # user_gamma (notificaciones OFF) igualmente dejamos datos manuales para que existan en BD
        safe_add(u3.iban, "TX-PRUEBA-008", 19.99, 0.88, "TIENDA_X")

    db.session.commit()

    return jsonify({
        "usuarios": [
            {"id": u1.id, "iban": u1.iban, "umbral": u1.umbral.value, "notificaciones": u1.notificaciones},
            {"id": u2.id, "iban": u2.iban, "umbral": u2.umbral.value, "notificaciones": u2.notificaciones},
            {"id": u3.id, "iban": u3.iban, "umbral": u3.umbral.value, "notificaciones": u3.notificaciones},
        ],
        "alertas_creadas": created_alerts
    }), 201

@app.route("/dev/reset", methods=["POST"])
def dev_reset():
    """
    Borra todas las filas y deja la BD vacía (tablas se mantienen).
    """
    num_alerts = AlertasEmitidas.query.delete()
    num_users = Usuarios.query.delete()
    db.session.commit()
    return jsonify({"reset_ok": True, "alertas_borradas": num_alerts, "usuarios_borrados": num_users})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
