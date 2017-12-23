import-module au

$releases = 'https://github.com/mickem/nscp/releases'

function global:au_SearchReplace {
    @{
       "$($Latest.PackageName).nuspec" = @{
          "(\<version\>).*?(\</version\>)" = "`${1}$($Latest.Version)`$2"
        }
     }

    @{
       "tools\chocolateyInstall.ps1" = @{
          "(^url\s*=\s*)('.*')"        = "`$1'$($Latest.URL32)'"
          "(^checksum\s*=\s*)('.*')"   = "`$1'$($Latest.Checksum32)'"
          "(^url64\s*=\s*)('.*')"      = "`$1'$($Latest.URL64)'"
          "(^checksum64\s*=\s*)('.*')" = "`$1'$($Latest.Checksum64)'"
        }
     }
}

function global:au_GetLatest {
    $download_page = Invoke-WebRequest -Uri $releases

    $re      = 'NSCP-.*.msi'
    $url     = $download_page.links | ? href -match $re | select -First 2 -expand href
    $url32   = 'https://github.com' + $url[0]
    $url64   = 'https://github.com' + $url[1]
    $version = $url[0] -split '\/' | select -Index 5

    return @{ URL64 = $url64; URL32 = $url32; Version = $version }
}

update -ChecksumFor all