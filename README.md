# Template:

*CI*

[![carlomazzaferro](https://circleci.com/gh/carlomazzaferro/scikit-hts-examples.svg?style=svg)](https://circleci.com/gh/carlomazzaferro/scikit-hts-examples)

*Docker Image*

[![](https://images.microbadger.com/badges/image/carlomazzaferro/scikit-hts-examples:0.2.2.svg)](https://microbadger.com/images/carlomazzaferro/scikit-hts-examples:0.2.2 "Get your own image badge on microbadger.com")
[![](https://images.microbadger.com/badges/version/carlomazzaferro/scikit-hts-examples:0.2.2.svg)](https://microbadger.com/images/carlomazzaferro/scikit-hts-examples:0.2.2 "Get your own version badge on microbadger.com")


Scikit-hts examples
==============================

The scaffolding for this project was based on 
[cookiecutter data science](https://drivendata.github.io/cookiecutter-data-science/)
and it contains code related to [scikit-hts](https://github.com/carlomazzaferro/scikit-hts)

Namely, you'll find usage examples. 

Installation
------------

*If you wish to get the notebooks up and running with a single command, look at the `docker` section below*

Requirements:

- `make`
- `python3.7`, `pip3` and `virtualenv` available in the system's path

###  Install required and optional dependencies

**all dependencies at once**

```bash
$ make install-all
```

**base dependencies only**

```bash
$ make install
```

**base + geo dependencies**

```bash
$ make install-geo
```

**base + auto arima dependencies**

```bash
$ make install-auto-arima
```

**base + auto prophet dependencies**

```bash
$ make install-prophet
```

And then, run 

```bash
$ source venv/bin activate 
$ jupyter lab 
```

Docker
------

Simply:

```bash
$ docker run carlomazzaferro/scikit-hts-examples:0.2.2
```




