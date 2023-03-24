# Welcome!

Hi! Please feel absolutely free to make PRs here, if you have features or bugfixes or _especially_ additions to documentation. This is a kind space, and new pythonistas are absolutely welcome.

If you're creating an issue, please do check if the issue you're running into has already been reported. If your issue is well-suited to a new contributor, please mark it as a good first issue.

## Development

This project is built using (vulcan-py)[https://github.com/optiver/vulcan-py]. This should not matter for typical development workflows, but is worth mentioning for powerusers. For typical development, the following should suffice:

```bash
$ git clone git@github.com:Thirdegree/language-server-protocol.git
$ cd language-server-protocol
$ python3.11 -m venv .venv
$ source .venv/bin/activate
$ pip install -e .
```

See (tox.inin)[./tox.ini] for the various development dependencies required.
