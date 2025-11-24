# Sistema Inteligente de Gestión de Facturas 🧾

Aplicación de IA y automatización que procesa facturas digitales, extrae datos clave mediante OCR, gestiona estados en base de datos y coordina flujos de aprobación mediante correos electrónicos interactivos.

  - **Procesamiento Inteligente:** Extracción de texto e identificación de campos (Monto, Fecha, Proveedor) usando Tesseract OCR y RegEx.
  - **Gestión de Estados:** Base de datos SQLite para trazar el ciclo de vida ("En Proceso" → "Aprobado" / "Rechazado").
  - **Notificaciones Interactivas:** Envío de correos HTML con botones funcionales para aprobar o rechazar facturas directamente.
  - **API RESTful:** Backend construido con FastAPI para subir archivos y manejar Webhooks de decisión.
  - **Auditoría:** Registro automático de timestamps y comentarios de justificación.

-----

## Requisitos previos ⚙️

  - **Python 3.8** o superior.
  - **Tesseract OCR:** Debe estar instalado en el sistema operativo (no solo la librería de Python).
      - *Windows:* [Descargar instalador aquí](https://www.google.com/search?q=https://github.com/UB-Mannheim/tesseract/wiki). **Importante:** Durante la instalación, seleccionar el idioma "Spanish" (spa) en "Additional script data".
  - **Cuenta de Gmail:** Con "Contraseña de Aplicación" generada (para el envío de correos).
  - **Navegador Web:** Para interactuar con la documentación automática de la API.

Dependencias de Python se instalan desde `requirements.txt`.

-----

## Instalación 📦

En **PowerShell** (Windows) o Terminal:

```powershell
# 1) Clonar el repositorio
# git clone https://github.com/<tu-usuario>/receipt-manager.git
# cd receipt-manager

# 2) Crear y activar entorno virtual (Recomendado)
python -m venv venv
.\venv\Scripts\Activate  # En Mac/Linux: source venv/bin/activate

# 3) Instalar dependencias
pip install -r requirements.txt
```

-----

## Configuración 🔧

El proyecto utiliza `python-dotenv` para la seguridad. Crea un archivo `.env` en la raíz (basado en `.env.example`) y configura tus variables:

| Variable | Descripción | Ejemplo |
| :--- | :--- | :--- |
| `DATABASE_URL` | Ruta de conexión a la BD | `sqlite:///./facturas.db` |
| `SMTP_SERVER` | Servidor de correo | `smtp.gmail.com` |
| `SENDER_EMAIL` | Tu correo (remitente) | `tucorreo@gmail.com` |
| `SENDER_PASSWORD` | Contraseña de Aplicación (16 caracteres) | `abcd efgh ijkl mnop` |
| `API_URL` | URL base donde corre la API | `http://localhost:8000` |
| `EMAIL_GERENTE` | Correo que recibirá las solicitudes | `jefe@ejemplo.com` |

-----

## Puesta en marcha rápida 🚀

1.  **Iniciar el Servidor:**
    Ejecuta el siguiente comando para levantar la API:

    ```powershell
    uvicorn main:app --reload
    ```

2.  **Acceder a la Interfaz:**
    Abre tu navegador en `http://127.0.0.1:8000/docs`. Verás la interfaz automática (Swagger UI) para probar los endpoints.

3.  **Probar el Flujo:**

      - Usa el endpoint `POST /api/upload` para subir una imagen de factura.
      - Revisa la consola para ver la extracción de datos.
      - Revisa tu correo: deberías recibir una notificación con botones.
      - Haz clic en "Aprobar" o "Rechazar" en el correo y verifica el cambio en la base de datos.

-----

## Flujo de trabajo 🧭

1.  **Ingesta:** El usuario sube una imagen (`.png`, `.jpg`) a través de la API (`main.py`).
2.  **Procesamiento (Módulo 1):** `ocr_engine.py` limpia la imagen con OpenCV y extrae texto con Tesseract. RegEx identifica los montos y fechas.
3.  **Persistencia (Módulo 2):** Se guarda la factura en `facturas.db` con estado "En Proceso" (`database.py`).
4.  **Notificación (Módulo 3):** `notifications.py` genera un email HTML con los datos y enlaces únicos hacia la API.
5.  **Decisión (Módulo 4):** El usuario hace clic en el correo. La API recibe la señal (Webhook), actualiza el estado y registra la auditoría.

-----

## Estructura del proyecto 📁

Cumpliendo con el diseño modular requerido:

```text
receipt-manager/
├── uploads/                    # Almacenamiento temporal de imágenes
├── .env                        # Credenciales (NO subir a Git)
├── database.py                 # Modelos ORM y conexión a SQLite
├── main.py                     # API FastAPI y orquestador del flujo
├── notifications.py            # Motor de envío de correos HTML
├── ocr_engine.py               # Lógica de Visión Computacional y NLP
├── requirements.txt            # Lista de dependencias del proyecto
└── facturas.db                 # Base de datos local (generada automáticamente)
```

-----

## Solución de problemas 🧩

  - **Error `TesseractNotFoundError`:** Asegúrate de haber instalado el programa `.exe` de Tesseract y, si es necesario, ajusta la ruta en `ocr_engine.py` (`tesseract_cmd`).
  - **Error de Autenticación SMTP:** Verifica que estás usando una "Contraseña de Aplicación" de Google y no tu contraseña habitual. Asegúrate de que la Verificación en 2 pasos esté activa.
  - **Botones del correo no funcionan:** Si el servidor no está corriendo (`uvicorn`), los enlaces darán error. Asegúrate de que `API_URL` en el `.env` coincida con la dirección de tu servidor local.

-----

## Notas de seguridad 🔒

  - El archivo `.env` está incluido en `.gitignore` para proteger las credenciales de correo.
  - La base de datos `facturas.db` y la carpeta `uploads/` también son ignoradas para no compartir datos de prueba sensibles.

-----

## Créditos 🙌

  - [FastAPI](https://fastapi.tiangolo.com/) para el backend moderno y veloz.
  - [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) para el motor de reconocimiento de texto.
  - [SQLAlchemy](https://www.sqlalchemy.org/) para el manejo robusto de base de datos.