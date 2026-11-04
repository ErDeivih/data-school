#!/usr/bin/env pwsh
<#
.SYNOPSIS
  Programa (o quita) la comprobación semanal de enlaces en el Programador de tareas de Windows.

.DESCRIPTION
  Sin GitHub Actions: la comprobación corre en local. Este script registra una tarea de usuario
  que ejecuta tools/comprobar-enlaces.ps1 una vez por semana y guarda su informe en INFORMES/.
  No se ejecuta solo: hay que lanzarlo una vez. No requiere permisos de administrador porque la
  tarea se registra para el usuario actual.

  Uso:
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/programar-enlaces.ps1
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/programar-enlaces.ps1 -Dia WED -Hora 08:30
    powershell -NoProfile -ExecutionPolicy Bypass -File tools/programar-enlaces.ps1 -Quitar
#>
param(
  [ValidateSet('MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN')]
  [string]$Dia = 'MON',
  [string]$Hora = '09:00',
  [switch]$Quitar,
  [string]$Nombre = 'DataSchool-ComprobarEnlaces'
)

$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $PSScriptRoot
$script = Join-Path $raiz 'tools\comprobar-enlaces.ps1'

if ($Quitar) {
  $existente = Get-ScheduledTask -TaskName $Nombre -ErrorAction SilentlyContinue
  if (-not $existente) { Write-Host "No existe la tarea '$Nombre'."; exit 0 }
  Unregister-ScheduledTask -TaskName $Nombre -Confirm:$false
  Write-Host "Tarea '$Nombre' eliminada."
  exit 0
}

if (-not (Test-Path $script)) { throw "No existe $script" }
if ($Hora -notmatch '^\d{2}:\d{2}$') { throw "Hora no válida: $Hora (formato HH:MM)" }

$accion = New-ScheduledTaskAction -Execute 'powershell.exe' `
  -Argument ('-NoProfile -ExecutionPolicy Bypass -File "{0}"' -f $script)
$disparador = New-ScheduledTaskTrigger -Weekly -DaysOfWeek $Dia -At $Hora
$descripcion = 'Data School: comprueba semanalmente los 80+ enlaces del catálogo y escribe INFORMES/enlaces-<fecha>.md (sin GitHub Actions).'

Register-ScheduledTask -TaskName $Nombre -Action $accion -Trigger $disparador `
  -Description $descripcion -Force | Out-Null

Write-Host "Tarea '$Nombre' registrada: todos los $Dia a las $Hora."
Write-Host "Ejecuta ahora una vez: powershell -NoProfile -ExecutionPolicy Bypass -File tools/comprobar-enlaces.ps1"
Write-Host "Para quitarla: powershell -NoProfile -ExecutionPolicy Bypass -File tools/programar-enlaces.ps1 -Quitar"
