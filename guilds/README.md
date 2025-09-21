## Intro to django.

First get your virtual environment setup to work

(Assuming you have python installed)
(Assuming you are in the JojosReferenceSASEHack directory and are doing this in the VSCode terminal)
python -m venv venv
(you may also use python3 instead of python depending on your version)
(you will see a file called venv appear)
. .\venv\Scripts\activate
(or depending on your OS)
. .\venv\bin\activate
(This will make a small "(venv)" appear in your terminal)
(This is a virtual environment and the command you just used above is how it is activated)
python -m pip install -r requirements.txt
(This will install all the requirements and modules you need)
cd guilds
(To go in the directory of the actual frontend)
python manage.py runserver
(This will run the actual frontend server)
``` bash
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
September 21, 2025 - 01:28:17
Django version 5.2.6, using settings 'guilds.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.

WARNING: This is a development server. Do not use it in a production setting. Use a production WSGI or ASGI server instead.
For more information on production servers see: https://docs.djangoproject.com/en/5.2/howto/deployment/
```
This will show up which is normal. Go to the link and it will show the main server link

Below is whatever ChatGPT thought would be appropriate info

Here’s the README in raw **Markdown (`.md`)** format — you can copy this directly into a `README.md` file in your repo:

````markdown
# 📖 Guild – Django Project for Frontend & Templates

Welcome to the **Guild** project! 🎉
This Django project is already set up with one app called **`pages`**.
As a frontend developer, your main task is to work on the **HTML templates** and design the site’s pages.

---

## ⚙️ 1. Setup Instructions

### Clone the Repository
```bash
git clone <your-repo-url>
cd guild
````

### Create a Virtual Environment

It’s best practice to use a virtual environment so dependencies don’t interfere with global Python.

```bash
# create venv (Windows)
python -m venv venv

# create venv (Mac/Linux)
python3 -m venv venv
```

Activate it:

* **Windows (PowerShell):**

  ```bash
  venv\Scripts\activate
  ```
* **Mac/Linux:**

  ```bash
  source venv/bin/activate
  ```

You should now see `(venv)` before your terminal prompt.

### Install Requirements

The repo includes a `requirements.txt`. Install everything with:

```bash
pip install -r requirements.txt
```

This installs Django and any other required libraries.

---

## 🚀 2. Run the Development Server

To preview your work, run:

```bash
python manage.py runserver
```

Open your browser at [http://127.0.0.1:8000/](http://127.0.0.1:8000/).
Whenever you edit templates, refresh the page to see updates.

---

## 🗂️ 3. Filesystem Overview

The key folders/files for frontend developers:

```
guild/
├── guild/                ← project config (ignore unless debugging)
│   └── urls.py           ← URL patterns (routes to views)
├── pages/                ← app containing templates
│   ├── templates/        ← HTML files live here
│   │   ├── base.html     ← main site layout
│   │   └── pages/        ← app-specific templates
│   │       └── home.html ← example page
│   ├── views.py          ← connects templates to the browser
└── manage.py             ← run commands (runserver, etc.)
```

---

## 🎨 4. Template Basics

### `base.html` – Layout

The **base template** defines the overall layout (header, nav, footer).

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>{% block title %}Guild{% endblock %}</title>
</head>
<body>
  <header>
    <h1>Guild</h1>
    <nav>
      <a href="/">Home</a>
    </nav>
  </header>

  <main>
    {% block content %}{% endblock %}
  </main>

  <footer>
    <p>&copy; 2025 Guild</p>
  </footer>
</body>
</html>
```

* `{% block title %}` → each page can set its own `<title>`.
* `{% block content %}` → placeholder for page content.

---

### `home.html` – Example Page

Located in `pages/templates/pages/home.html`:

```html
{% extends "base.html" %}

{% block title %}Home - Guild{% endblock %}

{% block content %}
  <h2>Welcome to Guild</h2>
  <p>This is the homepage.</p>
{% endblock %}
```

👉 This reuses `base.html` and only defines its content.

---

## 👀 5. Views & URLs (Quick Reference)

In `pages/views.py`:

```python
from django.shortcuts import render

def home(request):
    return render(request, "pages/home.html")
```

In `guild/urls.py`:

```python
from django.contrib import admin
from django.urls import path
from pages import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
]
```

So when you visit `/`, Django serves `home.html`.

---

## ✅ 6. Your Workflow

1. Activate the virtual environment (`venv`).
2. Run the server with `python manage.py runserver`.
3. Edit `base.html` for layout changes.
4. Create new pages inside `pages/templates/pages/`.
5. Refresh the browser to preview your work.

That’s all you need to get started with web design in this project! 🚀
