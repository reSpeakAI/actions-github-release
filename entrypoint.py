#!/usr/bin/env python3

from github import Github
import os

# Settings
wanted_release = os.getenv('type')
repository = os.getenv('repository')
token = os.getenv('token', None)
sha = os.getenv('sha', None)

# Init class
G = Github(token)
repo = G.get_repo(repository)
releases = list(repo.get_releases())
tags = list(repo.get_tags())
tag_names = [tag.name for tag in tags]

# Sort releases by created date
releases.sort(reverse=True, key=lambda x:x.created_at)

# Output formatting function
def output(release):
    print('::set-output name=release::{}'.format(release.tag_name))
    print('::set-output name=release_id::{}'.format(release.id))
    assets = release.get_assets()
    dl_url = assets[0].browser_download_url if assets.totalCount > 0 else '""'
    print('::set-output name=browser_download_url::{}'.format(dl_url))

# Handle SHA
if sha:
    tag_names = [tag.name for tag in tags if tag.commit.sha == sha]

# Releases parsing
for release in releases:
    # Only look at releases that have the tag name
    if release.tag_name not in tag_names:
        continue
    if wanted_release == 'stable':
        if release.prerelease == 0 and release.draft == 0:
            output(release)
            break
    elif wanted_release == 'prerelease':
        if release.prerelease == 1:
            output(release)
            break
    elif wanted_release == 'latest':
        output(release)
        break
    elif wanted_release == 'nodraft':
        if release.draft == 0:
            output(release)
            break
    else:
        print('Can\'t get release')
