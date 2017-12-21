$ErrorActionPreference = 'Stop'

$packageName = 'NSClient++'
$toolsDir = Split-Path $MyInvocation.MyCommand.Definition

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  file           = gi $toolsDir\*Win32.msi
  file64         = gi $toolsDir\*x64.msi
  silentArgs     = "/quiet"
  checksum       = 'AUTO_GENERATED'
  checksumType   = 'sha256'
  checksum64     = 'AUTO_GENERATED'
  checksumType64 = 'sha256'
}

Install-ChocolateyPackage @packageArgs
