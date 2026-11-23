# Lost It, Found It
**AI-Powered College Lost and Found Management System** · BCA Minor Project (2 credits) · Sarla Birla University, Ranchi

Students and faculty report lost or found belongings, browse and search listings, receive AI-suggested matches,
submit ownership claims and track the return of their items. Administrators moderate reports, review claims and manage users.

> **Status:** All code, templates, tests and documents have been written, but I could not run the application or the
> test suite while writing them (no packages could be installed there). Run the tests yourself (step 7) and fix or report
> anything that fails before you demonstrate the project.

## Features
- Student, faculty and administrator roles (admin accounts are created only from the command line)
- Lost and found reports with optional photo (checked by Pillow, renamed, metadata removed)
- Browse, keyword search, category and location filters, pagination
- **AI matching:** Sentence Transformers `all-MiniLM-L6-v2` embeddings + scikit-learn cosine similarity,
  plus small bonuses for same category, brand, colour, location and nearby dates
- Claim workflow: claim with private details → finder/admin approves or rejects with a reason → handover → marked Returned
- Notifications, profile management, admin dashboard, moderation, category management
- CSRF protection, password hashing, role checks, ownership checks, secure sessions, upload validation

## Windows 11 setup (PowerShell)
**Prerequisite:** Python 3.11 or 3.12 from python.org (tick "Add python.exe to PATH"). Check with `py --version`.

```powershell
# 1. Open the project folder
cd path\to\lost_it_found_it

# 2. Create and activate a virtual environment
py -3.12 -m venv .venv          # use -3.11 if that is what you installed
.\.venv\Scripts\Activate.ps1
# If PowerShell blocks the script, run once:  Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

# 3. Install dependencies (the AI libraries are large: allow several minutes and ~2-3 GB of disk)
python -m pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env
python -c "import secrets; print(secrets.token_hex(32))"     # paste the output as SECRET_KEY in .env

# 5. Create the database and the first administrator (password is typed, never stored in code)
python create_admin.py

# 6. Start the app, then open http://127.0.0.1:5000
python run.py

# 7. Run the automated tests (in a second terminal with the venv activated)
python -m pytest
```

**First AI use:** the model (~90 MB) downloads once from the internet and is then cached. To skip AI completely
(keyword matching is used instead) set `AI_ENABLED=0` in `.env`.
**Bootstrap** CSS/JS and icons load from a CDN, so the pages need internet to look right.

## Configuration (`.env`)
| Variable | Meaning | Default |
|---|---|---|
| `SECRET_KEY` | Signs sessions. Use a long random value. | random per start |
| `DATABASE_URL` | SQLAlchemy URL | `sqlite:///lost_it_found_it.db` (stored in `instance/`) |
| `MATCH_THRESHOLD` | Minimum similarity (0-1) to show a suggestion | `0.35` |
| `MAX_MATCHES` | Maximum suggestions per report | `5` |
| `AI_ENABLED` | `0` disables the transformer model | `1` |

## Project structure
```
app/            application package (factory in __init__.py)
  auth/ main/ items/ claims/ admin/   blueprints (routes, forms)
  ai/embeddings.py   loads the model once per process
  ai/matcher.py      similarity, ranking, suggestions
  claims/service.py  claim workflow rules
  templates/ static/
tests/          pytest suite
docs/           PROJECT_REPORT.md, VIVA_AND_PRESENTATION.md
config.py  run.py  create_admin.py  requirements.txt  .env.example
```
Deviation from the suggested layout: added `app/utils.py`, `app/items/images.py`, `app/claims/service.py`,
`app/admin/forms.py` and `pytest.ini`. `init.py` is written as the Python-required `__init__.py`.

## Security notes
- Passwords: Werkzeug hashes. CSRF: Flask-WTF on every POST. Authorization: role decorators and per-record owner checks.
- Uploads: allowed extensions, real image check, 3 MB limit, random file names, re-encoded to strip metadata.
- Claim verification answers and private item details are visible only to the claimant, the item's reporter and admins.
- Set `SESSION_COOKIE_SECURE = True` in `config.py` if you ever serve the site over HTTPS. Do not use `debug=True` in production.

## Troubleshooting
- `ModuleNotFoundError`: the virtual environment is not active (step 2).
- `pip install` fails on a pinned version: note the error; versions were chosen for Python 3.11/3.12 but not installed during writing.
- Admin cannot log in: run `python create_admin.py` again with a different email (it refuses duplicates).
- Reset the database: stop the app, delete `instance\lost_it_found_it.db`, restart, create the admin again.
