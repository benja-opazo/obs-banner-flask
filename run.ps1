# Create Venv if it does not exist
If(!(test-path -PathType container .venv))
{
      python -m venv .venv
}

# Activate venv
.venv\Scripts\activate.ps1

# Install requirements
pip install -r requirements.txt

# Run Flask
flask run --host=0.0.0.0