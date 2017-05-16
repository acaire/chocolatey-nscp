$packageName = 'NSClient++'
$url         = 'https://github.com/mickem/nscp/releases/download/0.5.0.62/NSCP-0.5.0.62-Win32.msi'
$url64       = 'https://github.com/mickem/nscp/releases/download/0.5.0.62/NSCP-0.5.0.62-x64.msi'

$packageArgs = @{
  packageName    = $packageName
  fileType       = 'msi'
  url            = $url
  url64bit       = $url64
  silentArgs     = "/quiet"
  validExitCodes = @(0)
  checksum       = 'a9503ed8f3c9aa43aeda439ac39b302f155eea59a43c097fa8adb90770ec4c56'
  checksumType   = 'sha256'
  checksum64     = '7c5ae04dffd956cfbc6fee80a8fefdbe4f53ca6dbc9901e8995003a1ce75e03e'
  checksumType64 = 'sha256'
}

Install-ChocolateyPackage @packageArgs
