<!--
SPDX-FileCopyrightText: 2026 The MCUHome Contributors
SPDX-License-Identifier: Apache-2.0
-->

# MCUHome Dashboard

This version is an early preview of the new web interface, running on
built-in sample data. There is no back end behind it yet: nothing you see
here is a real device or file, and no change you make is saved. Building
and flashing firmware do not work yet either. The rest of this page
describes what the app is going to do.

Create, build and manage Zephyr-based smart home devices from your
browser. Describe a device in YAML — board, sensors, what it reports —
and MCUHome turns it into firmware that commissions into Home Assistant
over Matter.

## Installing

Open the app and click **Open Web UI**. There is nothing to configure
first: the app creates its project directory on first start.

Only Home Assistant **administrators** can change or build anything.
Everyone else sees the project read-only. This is decided per request
from the Home Assistant user behind the ingress session, so it needs no
second password.

## Where your files are

The project lives in this app's own configuration directory. From a file
editor — Studio Code Server, for example — that is:

```
/addon_configs/<id>_mcuhome-ui/
```

The `<id>` prefix is assigned by Home Assistant. Everything a device is
made of is in there as plain files: `devices/<name>/main.yaml`,
`secrets/`, and shared pieces. You can edit them in the browser, in a
file editor, or keep the directory in git — the dashboard notices changes
either way.

The app maps nothing else. It cannot read or write your Home Assistant
configuration.

## Building firmware

**Building needs a build server, and this app is not one.** Compiling
Zephyr and Matter needs a toolchain of several gigabytes and more memory
than a Home Assistant host usually has to spare, so the dashboard never
compiles: it sends the build somewhere that can, and signs the result
here, where the signing key is.

Everything else — creating devices, editing and validating configurations,
drawing commissioning credentials — works without one.

## The firmware signing key

MCUHome signs every image with a key that is generated on first need and
stored in this app's private data directory. That key is the trust anchor
of every device you bootstrap: its public half goes into the device's
bootloader, and a device accepts only firmware signed by it.

**It is in your Home Assistant backups.** Keep them. Losing the key means
every device already bootstrapped has to be bootstrapped again, by hand,
with physical access.

## Why this app asks for administrator access to the Supervisor

Home Assistant's ingress tells an app *which* user is asking. It does not
say whether that user is an administrator — and that is exactly the line
between reading a configuration and changing or building one. The answer
comes from the Supervisor's own user list, which is open to the admin role
alone.

If the app cannot reach it, it fails closed: everyone is read-only.

## Support

Issues and questions:
[github.com/mcu-home/mcuhome-ui/issues](https://github.com/mcu-home/mcuhome-ui/issues)
