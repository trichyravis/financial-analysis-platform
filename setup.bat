@echo off
echo 🏔️ The Mountain Path - Financial Analysis Platform
echo Setting up your system...

REM Check Python version
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📥 Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

echo ✅ Setup complete!
echo.
echo 🚀 To launch the application, run:
echo    venv\Scripts\activate.bat
echo    streamlit run app.py
echo.
echo Happy analyzing! 🎉
