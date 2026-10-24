# mailbox.org email colours

A Chrome extension for mailbox.org's web mail with Chrome's auto dark mode
(`chrome://flags/#enable-force-dark`) turned on.

OX App Suite shows each email in an iframe on a white panel. With the dark
theme on, Chrome's auto dark mode only gets part of it right:

- HTML emails get darkened, but the white panel and the frame's bare canvas
  around them don't, so you see a dark box on a white page
- Plain-text emails don't get darkened at all, because OX declares a dark colour
  scheme on their frame, and Chrome skips any page that says it handles dark
  itself. Text stays black on white, with light-grey links
- The compose editor shows white text on white. Auto dark mode turns its
  default text white, but the editor's frame has no background of its own, and
  the white behind it belongs to the app, which auto dark mode leaves alone

The extension gives every email frame and the editor a light colour scheme and
an explicit white background. Chrome's auto dark mode then darkens the whole
frame with its own algorithm, and the extension clears the white panel behind
emails. Plain-text links get a proper link colour.

Turn "Show emails dark" off in the toolbar popup to keep emails and the editor
light instead. The frames then get `color-scheme: only light`, which tells auto
dark mode to leave them alone. The change applies to the next email you open or
write.

## Install

Chrome on Linux installs it from a managed policy. Put this in
`/etc/opt/chrome/policies/managed/mailbox-dark-emails.json` (for Chromium,
`/etc/chromium/policies/managed/`):

```json
{
  "ExtensionInstallForcelist": [
    "ccgjbgfofdpngcfncgfeajfpohndfhim;https://someonewithpc.github.io/mailbox-dark-emails/updates.xml"
  ]
}
```

Restart Chrome and it installs the extension, then picks up new releases from
the same URL by itself. Chrome on Windows and macOS only accepts this from
machines in a managed domain.

To work on it, load it unpacked instead. Open `chrome://extensions`, turn on
Developer mode, click "Load unpacked" and pick this directory. Remove the
policy first, or Chrome will show both copies.

## Releasing

Bump `version` in `manifest.json`, commit, and push a matching `v<version>`
tag. The release workflow signs the extension with the key in the `CRX_KEY`
secret and publishes the `.crx` and `updates.xml` to GitHub Pages. The key
fixes the extension ID, so a new key means a new extension.

`scripts/pack.py <key.pem> <out-dir> <base-url>` does the same packing locally.
