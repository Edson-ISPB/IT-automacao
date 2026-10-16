$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
$EnvironmentPath = Join-Path $Root ".venv-build"
$PythonPath = Join-Path $EnvironmentPath "Scripts\python.exe"

Set-Location $Root

if (-not (Test-Path $PythonPath)) {
    if (Get-Command py -ErrorAction SilentlyContinue) {
        & py -3 -m venv $EnvironmentPath
    } elseif (Get-Command python -ErrorAction SilentlyContinue) {
        & python -m venv $EnvironmentPath
    } else {
        throw "Python 3 is required on the build computer. It is not required on computers running the EXE."
    }

    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the build environment."
    }
}

& $PythonPath -m pip install -r requirements-build.txt
if ($LASTEXITCODE -ne 0) {
    throw "Could not install the build dependencies."
}

& $PythonPath -m PyInstaller `
    --noconfirm `
    --clean `
    --onefile `
    --name GTIC-Diagnostico `
    --collect-all psutil `
    --specpath build `
    --workpath build\work `
    --distpath dist `
    main.py

if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller failed to build the executable."
}

Write-Host "Build complete: $(Join-Path $Root 'dist\GTIC-Diagnostico.exe')"