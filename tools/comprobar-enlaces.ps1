#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Puerta de enlaces de Data School: comprueba el catálogo y falla si hay algún enlace caído.

.DESCRIPTION
  Envuelve tools/check-links.mjs con los tres ficheros que forman el catálogo vivo
  (fuentes/FUENTES.md, fuentes/POR-TRAMO.md e investigacion/INVESTIGACION.md) y sale con
  código 1 si hay enlaces caídos (404/410/451), para que sirva de puerta en local.

  NO usa GitHub Actions: se ejecuta en la máquina de David. Para programarlo cada semana,
  usa tools/programar-enlaces.ps1 (registra una tarea de Windows) o el Programador de tareas.

  Uso:
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/comprobar-enlaces.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/comprobar-enlaces.ps1 -Json

  Códigos de salida: 0 = sin enlaces caídos; 1 = hay caídos; 2 = no se pudo ejecutar.
#>
param(
  [switch]$Json,
  [string]$Raiz = ''
)

$ErrorActionPreference = 'Stop'
if (-not $Raiz) { $Raiz = Split-Path -Parent $PSScriptRoot }

$node = (Get-Command node -ErrorAction SilentlyContinue).Source
if (-not $node) {
  $candidato = 'C:\Users\David\.dsh\dsh-runtimes\dsh-primary-runtime\dependencies\node\bin\node.exe'
  if (Test-Path $candidato) { $node = $candidato }
}
if (-not $node) { Write-Error 'No encuentro node. Instala Node 20+ o pasa la ruta en el PATH.'; exit 2 }

$checker = Join-Path $Raiz 'tools\check-links.mjs'
if (-not (Test-Path $checker)) { Write-Error "No existe $checker"; exit 2 }

Push-Location $Raiz
try {
  $argumentos = @(
    $checker,
    '--file', 'fuentes/FUENTES.md',
    '--file', 'fuentes/POR-TRAMO.md',
    '--file', 'investigacion/INVESTIGACION.md',
    '--strict'
  )
  if ($Json) { $argumentos += '--json' }
  & $node @argumentos
  $codigo = $LASTEXITCODE
  Write-Host ''
  if ($codigo -eq 0) {
    Write-Host 'Puerta de enlaces: OK (0 caídos).' -ForegroundColor Green
  } else {
    Write-Host "Puerta de enlaces: FALLA (código $codigo). Revisa INFORMES/ y arregla o marca los caídos." -ForegroundColor Red
  }
  exit $codigo
} finally {
  Pop-Location
}
