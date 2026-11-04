#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Ejecuta los bloques `python verificable` de los conceptos importados y guarda la evidencia.

.DESCRIPTION
  El portal vivo tiene su propio verificador (generar.mjs --ejemplos + verificar-ejemplos.ps1),
  pero su carpeta .verificacion se quedo atras: cubre 438 de los 459 conceptos. Este script
  rellena el hueco SIN tocar el origen: extrae los bloques `python verificable` de los conceptos
  que no tienen evidencia en conceptos\verificacion\ y los ejecuta con el Python del sistema,
  guardando el script y su salida real.

  Es idempotente: un concepto que ya tiene evidencia no se vuelve a ejecutar.

  Uso:
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/verificar-conceptos.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/verificar-conceptos.ps1 -Python 'C:\Python312\python.exe'

  Requisitos: Python del sistema con las librerias de requirements.txt del portal
  (numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib, duckdb...).
#>
param(
  [string]$Raiz = '',
  [string]$Python = 'C:\Python312\python.exe',
  [int]$TimeoutSegundos = 60,
  [switch]$Forzar
)

$ErrorActionPreference = 'Stop'
if (-not $Raiz) { $Raiz = Split-Path -Parent $PSScriptRoot }
$conceptos = Join-Path $Raiz 'conceptos'
$verificacion = Join-Path $conceptos 'verificacion'
$salidas = Join-Path $verificacion 'salidas'
$fecha = Get-Date -Format 'yyyy-MM-dd'
$utf8 = New-Object System.Text.UTF8Encoding($false)

if (-not (Test-Path $conceptos)) { throw "No existe $conceptos" }
if (-not (Test-Path $salidas)) { New-Item -ItemType Directory -Path $salidas -Force | Out-Null }
if (-not (Test-Path $Python)) {
  $encontrado = (Get-Command python -ErrorAction SilentlyContinue).Source
  if (-not $encontrado) { throw "No encuentro Python. Pasa -Python <ruta>." }
  $Python = $encontrado
}

$env:PYTHONIOENCODING = 'utf-8'
$env:MPLBACKEND = 'Agg'
$env:PYTHONDONTWRITEBYTECODE = '1'

# Un concepto está cubierto si existe al menos un script <id>--NN.(py|sql) en la evidencia.
$cubiertos = New-Object System.Collections.Generic.HashSet[string]
Get-ChildItem -Path $verificacion -File | Where-Object { $_.Extension -in '.py', '.sql' } | ForEach-Object {
  [void]$cubiertos.Add(($_.BaseName -replace '--\d+$', ''))
}

$md = Get-ChildItem -Path $conceptos -Directory | Where-Object { $_.Name -match '^f\d\d$' } | ForEach-Object {
  Get-ChildItem -Recurse -File $_.FullName -Filter '*.md'
}
$ejecutados = 0
$saltados = 0
$sinEjecutable = New-Object System.Collections.Generic.List[string]
$fallos = New-Object System.Collections.Generic.List[string]

function Ejecutar-Bloque([string]$codigo, [string]$rutaScript) {
  [System.IO.File]::WriteAllText($rutaScript, $codigo, $utf8)
  $psi = New-Object System.Diagnostics.ProcessStartInfo
  $psi.FileName = $Python
  $psi.Arguments = '"' + $rutaScript + '"'
  $psi.WorkingDirectory = $Raiz
  $psi.UseShellExecute = $false
  $psi.RedirectStandardOutput = $true
  $psi.RedirectStandardError = $true
  $psi.StandardOutputEncoding = [System.Text.Encoding]::UTF8
  $psi.StandardErrorEncoding = [System.Text.Encoding]::UTF8
  $psi.EnvironmentVariables['PYTHONIOENCODING'] = 'utf-8'
  $psi.EnvironmentVariables['MPLBACKEND'] = 'Agg'
  $proc = [System.Diagnostics.Process]::Start($psi)
  $out = $proc.StandardOutput.ReadToEndAsync()
  $err = $proc.StandardError.ReadToEndAsync()
  if (-not $proc.WaitForExit($TimeoutSegundos * 1000)) {
    try { $proc.Kill() } catch { }
    return @{ timeout = $true; codigo = 124; salida = ''; error = 'timeout' }
  }
  return @{ timeout = $false; codigo = $proc.ExitCode; salida = $out.Result; error = $err.Result }
}

foreach ($f in $md) {
  $texto = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
  $idOrig = ($texto -split "`n" | Select-String '^id:\s*(.+)$').Matches.Groups[1].Value.Trim()
  if (-not $idOrig) { continue }
  if ($cubiertos.Contains($idOrig) -and -not $Forzar) { $saltados++; continue }

  $bloques = [regex]::Matches($texto, '```python verificable\r?\n(.*?)```', [System.Text.RegularExpressions.RegexOptions]::Singleline)
  if ($bloques.Count -eq 0) { $sinEjecutable.Add($idOrig) | Out-Null; continue }

  $n = 0
  foreach ($b in $bloques) {
    $n++
    $nombre = '{0}--{1:00}' -f $idOrig, $n
    $rutaScript = Join-Path $verificacion ($nombre + '.py')
    $rutaSalida = Join-Path $salidas ($nombre + '.txt')
    $r = Ejecutar-Bloque $b.Groups[1].Value.Trim() $rutaScript
    if ($r.timeout -or $r.codigo -ne 0) {
      $fallos.Add("$nombre (codigo $($r.codigo))") | Out-Null
      Write-Host ("FALLA  {0}  {1}" -f $nombre, ($r.error -split "`n" | Select-Object -Last 1))
      continue
    }
    $textoSalida = if ($r.salida) { $r.salida.TrimEnd() } else { '(sin salida)' }
    if ($textoSalida.Length -gt 20000) { $textoSalida = $textoSalida.Substring(0, 20000) }
    [System.IO.File]::WriteAllText($rutaSalida, $textoSalida, $utf8)
    $ejecutados++
    Write-Host ("OK     {0}" -f $nombre)
  }
}

Write-Host ''
Write-Host ("Ejecutados: {0} bloques nuevos · conceptos con evidencia previa: {1} · sin bloque ejecutable: {2} · fallos: {3}" -f $ejecutados, $saltados, $sinEjecutable.Count, $fallos.Count)
if ($sinEjecutable.Count) { Write-Host ('Sin bloque ejecutable: ' + ($sinEjecutable -join ', ')) }
if ($fallos.Count) { Write-Host ('Fallos: ' + ($fallos -join ', ')); exit 1 }
Write-Host "Evidencia actualizada el $fecha."
exit 0
