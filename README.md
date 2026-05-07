# 🤖 CleanpAI

**Prototipo innovador de detección de fraude en pagos bancarios mediante IA avanzada**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![TypeScript](https://img.shields.io/badge/TypeScript-31.6%25-blue)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python-28%25-green)](https://www.python.org/)
[![Status](https://img.shields.io/badge/Status-Development-yellow)](README.md)

---

## 📋 Descripción del Proyecto

CleanpAI es un prototipo desarrollado para el **Sabadell's Innovation Banking Hack Fest** que implementa inteligencia artificial avanzada para garantizar la seguridad de las transacciones financieras y prevenir pérdidas innecesarias de dinero.

El sistema combina:
- **🧠 Modelo de Lenguaje Avanzado (LLM)** - Análisis contextual y patrones lingüísticos
- **🤖 Red Neuronal Artificial** - Detección automática de anomalías y fraude
- **🔐 Validación Multi-capa** - Verificación de transacciones con múltiples capas de seguridad

---

## ✨ Características Principales

- ✅ Detección inteligente de fraude en transacciones
- ✅ Análisis en tiempo real de patrones de pago
- ✅ Interfaz web moderna y responsive
- ✅ Arquitectura escalable con backend robusto
- ✅ Integración con tecnología de IA de vanguardia
- ✅ Dashboards analíticos para monitoreo

---

## 🏗️ Composición del Proyecto

| Lenguaje | Porcentaje | Rol |
|----------|-----------|-----|
| TypeScript | 31.6% | Backend/Frontend avanzado |
| Python | 28% | Modelos de IA y ML |
| HTML | 26.6% | Estructura web |
| CSS | 6.9% | Estilos frontend |
| SCSS | 4.2% | Preprocesamiento de estilos |
| Dockerfile | 2.4% | Containerización |
| JavaScript | 0.3% | Scripts adicionales |

---

## 🚀 Tecnologías Utilizadas

### Frontend
- **TypeScript** - Tipado estático para mayor seguridad
- **HTML5 / CSS3 / SCSS** - Interfaz moderna y responsive
- **Frameworks modernos** - Experiencia de usuario optimizada

### Backend
- **TypeScript/Node.js** - API robusta y eficiente
- **Python** - Procesamiento de datos y modelos ML

### DevOps
- **Docker** - Containerización y despliegue

### IA & Machine Learning
- **Advanced LLM** - Análisis avanzado de patrones
- **Neural Network** - Detección de anomalías

---

## 📂 Estructura del Proyecto

```
CleanpAI/
├── Front2/                 # Frontend (v0.app)
│   ├── components/         # Componentes React
│   ├── pages/             # Páginas principales
│   └── styles/            # Estilos CSS/SCSS
├── backend/               # Backend API
│   ├── routes/            # Endpoints
│   └── middleware/        # Validación y seguridad
├── ml_models/            # Modelos de IA/ML
│   ├── llm/              # Modelos de lenguaje
│   └── neural_networks/  # Redes neuronales
├── docker/               # Configuración Docker
└── README.md            # Este archivo
```

---

## 🔧 Instalación y Configuración

### Requisitos Previos
- Node.js 16+ 
- Python 3.8+
- Docker (opcional)
- npm o yarn

### Instalación Local

**1. Clonar el repositorio**
```bash
git clone https://github.com/JuanmaDevG/CleanpAI.git
cd CleanpAI
```

**2. Configurar el Frontend**
```bash
cd Front2
npm install
npm run dev
```

**3. Configurar el Backend**
```bash
# En otra terminal
cd backend
npm install
npm start
```

**4. Configurar los Modelos de IA (Python)**
```bash
# En otra terminal
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
python ml_pipeline.py
```

### Con Docker
```bash
docker-compose up
```

---

## 🎯 Cómo Funciona

### 1️⃣ Análisis de Transacción
El sistema recibe información de una transacción bancaria y la procesa a través de múltiples capas de análisis.

### 2️⃣ Evaluación del LLM
El modelo de lenguaje avanzado analiza:
- Contexto de la transacción
- Patrones lingüísticos
- Información textual asociada

### 3️⃣ Detección Neural
La red neuronal artificial:
- Identifica anomalías estadísticas
- Detecta patrones de fraude conocidos
- Evalúa riesgo en tiempo real

### 4️⃣ Validación Multi-capa
- Verifica múltiples criterios de seguridad
- Genera puntuación de riesgo
- Toma decisión final (Aceptar/Rechazar/Revisar)

---

## 📊 Casos de Uso

- 🏦 **Detección de fraude en tiempo real** - Validación instantánea de transacciones
- 💳 **Prevención de pérdidas financieras** - Identificación de transacciones sospechosas
- 📈 **Análisis de patrones** - Monitoreo continuo de comportamiento
- 🚨 **Alertas automáticas** - Notificación inmediata de anomalías
- 📋 **Reportes detallados** - Análisis post-fraude y auditoría

---

## 🔐 Seguridad

- ✅ Validación en múltiples capas
- ✅ Análisis basado en IA
- ✅ Encriptación de datos sensibles
- ✅ Cumplimiento normativo financiero
- ✅ Monitoreo continuo

---

## 📈 Resultados y Métricas

El prototipo ha demostrado:
- ✅ Alta precisión en la detección de fraude
- ✅ Baja tasa de falsos positivos
- ✅ Procesamiento en tiempo real
- ✅ Escalabilidad eficiente

---

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👥 Autores

- **Juan Manuel** - *Desarrollador Principal* - [GitHub](https://github.com/JuanmaDevG)

---

## 🙏 Agradecimientos

- Sabadell Innovation Banking Hack Fest
- Comunidad de desarrolladores y contribuidores
- Equipo de evaluadores del hackathon

---

## 📞 Contacto y Soporte

Para preguntas, sugerencias o reportar problemas:
- 📧 Email: contacto@cleanpai.dev
- 🐛 Issues: [GitHub Issues](https://github.com/JuanmaDevG/CleanpAI/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/JuanmaDevG/CleanpAI/discussions)

---

## 🔗 Enlaces Útiles

- [Página del Proyecto](https://github.com/JuanmaDevG/CleanpAI)
- [Frontend Deployment](https://vercel.com/alr110-3314s-projects/v0-banco-sabadell-app)
- [Documentación de Sabadell Hackathon](#)

---

<p align="center">
  <strong>Desarrollado con ❤️ para el Sabadell's Innovation Banking Hack Fest</strong>
</p>

<p align="center">
  <a href="https://github.com/JuanmaDevG/CleanpAI">⭐ Si te gusta este proyecto, no olvides dejar una estrella</a>
</p>
