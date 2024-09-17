rem run after drop create and grant from SQL

pg_ctl -D "C:\Program Files\PostgreSQL\16\data" restart
cd C:\Dev\makolet_budget\backend
.\venv\Scripts\activate
python C:\Dev\makolet_budget\backend\manage.py migrate
cd C:\Dev\makolet_budget\frontend
npm run dev