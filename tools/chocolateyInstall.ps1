$ErrorActionPreference = 'Stop'

$packageName = 'NSClient++'
$toolsDir = Split-Path $MyInvocation.MyCommand.Definition

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  file           = gi $toolsDir\*Win32.msi
  file64         = gi $toolsDir\*x64.msi
  silentArgs     = "/quiet"
}

Install-ChocolateyPackage @packageArgs
