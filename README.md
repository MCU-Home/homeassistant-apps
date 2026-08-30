# homeassistant-apps

The Home Assistant app repository for MCUHome: the one source URL a user adds
so that every MCUHome app becomes installable from Home Assistant's app store.
It carries metadata only: the images it names are built and published by each
app's own source repository.

## What this repository holds

- `repository.yaml` — the manifest Home Assistant reads when the URL is added,
  naming the source and the project behind it.
- One directory per app, named by the slug a user sees in paths such as
  `/addon_configs/<id>_<slug>`; `mcuhome-ui/` is the MCUHome web interface.
- Each app's `config.yaml` — the image to pull and the architectures it exists
  for, the version tag, ingress, the Supervisor permissions the app receives,
  and its options schema.
- Each app's `DOCS.md`, which the Supervisor shows as the app's documentation,
  and `translations/`, which carries the wording of its configuration options.
- `scripts/check_apps.py` — the metadata check, which catches on a pull request
  what the Supervisor would otherwise report during an install on someone's
  machine.

## Using it

In Home Assistant, go to Settings → Apps and select Install app; from the
three-dot menu in the top-right corner choose Repositories, and add the URL
below. The MCUHome apps then appear in the app store and install, update and
start like any other.

```
https://github.com/mcu-home/homeassistant-apps
```

## How it fits into MCUHome

An app directory names an image and the version the Supervisor pulls as its
tag; the image itself is built and published by the repository that holds the
app's source. `mcuhome-ui/` points that way at
[mcuhome-ui](https://github.com/mcu-home/mcuhome-ui), whose release publishes
`ghcr.io/mcu-home/ui-homeassistant-app` and whose tag the version key here
matches. No app carries a Dockerfile, so adding an app to MCUHome's app
source means adding its metadata, not its build.

## Development — how to work on this repository

This repository has its own virtual environment in `.venv/`; nothing is
installed into the system Python or into another repository's environment.
`bin/` holds the user-facing entry points, `scripts/` the development
tooling: `scripts/test` and `scripts/lint` dispatch the checks — `all` runs
every one, `list` names them, `<name>` runs one — and each check is its own
wrapper in `scripts/test.d/` or `scripts/lint.d/`. The wrappers select
`.venv` themselves (never activate one by hand) and are exactly what CI
runs, one job per check.

The metadata check (`scripts/check_apps.py`) is a Python 3.13 script with
one dependency beyond the standard library; this repository publishes no
distribution, so only the dev group is installed.

```sh
python3.13 -m venv .venv && .venv/bin/pip install --group dev
```

```sh
scripts/test all
scripts/lint all
```

The rules that hold across every MCUHome repository — coding standards,
commits, licensing — are in the organization's
[contributing guide](https://github.com/mcu-home/.github/blob/main/CONTRIBUTING.md).

## Security

The permissions an installed app receives are declared here: whether it is
reached through ingress, which Supervisor role it asks for, and which
directories are mapped into it. Those keys decide what an app may read and
change on a user's system, so each app declares the grants it needs to work
and no others. Vulnerabilities are reported through the organization's
[security policy](https://github.com/mcu-home/.github/blob/main/SECURITY.md).

## Documentation

- [mcuhome-ui/DOCS.md](mcuhome-ui/DOCS.md) — what the MCUHome web interface app does
- [mcuhome-ui](https://github.com/mcu-home/mcuhome-ui) — its source and its images
- [Home Assistant app repositories](https://developers.home-assistant.io/docs/apps/repository/) — the format this follows
- [MCUHome on GitHub](https://github.com/mcu-home) — the family of repositories

## Contributing and support

Problem reports and questions belong in this repository's
[issue tracker](https://github.com/mcu-home/homeassistant-apps/issues).
Before opening a pull request, read the organization's
[contributing guide](https://github.com/mcu-home/.github/blob/main/CONTRIBUTING.md).

## License

Apache License 2.0, see [LICENSE](LICENSE).
