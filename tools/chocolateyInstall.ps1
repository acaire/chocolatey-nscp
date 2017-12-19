$packageName = 'NSClient++'
$url         = "https://github.com/mickem/nscp/releases/download/{0}/NSCP-{0}-Win32.msi" -f $env:pkg_version
$url64       = "https://github.com/mickem/nscp/releases/download/{0}/NSCP-{0}-x64.msi" -f $env:pkg_version

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  url            = $url
  url64bit       = $url64
  silentArgs     = "/quiet"
  validExitCodes = @(0)
  checksum       = $env:checksum
  checksumType   = 'sha256'
  checksum64     = $env:checksum64
  checksumType64 = 'sha256'
}

Install-ChocolateyPackage @packageArgs
