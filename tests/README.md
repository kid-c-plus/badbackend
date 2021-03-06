# Test Suite

Test items for Bad Backend.

## Requirements

- [Icecast](https://icecast.org)
- `pidof` bash command (installable on Mac OS using `brew install pidof`)

## Use

Set the shebang in runtests.py to the location of your Python 3 interpreter and run `./runtests.py`. It accepts a list of submodules to test - leave it blank to run all.
These tests are configured for Unix and use Bash system calls. Some modification will be required to run these tests in a Windows evironment

### Submodules Available by Default

- IcecastStatus
- Server

### Adding Tests

Add UnitTest subclasses to tests.py and provide the name of your subclass to the list of submodules passed to `./runtests.py`.
