
# Deployment at [Rosti.cz](https://rosti.cz/)

## Initial Setup

-   Register at [Rosti.cz](https://rosti.cz/), create an app with SSH access.
-   Clear default contents:

    ```
    $ rm -rf /srv/app
    ```

-   Clone the repository:

    ```
    $ git clone https://github.com/pyvec/python.cz /srv/app
    ```

-   Install:

    ```
    $ cd /srv/app
    $ pip install -r requirements.txt
    ```

-   Restart [Supervisor](http://supervisord.org/):

    ```
    $ supervisorctl restart app
    ```

    The `app.py` file in the root of the project is used as WSGI endpoint.

-   The app should be up and running (e.g. [pythoncz-0375.rostiapp.cz](http://pythoncz-0375.rostiapp.cz/)).

## Continuous Deployment

Continuous deployment means your app gets automatically deployed if continuous integration (CI) build was successful. When turned on only for the `master` branch, the app gets deployed every time someone pushes to `master`, including merged GitHub Pull Requests.

[Travis CI](http://travis-ci.org/) supports continuous deployment out of the box [for various PaaS services](http://docs.travis-ci.com/user/deployment/). [Rosti.cz](https://rosti.cz/) is not among them, but [it's possible to setup also your own deployment](http://docs.travis-ci.com/user/deployment/script/) using the `script` keyword.

### Setup, step by step

-   Create an SSH key which is going to be used for deployment. Make sure it is *without passphrase* as you, obviously, won't be able to interactively type in the password at the end of your TravisCI builds.

    ```
    $ ssh-keygen -t rsa -b 4096 -C "info@pyvec.org"
    ...
    $ ssh-add ~/.ssh/id_rsa_pyvec_deployment
    ```

-   Upload the public key to the production server. First, you need to prepare the server so it has `authorized_keys` available - follow instructions from the [Rosti.cz documentation](https://docs.rosti.cz/base/#ssh). Then upload the public key:

    ```
    $ ssh-copy-id -i ~/.ssh/id_rsa_pyvec_deployment.pub app@pluto.rosti.cz -p 10365  # see Rosti.cz administration for username, host, port...
    ```

-   Encrypt the private key. See [documentation for encrypting files](http://docs.travis-ci.com/user/encrypting-files/). Please be aware that the encryption is repository-specific. Even if using the same private key for multiple projects, it needs to be re-encrypted individually for each of them.

    ```
    $ gem install travis
    $ travis login --auto
    $ travis encrypt-file id_rsa_pyvec_deployment
    ```

    Follow instructions of the `travis encrypt-file` output. You need to add decrypting command to your build. This repository has it in the `deployment/deploy.sh` script.

-   Make sure the deploy is going to happen. Update `.travis.yml` with custom deployment settings:

    ```yaml
    deploy:
        provider: "script"
        script: "deployment/deploy.sh"
        on:
            branch: "master"
            python: "3.4"
            repo: "pyvec/python.cz"
    ```

    This triggers `deploy.sh` script only for `master` branch with Python 3.4.

-   The `deploy.sh` script, executed within the TravisCI build, does three things:

    1.   Decrypts the private key (see above).
    2.   Connects to the production machine via SSH and executes the `update.sh` script.
    3.   Deletes the decrypted private key.

-   The `update.sh` script, executed on the production machine, does four things:

    1.   Deletes all source code of the current app.
    2.   Uses `git` to get the latest source code in the `master` branch.
    3.   Installs dependencies (plain simple `pip install -r requirements.txt`).
    4.   Restarts the app ([specific to Rosti.cz](https://docs.rosti.cz/apps/python/#supervisor)).
