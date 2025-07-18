[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![PyQt6](https://img.shields.io/badge/GUI-PyQt6-green?logo=qt)](https://pypi.org/project/PyQt6/)
![License](https://img.shields.io/badge/license-MIT-green.svg)

# 🎬 Видео Конвертер на Python + PyQt6

Простое и удобное настольное приложение для пакетной конвертации видео в форматы `mp4` или `mp3` с ограничением по размеру. Интерфейс построен на PyQt6, а обработка видео — через `ffmpeg`.

---

## 🧑‍💻 Автор ментор по ручному и автоматизированному тестированию

👤 Даниил Николаев - [телеграм](https://t.me/aqa_pro_mentor)

---

## 🛠️ Возможности

* 📁 Выбор папки с видеофайлами (`.mp4`, `.mkv`, `.avi`, `.mov`, `.flv`)
* 🔄 Массовая конвертация файлов в:

  * 🎥 `mp4`
  * 🎵 `mp3` (только аудио)
* 📦 Ограничение выходного размера в мегабайтах (опционально)
* 📊 Прогресс-бар и лог операций
* 🛑 Возможность остановки процесса
* 🪄 Автоматическое определение пути к `ffmpeg` (в том числе при сборке через PyInstaller)

---
<img width="400" alt="Screenshot 2025-05-25 at 17 44 12" src="https://github.com/user-attachments/assets/d455b63f-1e52-490e-bb4e-363cfd69f35a" />

---
## 📦 Установка

### 🔧 Зависимости

Убедитесь, что у вас установлен Python 3.10+ и `ffmpeg`.

### 🐍 Создание виртуального окружения

```bash
python -m venv .venv
source .venv/bin/activate  # для Linux/macOS
.venv\Scripts\activate     # для Windows
```

### 🧩 Установка зависимостей

```bash
pip install -r requirements.txt
```

---

## 🚀 Запуск

```bash
python main.py
```

> `main.py` — это файл с кодом интерфейса (тот, который ты прислал).

---

## 🧪 Как использовать

1. Нажми **"Выбрать папку"** и укажи папку с видео.
2. Выбери формат выходных файлов: `mp4` или `mp3`.
3. Укажи лимит размера в мегабайтах (или `0`, чтобы не ограничивать).
4. Нажми **"Конвертировать"**.
5. Дождись завершения или нажми **"Завершить текущие операции"**, чтобы остановить.

---

## 🧰 FFMPEG

Программа использует `ffmpeg`, который должен быть размещён по пути:

```
bin/ffmpeg/7.1_4/bin/ffmpeg
```

---

## 📂 Структура проекта

```
transcoding_video/
├── bin/
│   └── ffmpeg/
│       └── 7.1_4/
│           └── bin/
│               └── ffmpeg
├── main.py
├── requirements.txt
└── README.md
```
