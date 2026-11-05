# Second opinion

Ask another agent to review a chat's changes. It reads them without changing anything, and its findings arrive as comments in Review for you to send or delete.

An [Abstract](https://github.com/endeken-com/abstract) plugin. It shipped inside the app
until ABS-190 moved it here, with its history.

## Install

In Abstract, Settings › Plugins lists it from the reviewed registry, or use
**Add from GitHub…** or the command line:

```sh
abstract plugin add abstract-ade/second-opinion
```

That installs the commit the [registry](https://github.com/abstract-ade/abstract-plugins)
approved. `abstract plugin add abstract-ade/abstract-plugin-second-opinion` installs this
repository's latest commit instead, marked "Not reviewed".

## What it can access

- See your chats
- See when your agents worked
- Read messages in the projects you pick
- Keep its own settings
- Start chats
- Send messages to your chats
- Add review comments

You review this list when you turn it on, and an update that asks for more stays off
until you review it again.

## Development

The plugin is the repository's root: `manifest.json` and the files beside it. Only
those are installed; `.gitattributes` keeps this README, `Tests/` and `.github/` out of
the package. There is no build step.

CI checks the package the way Abstract does (`.github/check-package.py`) and runs
`Tests/` inside Abstract's own test target, against Abstract's `main`.
To run them locally, from a checkout of `endeken-com/abstract`:

```sh
package=Abstract/Resources/Plugins/second-opinion.abstractplugin
rm -rf "$package" && mkdir -p "$package"
git -C ../abstract-plugin-second-opinion archive HEAD | tar -x -C "$package"
cp ../abstract-plugin-second-opinion/Tests/*.swift Packages/AbstractCore/Tests/AbstractCoreTests/
[ -d ../abstract-plugin-second-opinion/Tests/Fixtures ] &&
  cp -R ../abstract-plugin-second-opinion/Tests/Fixtures/. Packages/AbstractCore/Tests/AbstractCoreTests/Fixtures/
cd Packages/AbstractCore && swift test --filter SecondOpinionPluginTests
```

A new version needs a pull request to the registry with the new commit before
people who installed the listing are offered it.
