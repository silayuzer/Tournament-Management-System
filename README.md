# 🏆 TournamentHub — Tournament Management System

> A full-stack web application for creating, managing, and participating in tournaments — built with Django, Bootstrap 5, and SQLite.

---

## 📸 Overview

TournamentHub allows organizers to create tournaments across multiple sports disciplines, manage team and individual registrations, auto-generate match brackets, and track results — all through a clean, responsive interface.

---

## ✨ Features

### 🔐 Authentication & Users
- Custom email-based authentication (no username required)
- Email confirmation on registration
- Password reset via email link
- Role-based access: **Organizer** vs **Player**
- Full name displayed throughout the app

### 🏟 Tournament Management
- Create tournaments with discipline-aware logic:
  - **Team-based** (Soccer) → asks for max teams
  - **Individual** (Tennis, Chess) → asks for max participants
- Application deadline & start time validation
- Search & paginate tournaments on the homepage
- Admin panel with inline contestant and match management

### 👥 Team & Participant Registration
- Players register teams for team-based tournaments
- Players join individual tournaments with one click
- Duplicate registration prevention
- Max capacity enforcement at both model and view level

### ⚔️ Match Generation
- **Round-robin bracket** auto-generation (every contestant plays everyone else)
- Works for both team-based and individual tournaments
- Odd number of contestants supported
- Staff-only access to generate brackets

### 🥇 Results & Standings
- Winners assigned per match via Django Admin
- Winner displayed live on the tournament detail page
- Admin dropdown filtered to only show contestants in that specific match

### 🎨 UI / UX
- Responsive design with **Bootstrap 5** + custom CSS
- Gradient hero sections, animated tournament cards
- Discipline badges, stat counters, match result badges
- Mobile-friendly navbar with role-aware links

---

## 🛠 Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Backend     | Python 3.11, Django 5.2 |
| Database    | SQLite                  |
| Frontend    | Bootstrap 5, Custom CSS |
| Auth        | Custom `AbstractBaseUser` |
| Email       | Django Console Backend (dev) |
| Deployment  | — (see Future Work)     |

---

## 🗂 Project Structure

```
tournament_system/
├── accounts/          # Custom user model, auth, password reset
├── tournaments/       # Tournament & Match models, bracket logic
├── teams/             # Team registration
├── participants/      # Individual participant registration
├── config/            # Settings, URLs, base templates
└── static/css/        # Custom stylesheet
```

---

## ⚙️ Setup & Installation

```bash
# 1. Clone the repository
git clone https://github.com/silayuzer/Tournament-Management-System.git
cd Tournament-Management-System

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create a superuser
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then visit `http://127.0.0.1:8000`

---

## 🧠 Key Engineering Decisions

- **Custom `AbstractBaseUser`** — email as the primary identifier instead of username, giving full control over the auth flow.
- **Discipline-aware forms** — JavaScript dynamically shows/hides `max_teams` vs `max_participants` based on sport selection, preventing invalid data at the UI level before server-side validation runs.
- **Round-robin bracket generation** — uses Python's `itertools.combinations` to pair every contestant with every other, supporting odd numbers of players.
- **Separated `participants` app** — individual sport contestants live in their own Django app with its own admin section, keeping concerns clean and the admin sidebar organized.
- **Model-level capacity enforcement** — `clean()` + `save()` on `Participant` and `Team` models ensure limits are respected even if someone bypasses the view layer.
- **Admin winner filtering** — `MatchAdmin.formfield_for_foreignkey` restricts the winner dropdown to only the two contestants in that specific match.

---

## 🔮 Future Improvements

- [ ] Deployment on Render / Railway
- [ ] REST API with Django REST Framework
- [ ] Tournament bracket visualization (SVG tree)
- [ ] Leaderboard & standings table
- [ ] Email notifications for match results
- [ ] OAuth login (Google)

---

## 👤 Author

**Sıla Yüzer**
[github.com/silayuzer](https://github.com/silayuzer)