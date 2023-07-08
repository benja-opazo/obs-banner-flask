param ($env)

# Change to the directory where the Python app is located
cd "$PSScriptRoot"

# Create Venv if it does not exist
If(!(test-path -PathType container .venv))
{
      python -m venv .venv
}

# Activate venv
.venv\Scripts\activate.ps1

# Install requirements
pip install -r requirements.txt

# Create directories
$TMPDIR = "tmp"
if(!(Test-Path -Path $TMPDIR )){
      New-Item -ItemType directory -Path $TMPDIR
}

# Install Magick
$TARGETDIR = 'magick'
$TARGETFILE = 'magick/magick.zip'

if(!(Test-Path -Path $TARGETDIR )){
      New-Item -ItemType directory -Path $TARGETDIR
}

if(!(Test-Path -Path $TARGETFILE )){
      $MagickURL = "https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-12-portable-Q8-x64.zip"
      Invoke-WebRequest -URI $MagickURL -OutFile $TARGETFILE
      Expand-Archive -LiteralPath $TARGETFILE -DestinationPath $TARGETDIR
}

$env:MAGICK_HOME="/magick"


# Run Flask
if ($env -eq "dev")
{
      flask run --host=0.0.0.0 --debugger --reload
}
else
{
      flask run --host=0.0.0.0
}


