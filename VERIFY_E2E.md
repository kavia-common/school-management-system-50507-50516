# Verify Backend-DB connectivity and Frontend CRUD

This guide helps you verify:
1) Backend connects to PostgreSQL and auto-creates tables
2) Frontend performs CRUD on Teachers, Students, Exams, and Staff

## Prerequisites
- Database service reachable on HOST:5001 (as set in sms_backend/.env)
- FastAPI backend running on http://localhost:3001
- React frontend running on http://localhost:3000

## 1) Backend: DB connectivity and auto-creation
- Ensure `school-management-system-50507-50516/sms_backend/.env` is configured with:
  - `DATABASE_URL=postgresql+asyncpg://USER:PASSWORD@HOST:5001/DBNAME`
  - `ALLOWED_ORIGINS=http://localhost:3000`
- Start backend:
  - python -m venv .venv && source .venv/bin/activate
  - pip install -r sms_backend/requirements.txt
  - uvicorn src.api.main:app --host 0.0.0.0 --port 3001
- Observe logs:
  - Should show successful connection and "Creating database tables" or no exceptions.
  - Visit http://localhost:3001/docs to validate API is live.

## 2) Frontend: configure and start
- Ensure `school-management-system-50507-50517/sms_frontend/.env` contains:
  - `REACT_APP_API_BASE_URL=http://localhost:3001`
- Start frontend:
  - cd school-management-system-50507-50517/sms_frontend
  - npm install
  - npm start
- Open http://localhost:3000

## 3) CRUD validation steps

### Teachers
- Navigate to "Teachers"
- Create: Add teacher with first_name, last_name, email (unique), optional subject/phone
- List: New teacher should appear in list (GET /teachers)
- Update: Edit the created teacher (PUT/PATCH /teachers/{id}) and verify fields update
- Get: Open details if available or confirm list shows updated fields (GET /teachers/{id})
- Delete: Delete the teacher (DELETE /teachers/{id}) and confirm it disappears

### Students
- Navigate to "Students"
- Create: Provide first_name, last_name, email; optional grade and enrollment_date (YYYY-MM-DD)
- List/Update/Get/Delete as above

### Exams
- Navigate to "Exams"
- Create: Provide title, subject, exam_date (YYYY-MM-DD), optional description
- List/Update/Get/Delete as above

### Staff
- Navigate to "Staff"
- Create: Provide first_name, last_name, email; optional role and phone
- List/Update/Get/Delete as above

## 4) Notes/Troubleshooting
- CORS: If you see CORS errors in the browser console, ensure `ALLOWED_ORIGINS` includes `http://localhost:3000`. For multi-origin local testing, use a comma-separated list.
- Backend URL: If the frontend fails to call APIs, verify `REACT_APP_API_BASE_URL` matches the backend host/port and that the backend is reachable by the browser.
- DB URL: Confirm the `DATABASE_URL` host and credentials are correct. The backend auto-upgrades to `postgresql+asyncpg://` if needed; using that form is recommended.

