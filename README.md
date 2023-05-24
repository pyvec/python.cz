<h1 align="center">⚠️</h1>
<h3 align="center">Tento projekt nemá aktuálně nikoho, kdo by se o něj staral</h3>
<h4 align="center">Lákalo by tě python.cz udržovat, rozvíjet, nebo to celé předělat? <a href="https://docs.pyvec.org/operations/support.html#sit-kontaktu">Ozvi se na Slacku!</a></h4>
<hr>

# python.cz

Czech Python community homepage.

## Installation

The code is **Python 3.7**.

1.  [Install Pipenv](https://pipenv.readthedocs.io/en/latest/install/#installing-pipenv)
1.  Clone the project:

    ```sh
    $ git clone git@github.com:pyvec/python.cz.git --depth=10
    ```

    It is recommended to start with a [shallow clone](https://git-scm.com/docs/git-clone#git-clone---depthltdepthgt) as historically, this repo has contained a lot of rather large photos.
1.  Go inside the project directory and run Pipenv to install dependencies:

    ```
    $ cd ./python.cz
    $ pipenv install --dev
    ```

### Development

The site uses GitHub API. For certain pages to work correctly, you need to set the `GITHUB_TOKEN` environment variable to a [GitHub Personal Access Token](https://github.com/settings/tokens) (no scopes needed).

```sh
$ export GITHUB_TOKEN=...
$ pipenv run serve
```

### Deployment

The site gets automatically deployed after any push to the `master` branch. It is frozen by [Elsa](https://github.com/pyvec/elsa). A GitHub action redeploys it daily, so any content of dynamic nature isn't outdated.

-   **Domain:** bestowed by [KRAXNET](http://www.kraxnet.cz/)<br>
    Access: e-mail request to [KRAXNET](http://www.kraxnet.cz/)
-   **Public Analytics:** [Simple Analytics](https://simpleanalytics.com/python.cz)<br>
    Access: [@honzajavorek](http://github.com/honzajavorek)

## Authors & Contributions

**This site is community effort and contributions are very welcome!** See the [Hall of fame](https://github.com/pyvec/python.cz/graphs/contributors) for the most active contributors.

The site is backed by [Pyvec](http://pyvec.org/), nonprofit organization dedicated to support of Python in the Czech Republic. [Honza Javorek](http://github.com/honzajavorek) is the original author, the [@pyvec/python-cz](https://github.com/orgs/pyvec/teams/python-cz) are python.cz maintainers.

## License

[MIT](LICENSE)
