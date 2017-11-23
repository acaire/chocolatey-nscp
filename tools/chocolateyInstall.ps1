$packageName = 'NSClient++'
$url         = 'https://github.com/mickem/nscp/releases/download/0.5.1.44/NSCP-0.5.1.44-Win32.msi'
$url64       = 'https://github.com/mickem/nscp/releases/download/0.5.1.44/NSCP-0.5.1.44-x64.msi'

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  url            = $url
  url64bit       = $url64
  silentArgs     = "/quiet"
  validExitCodes = @(0)
  checksum       = 'FD26AD092A4956DBF2E6E9DB85A911E49DE9CE49793764AB1A87B80336F30A50'
  checksumType   = 'sha256'
  checksum64     = 'D13C84BFEDA3E84B4E0F7858173A2AE0B1F265C03E5AFF88E1194486FF16A730'
  checksumType64 = 'sha256'
}

Install-ChocolateyPackage @packageArgs
