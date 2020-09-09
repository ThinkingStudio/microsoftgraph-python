# microsoft-python
Microsoft graph API wrapper for Microsoft Graph written in Python.

## Installing
```
pip install ts-microsoftgraph-python
```

## Usage
Read the [docs](docs/index.md)

## Changelog

### 2020-09-10 version 0.2.0
* Forked from https://github.com/jkmartindale/microsoftgraph-python - but took master branch and reapplied the swap of authority URLs
* Renamed the project so it can be published on PyPi since the original is not really being maintained
* Breaking changes from the forked project, totally different coherent naming convention for methods
* Fixed issues with O365 vs MS authentication being opposite to what you would expect (this is an issue that was identified upstream)
* Added documentation for the calls and split the old README up into those pages - TODO: add to this documentation, especially the `Auth` class
* Added proper support for reading mailboxes and traversing mail folders
* Added support for chaining-calls of paginated data using the ODATA 'header' 
* Complete overhaul of Auth and support for scopes - all of this was way too complex and really didn't help you get your app
working quickly. I hope that the Auth and AuthScope objects greatly reduce the angst in figuring out how to use this API.

