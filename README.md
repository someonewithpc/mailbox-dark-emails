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

1. Open `chrome://extensions` and turn on Developer mode
2. Click "Load unpacked" and pick this directory
3. Reload app.mailbox.org
