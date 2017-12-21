import-module au

$releases = 'https://github.com/mickem/nscp/releases'

function global:au_SearchReplace {
    @{
       "$($Latest.PackageName).nuspec" = @{
          "(\<version\>).*?(\</version\>)" = "`${1}$($Latest.Version)`$2"
        }
     }
}

function global:au_GetLatest {
    $download_page = Invoke-WebRequest -Uri $releases

    $re      = 'NSCP-.*64.msi'
    $url     = $download_page.links | ? href -match $re | select -First 1 -expand href
    $url64   = 'https://github.com' + $url[0]
    $version = $url[0] -split '\/' | select -Index 5

    return @{ URL64 = $url64; URL32 = $url32; Version = $version }
}

update -ChecksumFor all