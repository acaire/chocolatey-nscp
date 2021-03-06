#!/usr/bin/env python3

import hashlib
import os
import re
import requests
import uuid
import yaml
import zipfile
from pathlib import Path
from shutil import rmtree

def get_uuid():
    return str(uuid.uuid4()).replace('-', '')

def get_latest_release(repo, regex_32, regex_64):
    req = requests.get(f'https://github.com/{repo}/releases/latest', allow_redirects=True)
    version = req.history[0].headers['Location'].split('/')[-1]

    m = re.search(regex_32, req.text)
    url_32 = f"https://github.com/{repo}/releases/download/{version}/{m.group().split('/')[-1]}"

    m = re.search(regex_64, req.text)
    url_64 = f"https://github.com/{repo}/releases/download/{version}/{m.group().split('/')[-1]}"

    return version, url_32, url_64


def get_checksum(url):
    req = requests.get(url)
    return hashlib.sha256(bytes(req.content)).hexdigest()

def mkdir(directory):
    try:
        os.makedirs(directory)
    except FileExistsError:
        pass

def zipdir(path, ziph):
    for root, dirs, files in os.walk(path):
        for file in files:
            write_to = os.path.join(root, file)
            ziph.write(write_to, str(Path(write_to).relative_to(path)))

def write_file(fname, content):
    parent_dir = Path(fname).parent
    mkdir(parent_dir)

    with open(fname, 'w') as f:
        f.write(content)

def main():
    with open('packages.yaml', 'r') as fh:
        packages_yaml = yaml.load(fh, Loader=yaml.SafeLoader)

    for package in packages_yaml['packages']:
        print('Processing package:', package['name'])

        app_uuid = get_uuid()

        version, url_32, url_64 = get_latest_release(package['repo'], package['regex_32'], package['regex_64'])

        checksum_32 = get_checksum(url_32)
        checksum_64 = get_checksum(url_64)

        write_file(f"out/{package['name']}.nuspec", f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd">
  <metadata>
    <id>{package['name'].lower()}</id>
    <version>{version}</version>
    <title>{package['title']}</title>
    <authors>{package['authors']}</authors>
    <owners>{package['owners']}</owners>
    <licenseUrl>{package['license_url']}</licenseUrl>
    <projectUrl>{package['project_url']}</projectUrl>
    <iconUrl>{package['icon_url']}</iconUrl>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <description>{package['summary']}</description>
    <summary>{package['summary']}</summary>
    <releaseNotes>{package['release_notes']}</releaseNotes>
    <copyright />
    <tags>{package['keywords']}</tags>
    <projectSourceUrl>{package['project_source_url']}</projectSourceUrl>
    <packageSourceUrl>{package['package_source_url']}</packageSourceUrl>
    <docsUrl>{package['docs_url']}</docsUrl>
    <bugTrackerUrl>{package['bug_tracker_url']}</bugTrackerUrl>
  </metadata>
</package>""")

        write_file('out/[Content_Types].xml', """\ufeff<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml" /><Default Extension="nuspec" ContentType="application/octet" /><Default Extension="ps1" ContentType="application/octet" /><Default Extension="psmdcp" ContentType="application/vnd.openxmlformats-package.core-properties+xml" /></Types>""".strip())

        write_file('out/_rels/.rels', f"""\ufeff<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Type="http://schemas.microsoft.com/packaging/2010/07/manifest" Target="/{package['name']}.nuspec" Id="Rd1bf6afa331d4810" /><Relationship Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="/package/services/metadata/core-properties/{app_uuid}.psmdcp" Id="R04cea82418ad48d4" /></Relationships>""".strip())

        write_file(f'out/package/services/metadata/core-properties/{app_uuid}.psmdcp', f"""\ufeff<?xml version="1.0" encoding="utf-8"?><coreProperties xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"><dc:creator>{package['authors']}</dc:creator><dc:description>{package['summary']}</dc:description><dc:identifier>{package['name']}</dc:identifier><version>{version}</version><keywords>{package['keywords']}</keywords><dc:title>{package['title']}</dc:title><lastModifiedBy>choco, Version=0.10.11.0, Culture=neutral, PublicKeyToken=79d02ea9cad655eb;Microsoft Windows NT 6.2.9200.0;.NET Framework 4</lastModifiedBy></coreProperties>""")

        write_file('out/tools/chocolateyInstall.ps1', f"""\ufeff$packageName = '{package['title']}'
$url = '{url_32}'
$url64 = '{url_64}'

$packageArgs = @{{
  packageName    = $packageName
  fileType       = 'msi'
  url            = $url
  url64bit       = $url64
  silentArgs     = "/quiet"
  validExitCodes = @(0)
  checksum       = '{checksum_32}'
  checksumType   = 'sha256'
  checksum_64     = '{checksum_64}'
  checksumType64 = 'sha256'
}}

Install-ChocolateyPackage @packageArgs""")

        zipf = zipfile.ZipFile(f"{package['name']}.{version}.nupkg", 'w', zipfile.ZIP_DEFLATED)
        zipdir('out/', zipf)
        zipf.close()

        rmtree('out')

if __name__ == '__main__':
    main()
