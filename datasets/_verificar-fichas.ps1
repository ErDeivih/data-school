# Verificador de la entrega de fichas y verificacion de datasets (task-4).
# Uso: powershell.exe -NoProfile -ExecutionPolicy Bypass -File datasets\_verificar-fichas.ps1
# Devuelve exit 0 solo si TODO pasa. Es un artefacto temporal: se borra al cerrar la tarea.
# ASCII puro + -Encoding UTF8 al leer: Windows PowerShell 5.1 lee los .md como ANSI si no se le dice.

$ErrorActionPreference = 'Stop'
$datasets = $PSScriptRoot
$fallos = New-Object System.Collections.ArrayList

$iAcento = [char]0x00ED   # i con tilde
$nTilde  = [char]0x00F1   # n con tilde
$script:total = 0

function Ok($cond, $msg) {
  $script:total++
  if ($cond) { "  OK    $msg" } else { "  FALLO $msg"; [void]$fallos.Add($msg) }
}

function LeerMd($ruta) { Get-Content $ruta -Raw -Encoding UTF8 }

"== 1. FICHAS.md =="
$fichasPath = Join-Path $datasets 'FICHAS.md'
$fichasOk = Test-Path $fichasPath
Ok $fichasOk 'FICHAS.md existe'
if ($fichasOk) {
  $f = LeerMd $fichasPath
  $ids = [regex]::Matches($f, '(?m)^- \*\*id\*\*:')
  Ok ($ids.Count -eq 10) "10 fichas (encontradas $($ids.Count))"
  $campos = @('id', ('t' + $iAcento + 'tulo'), 'fichero', 'licencia', 'procedencia',
              ('tama' + $nTilde + 'o'), 'columnas y tipos', 'checksum', 'dificultad',
              'preguntas que permite responder', 'proyectos que lo usan', 'limitaciones')
  foreach ($c in $campos) {
    $pat = '(?m)^- \*\*' + [regex]::Escape($c) + '\*\*:'
    $n = [regex]::Matches($f, $pat).Count
    Ok ($n -eq 10) "campo '$c' en 10 fichas (encontrado $n)"
  }
  $esperados = @('ventas-mensuales','clientes-churn','precios-accion','sensores-planta',
                 'encuestas-satisfaccion','algoritmos-tiempos','telemetria-f1','cartera-acciones',
                 'f1-clasificacion','futbol-partidos')
  $faltan = @($esperados | Where-Object { $f -notmatch [regex]::Escape($_) })
  Ok ($faltan.Count -eq 0) "los 10 ids aparecen (faltan: $($faltan -join ', '))"
  Ok (([regex]::Matches($f, '(?m)^### ')).Count -eq 10) '10 secciones ### (una por ficha)'
  Ok (($f -match 'CC0-1\.0')) 'licencia CC0-1.0 citada'
  Ok (($f -match 'generar-datasets\.mjs')) 'procedencia: generar-datasets.mjs citado'
  # uniformidad: misma secuencia de campos en las 10 fichas
  $bloques0 = [regex]::Split($f, '(?m)^### \d+\. ') | Select-Object -Skip 1
  $secuencias = @{}
  foreach ($b in $bloques0) {
    $k = (@([regex]::Matches($b, '(?m)^- \*\*([^*]+)\*\*:') | ForEach-Object { $_.Groups[1].Value }) -join '|')
    if (-not $secuencias.ContainsKey($k)) { $secuencias[$k] = 0 }
    $secuencias[$k]++
  }
  Ok ($secuencias.Count -eq 1) "secuencia de campos identica en las 10 fichas ($($secuencias.Count) variante/s)"
  # preguntas: entre 3 y 5 por ficha
  foreach ($b in $bloques0) {
    $idb = [regex]::Match($b, '`([a-z0-9\-]+)`').Groups[1].Value
    $preg = @([regex]::Matches($b, '(?m)^  - [^`]') | ForEach-Object { $_.Value })
    Ok ($preg.Count -ge 3 -and $preg.Count -le 5) "ficha '$idb': 3-5 preguntas ($($preg.Count))"
  }
}

"== 2. VERIFICACION.md =="
$verifPath = Join-Path $datasets 'VERIFICACION.md'
$verifOk = Test-Path $verifPath
Ok $verifOk 'VERIFICACION.md existe'
if ($verifOk) {
  $v = LeerMd $verifPath
  $secciones = [regex]::Matches($v, '(?m)^### \d+\. `')
  Ok ($secciones.Count -eq 10) "10 perfiles con seccion propia (encontrados $($secciones.Count))"
  Ok (($v -match '2026-11-04')) 'fecha 2026-11-04'
  Ok (($v -match 'data_profile')) 'herramienta usada citada'
  Ok (($v -match '10/10')) 'resultado global 10/10'
  Ok (([regex]::Matches($v, '(?m)^\| \d+ \| `')).Count -eq 10) 'tabla resumen con 10 filas de dataset'
}

"== 2b. Cifras del resumen contrastadas con el manifiesto =="
$m0 = LeerMd (Join-Path $datasets 'datasets.json') | ConvertFrom-Json
$porTipo = @{}
foreach ($c in ($m0.conjuntos | ForEach-Object { $_.columnas })) {
  if (-not $porTipo.ContainsKey($c.tipo)) { $porTipo[$c.tipo] = 0 }
  $porTipo[$c.tipo]++
}
$v2 = LeerMd $verifPath
$bt = [char]0x60
foreach ($k in $porTipo.Keys) {
  $esperado = "$bt$k$bt $($porTipo[$k])"
  Ok ($v2 -match [regex]::Escape($esperado)) "recuento de tipo '$k' = $($porTipo[$k]) en VERIFICACION"
}
Ok (($v2 -match 'total 63') -or ($v2 -match '63/63')) 'total de columnas 63 citado en VERIFICACION'
$totFilas = ($m0.conjuntos | ForEach-Object { $_.filas } | Measure-Object -Sum).Sum
Ok ($v2 -match [regex]::Escape("$totFilas / $totFilas")) "total de filas $totFilas citado en VERIFICACION"

"== 2c. Proyectos citados en FICHAS.md coinciden con proyectos/CATALOGO.md =="
$catPath = Join-Path (Split-Path -Parent $datasets) 'proyectos/CATALOGO.md'
if (-not (Test-Path $catPath)) {
  Ok $false "no existe $catPath"
} else {
  $cat = LeerMd $catPath
  $mapa = @{}
  foreach ($mm in [regex]::Matches($cat, '(?m)^\| (proj:P\d\d|lab:L\d\d) \|(?:[^|\n]+\|){2,4} `([a-z0-9\-]+)` \|$')) {
    $rec = $mm.Groups[1].Value; $ds = $mm.Groups[2].Value
    if (-not $mapa.ContainsKey($ds)) { $mapa[$ds] = @() }
    $mapa[$ds] += $rec
  }
  Ok ($mapa.Keys.Count -eq 10) "catalogo de proyectos: 10 datasets asignados ($($mapa.Keys.Count))"
  $fx = LeerMd $fichasPath
  $bloques = [regex]::Split($fx, '(?m)^### \d+\. ') | Select-Object -Skip 1
  Ok ($bloques.Count -eq 10) "FICHAS.md dividido en 10 bloques ($($bloques.Count))"
  $totalCitados = 0
  foreach ($b in $bloques) {
    $idm = [regex]::Match($b, '`([a-z0-9\-]+)`')
    if (-not $idm.Success) { continue }
    $ds = $idm.Groups[1].Value
    $citados = @([regex]::Matches($b, '(proj:P\d\d|lab:L\d\d)') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    $esperados = @()
    if ($mapa.ContainsKey($ds)) { $esperados = @($mapa[$ds] | Sort-Object -Unique) }
    $iguales = (($citados -join ',') -eq ($esperados -join ','))
    Ok $iguales "ficha '$ds': proyectos citados = catalogo (ficha: $($citados -join ','); catalogo: $($esperados -join ','))"
    $totalCitados += $citados.Count
  }
  Ok ($totalCitados -eq 30) "30 citas de proyecto en total (encontradas $totalCitados)"
}

"== 3. datasets.json y CSV sin modificar =="
$hashJson = (Get-FileHash (Join-Path $datasets 'datasets.json') -Algorithm SHA256).Hash.ToLower()
Ok ($hashJson -eq 'e25351858ef11b3a5e087adb660b3fbc60cf209f0e707e689301db0a9cee222d') "datasets.json intacto ($hashJson)"
$m = LeerMd (Join-Path $datasets 'datasets.json') | ConvertFrom-Json
$mal = 0; $ok = 0
foreach ($s in $m.conjuntos) {
  $csv = Join-Path $datasets ("csv/" + $s.id + '.csv')
  if (-not (Test-Path $csv)) { $mal++; continue }
  $h = 'sha256:' + (Get-FileHash $csv -Algorithm SHA256).Hash.ToLower()
  if ($h -eq $s.checksum) { $ok++ } else { $mal++ }
}
Ok ($ok -eq 10 -and $mal -eq 0) "sha256 de los 10 CSV coincide con el manifiesto ($ok OK / $mal MAL)"

"== 3b. Cabeceras: nombres y orden iguales al manifiesto =="
foreach ($s in $m.conjuntos) {
  $hdr = (Get-Content (Join-Path $datasets ("csv/" + $s.id + '.csv')) -TotalCount 1)
  $cols = $hdr -split ','
  $esp = @($s.columnas | ForEach-Object { $_.nombre })
  Ok ((($cols -join ',') -eq ($esp -join ','))) "cabecera de '$($s.id)': nombres y orden coinciden"
  Ok (-not ($hdr -match '"') -and @($cols | Where-Object { $_ -eq '' }).Count -eq 0) "cabecera de '$($s.id)': sin comillas ni campos vacios"
}

"== 4. README enlaza las dos piezas =="
$r = LeerMd (Join-Path $datasets 'README.md')
Ok (($r -match '\[FICHAS\.md\]\(FICHAS\.md\)')) 'README enlaza FICHAS.md'
Ok (($r -match '\[VERIFICACION\.md\]\(VERIFICACION\.md\)')) 'README enlaza VERIFICACION.md'
Ok (($r -match '\]\(_verificar-fichas\.ps1\)')) 'README enlaza el comprobador (_verificar-fichas.ps1)'
Ok (($v -match '\]\(_verificar-fichas\.ps1\)')) 'VERIFICACION enlaza el comprobador (_verificar-fichas.ps1)'
Ok (-not ($r -match '92 criterios')) 'README no cita un recuento fijo de criterios (no se queda obsoleto)'
Ok (-not ($v -match 'los 92 criterios')) 'VERIFICACION no cita un recuento fijo de criterios'

"== 5. Enlaces relativos de los .md nuevos resuelven =="
foreach ($doc in @($fichasPath, $verifPath)) {
  if (-not (Test-Path $doc)) { Ok $false "$(Split-Path -Leaf $doc): no existe, no se pueden comprobar enlaces"; continue }
  $nombre = Split-Path -Leaf $doc
  $texto = LeerMd $doc
  $enlaces = [regex]::Matches($texto, '\]\(([^)#\s]+)') | ForEach-Object { $_.Groups[1].Value }
  $rotos = @()
  foreach ($e in $enlaces) {
    if ($e -match '^(https?:|mailto:)') { continue }
    if (-not (Test-Path (Join-Path $datasets $e))) { $rotos += $e }
  }
  Ok ($rotos.Count -eq 0) "${nombre}: enlaces relativos correctos (rotos: $($rotos -join ', '))"
}

""
"criterios ejecutados: $script:total"
if ($fallos.Count -eq 0) { "RESULTADO: VERDE - todos los criterios pasan"; exit 0 }
"RESULTADO: ROJO - $($fallos.Count) criterio(s) sin cumplir:"
$fallos | ForEach-Object { "  - $_" }
exit 1
