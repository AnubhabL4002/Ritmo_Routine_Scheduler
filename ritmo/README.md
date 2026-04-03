# 🌸 Ritmo — Your Daily Rhythm

A beautiful daily planner app built with Django. Features drag-and-drop task scheduling, a monthly calendar view, progress tracking, dark/light mode, and a full login/register system — all in coral pink.

---

## ✨ Features

- **Login / Register / Logout** — each user has their own private data
- **Reload-safe routing** — URLs like `/day/2026-04-01/` work on refresh
- **Monthly Calendar** — click any date to open its day planner
- **Drag & Drop** — drag tasks from the pool into time slots
- **Progress tracking** — see % completion per day and per calendar cell
- **Celebration confetti** — all tasks done triggers a party 🎉
- **Dark / Light mode** — preference saved per user
- **Full coral pink theme** — `#f08080` with multiple pink variants

---

## 🚀 Run Locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run migrations

```bash
python manage.py migrate
```

### 3. Start the server

```bash
python manage.py runserver
```

### 4. Open in browser

Visit **http://localhost:8000** — register an account and start planning!

---

## 🌐 Deploy Free Online

### Option A — Railway (Recommended, easiest)

1. Push this folder to a GitHub repository
2. Go to [railway.app](https://railway.app) and sign in with GitHub
3. Click **New Project → Deploy from GitHub repo**
4. Select your repo
5. Railway auto-detects Django via the Procfile
6. Add environment variables in the Railway dashboard:
   - `SECRET_KEY` → any long random string
   - `DEBUG` → `False`
   - `ALLOWED_HOSTS` → `yourapp.railway.app`
7. Click **Deploy** — you'll get a public URL like `https://ritmo-production.railway.app`

### Option B — Render

1. Push to GitHub
2. Go to [render.com](https://render.com) and create a **Web Service**
3. Connect your repo
4. Set:
   - **Build command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start command:** `gunicorn ritmo.wsgi`
5. Add the same environment variables as above
6. Deploy — free tier gives you a `*.onrender.com` URL

### Option C — PythonAnywhere (Free, no credit card)

1. Go to [pythonanywhere.com](https://pythonanywhere.com) and create a free account
2. Open a **Bash console** and run:
   ```bash
   git clone https://github.com/yourusername/ritmo.git
   cd ritmo
   pip3.11 install --user -r requirements.txt
   python manage.py migrate
   python manage.py collectstatic --noinput
   ```
3. Go to **Web** tab → Add a new web app → Manual config → Python 3.11
4. Set the **WSGI file** to point to your project's `wsgi.py`
5. Set the **working directory** to `/home/yourusername/ritmo`
6. Reload — your app is live at `yourusername.pythonanywhere.com`

---

## 📁 Project Structure

```
ritmo/
├── manage.py
├── requirements.txt
├── Procfile                    # for Railway/Render
├── runtime.txt                 # Python version
├── ritmo/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── planner/
    ├── models.py               # Task, DayData, UserPreference
    ├── views.py                # Auth + page views + JSON API
    ├── urls.py
    └── templates/planner/
        ├── login.html
        ├── register.html
        └── app.html            # Main SPA shell
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `SECRET_KEY` | Production only | Long random string for Django security |
| `DEBUG` | Optional | Set to `False` in production |
| `ALLOWED_HOSTS` | Production only | Comma-separated list of your domains |

---

## 🎨 Colour Palette

| Variable | Hex | Use |
|---|---|---|
| `--coral` | `#f08080` | Primary — buttons, accents, logo |
| `--coral-2` | `#ff9090` | Hover states, links |
| `--coral-3` | `#e87878` | Borders, subtle accents |
| `--coral-4` | `#ffa0a0` | Error text, light accents |
| `--coral-5` | `#d06868` | Pressed states, deep accents |
| `--coral-6` | `#ffb5b5` | Confetti, celebrations |
| `--coral-d` | `#e06060` | Gradient end, dark coral |
