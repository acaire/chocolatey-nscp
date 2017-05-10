$packageName = 'NSClient++'
$installerType = 'msi'
$url = 'https://github.com/mickem/nscp/releases/download/0.5.0.62/NSCP-0.5.0.62-Win32.msi'
$url64 = 'https://github.com/mickem/nscp/releases/download/0.5.0.62/NSCP-0.5.0.62-x64.msi'

$silentArgs = '/quiet'
$validExitCodes = @(0)

Install-ChocolateyPackage "$packageName" "$installerType" "$silentArgs" "$url" "$url64"  -validExitCodes $validExitCodes
