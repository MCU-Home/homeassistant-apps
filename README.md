# MCUHome — Home Assistant Apps

Add this repository to Home Assistant once, and every MCUHome App becomes
installable from the App store.

**Settings → Apps → App Store → ⋮ → Repositories**, then paste:

```
https://github.com/mcu-home/homeassistant-apps
```

## The Apps

| App | What it is | Source |
|---|---|---|
| [MCUHome Dashboard](mcuhome-ui/) | The web interface: create, edit, validate and build devices | [mcu-home/mcuhome-ui](https://github.com/mcu-home/mcuhome-ui) |

MCUHome never compiles firmware inside the dashboard, so a build needs a
build server. That App is not here yet.

## What this repository is, and is not

It is **metadata only**: one directory per App, each holding the
`config.yaml` Home Assistant reads, its documentation and its
translations. There is no Dockerfile here and there will not be one.

Every App's image is built and published by the repository that holds its
**source**, from the same commit that produced the code inside it. This
repository names those images and pins the tag. The split follows the one
rule worth having about packaging: the thing that knows how to build the
program is the thing that builds it, and metadata is metadata.

```
repository.yaml          the source Home Assistant adds
mcuhome-ui/
  config.yaml            what Home Assistant installs, and from where
  DOCS.md                the App's Documentation tab
  translations/en.yaml   option labels
tools/check_apps.py      what CI checks before a user's Supervisor does
```

## Releasing an App

The Supervisor pulls the image tag named by `version:` in an App's
`config.yaml`. So a release is two steps, in this order:

1. **In the source repository**, tag the release. Its workflow builds the
   image and pushes it to GHCR under that version.
2. **Here**, set `version:` in the App's `config.yaml` to the same string.

Home Assistant then offers the update to everyone who has the App
installed. Doing it the other way round offers an update that cannot be
pulled, so the order is the whole procedure.

The two are kept in step by hand for now. If that turns out to be a
recurring nuisance rather than an occasional one, it becomes a workflow.

## Contributing

Issues about an App itself belong in its source repository — the table
above links each one. What belongs here is packaging: a wrong permission,
a missing mapping, documentation that describes the App incorrectly.

Licensed under Apache-2.0; the repository is
[REUSE](https://reuse.software/)-compliant.
