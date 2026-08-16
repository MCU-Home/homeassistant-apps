#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 The MCUHome Contributors
# SPDX-License-Identifier: Apache-2.0
"""Check this repository against what a Home Assistant Supervisor expects.

The Supervisor is the real validator, and it validates at *install* time —
on a user's machine, after they added this repository. That is a bad place
to find out that a key is misspelled, so the cheap half of its schema is
checked here instead: the keys an app cannot work without, the ones this
repository has rules about, and the two mistakes that are specific to
publishing images from somewhere else (a tag on the image name, and a
version that no longer matches it).

It deliberately does not reimplement the Supervisor's schema. Anything not
listed below is the Supervisor's business.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

import yaml

REPO = Path(__file__).resolve().parent.parent

#: Keys every app in this repository must set. `image` is on the list
#: because an app here never carries a Dockerfile: the image is built and
#: published by the app's own source repository and only referenced here.
REQUIRED_APP_KEYS = ("name", "version", "slug", "description", "url", "image", "arch")

#: Architectures Home Assistant knows. `armhf`/`armv7`/`i386` were dropped
#: by Home Assistant itself; listing one would be a promise nothing can keep.
KNOWN_ARCH = frozenset({"amd64", "aarch64"})


def _load(path: Path) -> Any:
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def _check_repository(problems: list[str]) -> None:
    path = REPO / "repository.yaml"
    if not path.is_file():
        problems.append("repository.yaml is missing — Home Assistant needs it to add this source")
        return
    data = _load(path)
    if not isinstance(data, dict):
        problems.append("repository.yaml must be a mapping")
        return
    for key in ("name", "url", "maintainer"):
        if not data.get(key):
            problems.append(f"repository.yaml: {key} is missing or empty")


def _check_app(directory: Path, problems: list[str]) -> None:
    where = directory.name
    data = _load(directory / "config.yaml")
    if not isinstance(data, dict):
        problems.append(f"{where}/config.yaml must be a mapping")
        return

    for key in REQUIRED_APP_KEYS:
        if data.get(key) in (None, "", [], {}):
            problems.append(f"{where}: {key} is missing or empty")

    slug = data.get("slug")
    if slug != where:
        problems.append(
            f"{where}: slug is {slug!r}. The directory name is the slug users see in paths "
            "like /addon_configs/<id>_<slug>, so the two must agree"
        )

    version = str(data.get("version", ""))
    if version and not all(part.isdigit() for part in version.split(".")[:3]):
        problems.append(f"{where}: version {version!r} is not the image tag this can pull")

    image = str(data.get("image", ""))
    if ":" in image:
        problems.append(
            f"{where}: image {image!r} carries a tag. The Supervisor appends the `version` "
            "key as the tag, so a tag here is either ignored or wrong"
        )

    arch = data.get("arch") or []
    if isinstance(arch, list):
        for entry in arch:
            if entry not in KNOWN_ARCH:
                problems.append(f"{where}: arch {entry!r} is not one Home Assistant builds for")
        if "{arch}" in image and not arch:
            problems.append(f"{where}: image uses the {{arch}} placeholder but arch is empty")
    else:
        problems.append(f"{where}: arch must be a list")

    if data.get("ingress") and not isinstance(data.get("ingress_port"), int):
        problems.append(f"{where}: ingress is on but ingress_port is not a number")

    options, schema = data.get("options") or {}, data.get("schema") or {}
    if isinstance(options, dict) and isinstance(schema, dict):
        for key in options:
            if key not in schema:
                problems.append(f"{where}: option {key!r} has no entry in schema")

    for required in ("DOCS.md", "translations/en.yaml"):
        if not (directory / required).is_file():
            problems.append(f"{where}: {required} is missing")


def main() -> int:
    problems: list[str] = []
    _check_repository(problems)

    apps = sorted(path.parent for path in REPO.glob("*/config.yaml"))
    if not apps:
        problems.append("no app found — a repository with no app is not one")
    for directory in apps:
        _check_app(directory, problems)

    for problem in problems:
        print(f"error: {problem}", file=sys.stderr)
    if problems:
        return 1
    print(f"{len(apps)} app(s) checked, nothing to report: {', '.join(p.name for p in apps)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
