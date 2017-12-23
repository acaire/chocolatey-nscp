$packageName = 'NSClient++'
$url         = 'https://github.com/mickem/nscp/releases/download/0.5.0.62/NSCP-0.5.0.62-Win32.msi'
$url64       = 'https://github.com/mickem/nscp/releases/download/0.5.0.62/NSCP-0.5.0.62-x64.msi'
$checksum    = 'foo'
$checksum64  = 'foobar'

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  url            = $url
  url64bit       = $url64
  silentArgs     = "/quiet"
  validExitCodes = @(0)
  checksum       = $checksum
  checksumType   = 'sha256'
  checksum64     = $checksum64
  checksumType64 = 'sha256'
}

Install-ChocolateyPackage @packageArgs
