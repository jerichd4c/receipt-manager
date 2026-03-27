<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a id="readme-top"></a>

<h3 align="center">Intelligent Receipt Management System </h3>

  <p align="center">
    AI and automation application that processes digital receipts (images and PDFs), extracts key data via OCR, manages states in a database, and coordinates approval flows through interactive emails.
  </p>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#configuration">Configuration</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This application automates receipt processing and approval using modern Computer Vision and AI technologies. It facilitates the receipt lifecycle from reception to final resolution.

**Key Features:**
- **Intelligent Processing:** Text extraction from images and PDFs and identification of fields (Amount, Date, Vendor) using Tesseract OCR and RegEx.
- **State Management:** SQLite database to track the lifecycle ("In Process" → "Approved" / "Rejected").
- **Interactive Notifications:** HTML email delivery with functional buttons to approve or reject receipts directly.
- **RESTful API:** Backend built with FastAPI to upload files and handle decision Webhooks.
- **Audit:** Automatic recording of timestamps and justification comments.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

* [![Python][Python-shield]][Python-url]
* [![FastAPI][FastAPI-shield]][FastAPI-url]
* [![Tesseract][Tesseract-shield]][Tesseract-url]
* [![SQLite][SQLite-shield]][SQLite-url]
* [![SQLAlchemy][SQLAlchemy-shield]][SQLAlchemy-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Follow these steps to set up the project locally.

### Prerequisites

* **Python 3.8** or higher.
* **Tesseract OCR:** Must be installed on the operating system.
    - *Windows:* [Download installer here](https://github.com/UB-Mannheim/tesseract/wiki). **Important:** Select "Spanish" (spa) language in "Additional script data" during installation.
* **Poppler for Windows:** Required to convert PDFs to images. Ensure the path matches `POPPLER_PATH` in `ocr_engine.py`.
* **Gmail Account:** With a generated "App Password" for email sending.

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/jerichd4c/receipt-manager.git
   ```
2. Create and activate virtual environment
   ```sh
   python -m venv venv
   .\venv\Scripts\Activate  # Windows: .\venv\Scripts\Activate, Linux/Mac: source venv/bin/activate
   ```
3. Install dependencies
   ```sh
   pip install -r requirements.txt
   ```

### Configuration

Create a `.env` file in the root (based on `.env.sample`) and configure your variables:

| Variable | Description | Example |
| :--- | :--- | :--- |
| `DATABASE_URL` | DB connection string | `sqlite:///./receipts.db` |
| `SMTP_SERVER` | Email server | `smtp.gmail.com` |
| `SENDER_EMAIL` | Your email (sender) | `youremail@gmail.com` |
| `SENDER_PASSWORD` | App Password (16 characters) | `abcd efgh ijkl mnop` |
| `API_URL` | Base URL where the API runs | `http://localhost:8000` |
| `EMAIL_GERENTE` | Email that will receive requests | `manager@example.com` |

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

1. **Start the server:**
   ```sh
   python run.py
   ```
2. **Access the interface:**
   Open your browser at `http://127.0.0.1:8000/docs` to see the Swagger UI.
3. **Full Flow:**
    - Upload a receipt via `POST /api/upload`.
    - Receive email notification with decision buttons.
    - Click "Approve" or "Reject" and verify the state change in the database.

_For more details on the architecture, check `ocr_engine.py` and `notifications.py` files._

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [FastAPI](https://fastapi.tiangolo.com/) - Modern and fast backend.
* [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) - Text recognition engine.
* [SQLAlchemy](https://www.sqlalchemy.org/) - Robust database management.
* [OpenCV](https://opencv.org/) - Image processing.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
[Python-shield]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[FastAPI-shield]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Tesseract-shield]: https://img.shields.io/badge/Tesseract-OCR-blue?style=for-the-badge
[Tesseract-url]: https://github.com/tesseract-ocr/tesseract
[SQLite-shield]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white
[SQLite-url]: https://www.sqlite.org/
[SQLAlchemy-shield]: https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white
[SQLAlchemy-url]: https://www.sqlalchemy.org/
