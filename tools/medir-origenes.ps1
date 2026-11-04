#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Mide los cinco origenes de la consolidacion de Data School.

.DESCRIPTION
  Solo lectura: recorre los origenes y cuenta ficheros, conceptos, fases, datasets,
  figuras, recursos y documentacion. No crea ni modifica nada fuera de la salida.

  Los cinco origenes (rutas de la maquina de David, 2026-11-04):
    1. F:\Proyectos\ProyectoServidor\aprender
    2. F:\Proyectos\ProyectoServidor\aprender\docs\data-school-import
    3. E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia
    4. C:\Users\David\orca\preview-data
    5. F:\Proyectos\data-school

  Uso:
    pwsh -NoProfile -File tools/medir-origenes.ps1
    pwsh -NoProfile -File tools/medir-origenes.ps1 -Ruta 'F:\Proyectos\ProyectoServidor\aprender'
#>
param(
  [string]$Ruta = '',
  [string]$Salida = ''
)

$ErrorActionPreference = 'SilentlyContinue'
$A = 'F:\Proyectos\ProyectoServidor\aprender'
$I = Join-Path $A 'docs\data-school-import'
$O = 'E:\orca-workspaces-archivo-2026-11-03\aprender\equipo-ia'
$P = 'C:\Users\David\orca\preview-data'
$D = 'F:\Proyectos\data-school'
$fecha = (Get-Date).ToString('yyyy-MM-dd')

function Get-Medida([string]$path) {
  $f = @(Get-ChildItem -Recurse -File -Force $path -ErrorAction SilentlyContinue)
  $mb = 0.0
  if ($f.Count -gt 0) { $mb = [math]::Round((($f | Measure-Object Length -Sum).Sum / 1MB), 2) }
  [pscustomobject]@{ Ficheros = $f.Count; MB = $mb }
}

function Get-Recuento([string]$path, [string]$filter = '*') {
  return @(Get-ChildItem -Recurse -File $path -Filter $filter -ErrorAction SilentlyContinue).Count
}

$lineas = [System.Collections.Generic.List[string]]::new()
function Escribe([string]$t) { $lineas.Add($t); Write-Output $t }

Escribe "# Medicion de los cinco origenes - $fecha"
Escribe ''
Escribe 'Origen | Ficheros | MB'
Escribe '---|---|---'
foreach ($par in @(@('1. aprender (portal vivo)', $A), @('2. data-school-import', $I), @('3. Orca equipo-ia', $O), @('4. preview-data', $P), @('5. data-school', $D))) {
  $m = Get-Medida $par[1]
  if (Test-Path $par[1]) { Escribe ("{0} | {1} | {2}" -f $par[0], $m.Ficheros, $m.MB) } else { Escribe ("{0} | NO EXISTE | -" -f $par[0]) }
}
Escribe ''

Escribe '## 1. Portal vivo (aprender)'
Escribe ''
Escribe 'Conceptos por fase (.md) y comparacion con el archivo de Orca:'
Escribe ''
Escribe 'Fase | Aprender .md | Orca .md | Delta'
Escribe '---|---|---|---'
$totalA = 0; $totalO = 0
foreach ($d in (Get-ChildItem -Directory (Join-Path $A 'contenido') | Sort-Object Name)) {
  $na = Get-Recuento (Join-Path $A "contenido\$($d.Name)") '*.md'
  $no = 0
  if (Test-Path (Join-Path $O "contenido\$($d.Name)")) { $no = Get-Recuento (Join-Path $O "contenido\$($d.Name)") '*.md' }
  $totalA += $na; $totalO += $no
  Escribe ("{0} | {1} | {2} | {3}" -f $d.Name, $na, $no, ($na - $no))
}
Escribe ("**Total** | **$totalA** | **$totalO** | **$($totalA - $totalO)**")
Escribe ''
$fases = @(Get-ChildItem -Directory (Join-Path $A 'contenido'))
Escribe "- Fases: $($fases.Count) (f00..f12)"
Escribe "- Conceptos con bloque de codigo: $(@(Get-ChildItem -Recurse -File -Filter '*.md' (Join-Path $A 'contenido') | Where-Object { Select-String -Path $_.FullName -Pattern '^```' -Quiet }).Count) de $totalA"
Escribe "- Bloques :::figura en los conceptos: $(@(Select-String -Path (Join-Path $A 'contenido\*\*.md') -Pattern '^:::figura' -AllMatches).Count)"
Escribe ''
Escribe '### Datasets'
Escribe ''
$csvPortal = @(Get-ChildItem -File (Join-Path $A 'web\datos\datasets') -Filter '*.csv')
$csvProy = @(Get-ChildItem -Recurse -File (Join-Path $A 'proyectos') -Filter '*.csv')
$csvOrca = @(Get-ChildItem -File (Join-Path $O 'web\datos\datasets') -Filter '*.csv')
Escribe "- CSV en web/datos/datasets: $($csvPortal.Count)"
Escribe "- CSV dentro de proyectos/: $($csvProy.Count)"
Escribe "- CSV en el archivo de Orca: $($csvOrca.Count)"
$iguales = 0
foreach ($c in $csvOrca) { $otro = Join-Path $A "web\datos\datasets\$($c.Name)"; if (Test-Path $otro) { if ((Get-FileHash $c.FullName).Hash -eq (Get-FileHash $otro).Hash) { $iguales++ } } }
Escribe "- De los $($csvOrca.Count) CSV de Orca, identicos en la viva: $iguales"
Escribe ''
Escribe '### Figuras y recursos'
Escribe ''
Escribe "- Scripts de figura (.py) en figuras/: $(Get-Recuento (Join-Path $A 'figuras') '*.py')"
Escribe "- Cache de bytecode (.pyc) en figuras/: $(Get-Recuento (Join-Path $A 'figuras') '*.pyc')"
Escribe "- SVG servidos en web/figuras/: $(Get-Recuento (Join-Path $A 'web\figuras') '*.svg')"
Escribe "- SVG en recursos/figuras/: $(Get-Recuento (Join-Path $A 'recursos\figuras') '*.svg')"
Escribe "- Recursos totales (origen): $(Get-Recuento (Join-Path $A 'recursos')) ; en Orca: $(Get-Recuento (Join-Path $O 'recursos'))"
Escribe ''
Escribe '### Verificacion (codigo ejecutado)'
Escribe ''
Escribe "- Aprender: $(Get-Recuento (Join-Path $A '.verificacion') '*.py') .py, $(Get-Recuento (Join-Path $A '.verificacion') '*.sql') .sql, $(Get-Recuento (Join-Path $A '.verificacion') '*.txt') salidas .txt"
Escribe "- Orca: $(Get-Recuento (Join-Path $O '.verificacion') '*.py') .py, $(Get-Recuento (Join-Path $O '.verificacion') '*.sql') .sql, $(Get-Recuento (Join-Path $O '.verificacion') '*.txt') salidas .txt"
Escribe ''
Escribe '### Proyectos, documentacion y especificaciones'
Escribe ''
Escribe "- Proyectos completos en proyectos/: $((Get-ChildItem -Directory (Join-Path $A 'proyectos')).Count)"
Escribe "- Documentacion (docs/): $(Get-Recuento (Join-Path $A 'docs')) ; en Orca: $(Get-Recuento (Join-Path $O 'docs'))"
Escribe "- Especificaciones: $(Get-Recuento (Join-Path $A 'especificaciones')) ; en Orca: $(Get-Recuento (Join-Path $O 'especificaciones'))"
Escribe "- Web (web/): $(Get-Recuento (Join-Path $A 'web')) ; en Orca: $(Get-Recuento (Join-Path $O 'web'))"
Escribe ''
Escribe '### Identidad de ficheros compartidos con Orca (hash)'
Escribe ''
$igualesMd = 0; $distintosMd = 0; $soloOrcaMd = 0
foreach ($f in (Get-ChildItem -Recurse -File -Filter '*.md' (Join-Path $O 'contenido'))) {
  $rel = $f.FullName.Substring((Join-Path $O 'contenido').Length + 1)
  $av = Join-Path $A "contenido\$rel"
  if (Test-Path $av) { if ((Get-FileHash $f.FullName).Hash -eq (Get-FileHash $av).Hash) { $igualesMd++ } else { $distintosMd++ } } else { $soloOrcaMd++ }
}
Escribe "- Conceptos: iguales=$igualesMd distintos=$distintosMd solo-en-Orca=$soloOrcaMd"
$igualesPy = 0; $distintosPy = 0
foreach ($f in (Get-ChildItem -File -Filter '*.py' (Join-Path $O 'figuras'))) {
  $av = Join-Path $A "figuras\$($f.Name)"
  if (Test-Path $av) { if ((Get-FileHash $f.FullName).Hash -eq (Get-FileHash $av).Hash) { $igualesPy++ } else { $distintosPy++ } }
}
Escribe "- Scripts de figura: iguales=$igualesPy distintos=$distintosPy"
$igualesRec = 0; $distintosRec = 0
foreach ($f in (Get-ChildItem -Recurse -File (Join-Path $O 'recursos'))) {
  $rel = $f.FullName.Substring((Join-Path $O 'recursos').Length + 1)
  $av = Join-Path $A "recursos\$rel"
  if (Test-Path $av) { if ((Get-FileHash $f.FullName).Hash -eq (Get-FileHash $av).Hash) { $igualesRec++ } else { $distintosRec++ } }
}
Escribe "- Recursos: iguales=$igualesRec distintos=$distintosRec"
Escribe ''

Escribe '## 2. data-school-import'
Escribe ''
Escribe "- Ficheros: $((Get-Medida $I).Ficheros) ($((Get-Medida $I).MB) MB)"
Escribe "- FUENTES.md: $((Get-Item (Join-Path $I 'FUENTES.md')).Length) bytes"
Escribe "- Herramientas: $(Get-Recuento (Join-Path $I 'tools'))"
Escribe "- Diseno: $(Get-Recuento (Join-Path $I 'designs'))"
Escribe ''

Escribe '## 3. Archivo de Orca (equipo-ia)'
Escribe ''
Escribe "- Ficheros: $((Get-Medida $O).Ficheros) ($((Get-Medida $O).MB) MB)"
Escribe "- Conceptos .md: $totalO; fases: $($fases.Count); CSV: $($csvOrca.Count); scripts de figura: $(Get-Recuento (Join-Path $O 'figuras') '*.py'); recursos: $(Get-Recuento (Join-Path $O 'recursos'))"
Escribe "- Documentos exclusivos de Orca (docs/diseno): $(Get-Recuento (Join-Path $O 'docs\diseno')) ficheros, $((Get-Medida (Join-Path $O 'docs\diseno')).MB) MB"
Escribe "- Modulos web exclusivos: $(@(Get-ChildItem -File (Join-Path $O 'web\assets') | Where-Object { -not (Test-Path (Join-Path $A "web\assets\$($_.Name)")) }).Count) (assets/actividades.js)"
Escribe ''

Escribe '## 4. preview-data'
Escribe ''
$pm = Get-Medida $P
Escribe "- Ficheros: $($pm.Ficheros) ($($pm.MB) MB)"
Escribe "- Contenido: base SQLite de la vista previa (servicio opofuente) + log; sin ficheros de contenido de datos/IA"
Escribe ''

Escribe '## 5. data-school (esta carpeta, antes de la consolidacion)'
Escribe ''
$sinGit = @(Get-ChildItem -Recurse -File -Force $D | Where-Object { $_.FullName -notmatch '\\\.git\\' }).Count
$vacias = (@(Get-ChildItem -Directory $D | Where-Object { @(Get-ChildItem -Recurse -File $_.FullName).Count -eq 0 }).Name) -join ', '
Escribe "- Ficheros (sin .git): $sinGit"
Escribe "- Carpetas vacias: $vacias"
Escribe ''

if ($Salida) {
  $dir = Split-Path -Parent $Salida
  if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
  $lineas | Set-Content -Path $Salida -Encoding utf8
  Write-Output "Informe escrito en $Salida"
}
