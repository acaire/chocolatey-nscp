#!/usr/bin/env python3

import hashlib
import os
import re
import uuid
import zipfile
from pathlib import Path
from shutil import rmtree
from datetime import datetime

import requests
import yaml

def get_uuid():
    return str(uuid.uuid4()).replace('-', '')

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

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    with open('packages.yaml', 'r') as fh:
        packages_yaml = yaml.load(fh, Loader=yaml.SafeLoader)

    for package in packages_yaml['packages']:
        print('Processing package:', package['name'])

        app_uuid = get_uuid()

        version = package['version']

        url_32 = f"https://github.com/mickem/nscp/releases/download/{version}/NSCP-{version}-Win32.msi"
        url_64 = f"https://github.com/mickem/nscp/releases/download/{version}/NSCP-{version}-x64.msi"

        checksum_32 = get_checksum(url_32)
        checksum_64 = get_checksum(url_64)

        release_json = requests.get(f'https://api.github.com/repos/mickem/nscp/releases/tags/{version}').json()
        release_date = datetime.strptime(release_json['published_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
        pre_release = release_json['prerelease']

        release_notes = f"""{release_json['name']} ({release_date})

{release_json['body']}

Release notes sourced from https://github.com/mickem/nscp/releases/tag/{version}
"""

        version_with_beta = version
        if pre_release:
            release_notes = 'Pre-release ' + release_notes
            version_with_beta += '-beta'

        write_file(f"out/{package['name']}.nuspec", f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2011/08/nuspec.xsd">
  <metadata>
    <id>{package['name'].lower()}</id>
    <version>{version_with_beta}</version>
    <title>{package['title']}</title>
    <authors>{package['authors']}</authors>
    <owners>{package['owners']}</owners>
    <licenseUrl>{package['license_url']}</licenseUrl>
    <projectUrl>{package['project_url']}</projectUrl>
    <iconUrl>{package['icon_url']}</iconUrl>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <description>{package['summary']}</description>
    <summary>{package['summary']}</summary>
    <releaseNotes>{release_notes}</releaseNotes>
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

        write_file(f'out/package/services/metadata/core-properties/{app_uuid}.psmdcp', f"""\ufeff<?xml version="1.0" encoding="utf-8"?><coreProperties xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"><dc:creator>{package['authors']}</dc:creator><dc:description>{package['summary']}</dc:description><dc:identifier>{package['name']}</dc:identifier><version>{version_with_beta}</version><keywords>{package['keywords']}</keywords><dc:title>{package['title']}</dc:title><lastModifiedBy>choco, Version=0.10.11.0, Culture=neutral, PublicKeyToken=79d02ea9cad655eb;Microsoft Windows NT 6.2.9200.0;.NET Framework 4</lastModifiedBy></coreProperties>""")

        write_file('out/tools/chocolateyInstall.ps1', f"""\ufeff$packageName = '{package['title']}'
$url32 = '{url_32}'
$url64 = '{url_64}'

$packageArgs = @{{
  PackageName    = $packageName
  FileType       = 'msi'
  Url            = $url32
  Url64bit       = $url64
  SilentArgs     = "/quiet"
  ValidExitCodes = @(0)
  Checksum       = '{checksum_32}'
  ChecksumType   = 'sha256'
  Checksum64     = '{checksum_64}'
  ChecksumType64 = 'sha256'
}}

Install-ChocolateyPackage @packageArgs""")

        zip_filename = f"{package['name']}.{version_with_beta}.nupkg"
        zipf = zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED)
        zipdir('out/', zipf)
        zipf.close()

        rmtree('out')

        if os.getenv('CI', 'false') == 'true':
            with open(os.environ['GITHUB_OUTPUT'], 'a') as fh:
                fh.write(f'nupkg_filename={zip_filename}\n')

if __name__ == '__main__':
    main()
