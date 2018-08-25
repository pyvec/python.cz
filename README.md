
# python.cz

Czech Python community homepage.

[![Build Status](https://travis-ci.org/pyvec/python.cz.svg?branch=master)](https://travis-ci.org/pyvec/python.cz)
[![Test Coverage](https://coveralls.io/repos/github/pyvec/python.cz/badge.svg?branch=master)](https://coveralls.io/github/pyvec/python.cz?branch=master)

## Installation

The code is **Python 3** (the production Python version is 3.6).

```sh
$ pip install .
```

### Development

The site uses GitHub API. For certian pages to work correctly, you need to set the `GITHUB_TOKEN` environment variable to a [GitHub Personal Access Token](https://github.com/settings/tokens) (no scopes needed).

```sh
$ export GITHUB_TOKEN=...
$ python runserver.py --help
```

### Deployment

The site gets automatically deployed after any push to the `master` branch.
It is frozen by [Elsa](https://github.com/pyvec/elsa). A cron job redeploys
it daily, so any content of dynamic nature isn't outdated.

-   **Domain:** bestowed by [KRAXNET](http://www.kraxnet.cz/)<br>
    Access: e-mail request to [KRAXNET](http://www.kraxnet.cz/)
-   **Analytics:** [Google Analytics](http://www.google.com/analytics/)<br>
    Access: [@honzajavorek](http://github.com/honzajavorek), [@encukou](http://github.com/encukou), [@martinbilek](http://github.com/martinbilek), [@benabraham](http://github.com/benabraham)

## Authors & Contributions

**This site is community effort and contributions are very welcome!** See the [Hall of fame](https://github.com/pyvec/python.cz/graphs/contributors) for the most active contributors.

The site is backed by [Pyvec](http://pyvec.org/), nonprofit organization dedicated to support of Python in the Czech Republic. [Honza Javorek](http://github.com/honzajavorek) is the original author, core commiter and maintainer of python.cz.

## License

[MIT](LICENSE)
