# Check requirements
python --version
node --version

# Setup Backend
Write-Host "Setting up Backend..."
cd backend
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt

# Init DB
Write-Host "Initializing Database..."
python -m app.init_data

# Start Backend in new window
Write-Host "Starting Backend Server..."
Start-Process powershell -ArgumentList "cd '$PWD'; .\venv\Scripts\activate; uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Setup Frontend
Write-Host "Setting up Frontend..."
cd ..\frontend
npm install

# Start Frontend in new window
Write-Host "Starting Frontend Server..."
Start-Process powershell -ArgumentList "cd '$PWD'; npm run dev"

Write-Host "Project started!"
Write-Host "Backend API: http://localhost:8000/docs"
Write-Host "Frontend: http://localhost:5173"
