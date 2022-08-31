# Rollover Obsidian TODOs in Daily Notes

This is a Python script that can be called from the Obsidian [Templater](https://github.com/SilentVoid13/Templater) 
plugin. Much of this script comes from [obsidian-templater-helpers](https://github.com/JasonBraddy/obsidian-templater-helpers)
but is modified for a daily/periodic note with a custom format (i.e. Thursday, August 25th, 2022). The script looks for
the most recent daily note (doesn't have to be yesterday) and moves any open TODO items to today's daily note.

## Features
- moves a daily/periodic note's open TODOs to a future daily/periodic note upon creation
- the notes don't have to be from adjacent days (i.e. if it's Monday and no daily notes were created over the weekend, it will migrate the TODOs from Friday)
- moves nested open TODOs
- moves bullet points that are nested under an open TODO
- skips empty open TODOs (regardless how nested they are) and removes them from the source note
- skips bullet points that are not nested under a TODO
- skips nested bullet points that are empty and removes them from the source note

**Example:**
- [ ] this open TODO will be moved
  - this nested bullet point under an open TODO will be moved
  - *_pretend this bullet point is empty_ - it **_will not_** be moved and will also be removed from the source note
  - [ ] this nested open TODO will be moved
    - [ ] this double nested open TODO will be moved
- [ ] *_pretend this TODO is empty_ - it **_will not_** be moved and will also be removed from the source note
- this non-nested bullet point **_will not_** be moved
- [x] this completed TODO **_will not_** be moved
  - this bullet point that's nested under a complete TODO **_will not_** be moved

## Templater Settings & Setup
![templater_settings.png](templater_settings.png)

### Invoke Templater User Command Function from Obsidian
The left side ("rollover_todos") is the name of the function as it should be invoked from a
template. A template can be any note inside a folder that is designated as a template
folder in Templater settings.

Here's the [daily note](daily%20note%20template.md) that I use.

`<% tp.user.rollover_todos() %>` is how the custom function is invoked by Templater.

### Setup User Function
On the right side there are three arguments provided:

1. Python path or command (i.e. `path/to/python3` or simply `python3`).
2. Path to python script.
3. [Templater internal function](https://silentvoid13.github.io/Templater/internal-functions/internal-modules/file-module.html#tpfilefolderrelative-boolean--false) that can be passed to the script.
In this case, `<% tp.file.path(false) %>` passes the absolute path of the note that's invoking the script.