$packageName = 'NSClient++'

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  file           = gi package\*x86.msi
  file64         = gi package\*x64.msi
  silentArgs     = "/quiet"
  checksum       = 'AUTO_GENERATED'
  checksumType   = 'sha256'
  checksum64     = 'AUTO_GENERATED'
  checksumType64 = 'sha256'
}

Install-ChocolateyPackage @packageArgs
