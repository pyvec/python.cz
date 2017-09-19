
# python.cz

Czech Python community homepage

[![Build Status](https://travis-ci.org/pyvec/python.cz.svg?branch=master)](https://travis-ci.org/pyvec/python.cz)
[![Test Coverage](https://coveralls.io/repos/github/pyvec/python.cz/badge.svg?branch=master)](https://coveralls.io/github/pyvec/python.cz?branch=master)

### Requirements

-  The code is **Python 3** (the production Python version is 3.4)
-  The site uses GitHub API. For certian pages to work correctly, you need to set the `GITHUB_TOKEN` environment variable to a [GitHub Personal Access Token](https://github.com/settings/tokens) (no scopes needed)

### Get Started

#### Development

Installation:

```sh
$ pip install -e .[tests]
```

Development server:

```sh
$ export GITHUB_TOKEN=...
$ pythoncz run
```

#### Production

Installation:

```sh
$ pip install .
$ pip install gunicorn
```

Server:

```sh
$ export GITHUB_TOKEN=...
$ gunicorn pythoncz.app:app
```

**Note:** The above won't work locally on your development machine, unless you set an environment variable `SERVER_NAME` to something like `localhost:8000`. Then access the site from `localhost:8000` in your browser.

### Deployment

The site gets automatically deployed after any push to the `master` branch. See [documentation in the `deployment` directory](deployment/README.md).

-   **Hosting:** [Rosti.cz](https://rosti.cz/)<br>
    Access: [Pyvec](http://pyvec.org/)

-   **Domain:** bestowed by [KRAXNET](http://www.kraxnet.cz/)<br>
    Access: e-mail request to [KRAXNET](http://www.kraxnet.cz/)

-   **Monitoring:** [UptimeRobot](https://uptimerobot.com/)<br>
    Access: [@honzajavorek](http://github.com/honzajavorek)

-   **Analytics:** [Google Analytics](http://www.google.com/analytics/)<br>
    Access: [@honzajavorek](http://github.com/honzajavorek), [@encukou](http://github.com/encukou), [@martinbilek](http://github.com/martinbilek), [@benabraham](http://github.com/benabraham)

## Authors & Contributions

**This site is community effort and contributions are very welcome!** See the [Hall of fame](https://github.com/pyvec/python.cz/graphs/contributors) for the most active contributors.

The site is backed by [Pyvec](http://pyvec.org/), nonprofit organization dedicated to support of Python in the Czech Republic. [Honza Javorek](http://github.com/honzajavorek) is the original author, core commiter and maintainer of python.cz.

## License

[MIT](LICENSE)
