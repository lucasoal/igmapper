<div align="center">
	<picture>
	<source media="(prefers-color-scheme: dark)" srcset="assets/igmapper.svg">
	<source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/lucasoal/igmapper/refs/heads/main/assets/igmapper.svg">
		<img src="https://raw.githubusercontent.com/lucasoal/igmapper/refs/heads/main/assets/igmapper.svg" width="100%">
	</picture>
	<br><br><br>
	<hr>
<h1>igmapper: An Instagram Unofficial API</h1>

<img src="https://img.shields.io/badge/Author-lucasoal-blue?logo=github&logoColor=white"> <img src="https://img.shields.io/badge/License-MIT-750014.svg"> <!-- <img src="https://img.shields.io/badge/Status-Beta-DF1F72">  -->
<br>
<img src="https://img.shields.io/pypi/v/igmapper.svg?label=Version&color=white"> <img src="https://img.shields.io/pypi/pyversions/igmapper?logo=python&logoColor=white&label=Python"> <img src="https://img.shields.io/badge/Code Style-Black Formatter-111.svg"> 
<br>
<img src="https://static.pepy.tech/badge/igmapper">
<!-- <img src="https://img.shields.io/pypi/dm/igmapper.svg?label=PyPI Downloads"> -->

</div>

## What is it?
**igmapper** is a high-performance Python library designed for Instagram data extraction, 
providing structured access to profiles, feeds, and comments. It offers a flexible
architecture that allows data engineers to toggle between Requests and native CURL
transport, ensuring resilience against environment constraints.

<h2>Table of Contents</h2><br>

- [What is it?](#what-is-it)
- [Main Features](#main-features)
- [Where to get it / Install](#where-to-get-it--install)
- [Documentation](#documentation)
- [License](#license)
- [Dependencies](#dependencies)

## Main Features
Here are just a few of the things that pandas does well:

- [`InstaClient`](doc/DOCUMENTATION.md#instaclient): Initializes the session and handles transport selection (Requests or CURL)
  - [`get_profile_info()`](doc/DOCUMENTATION.md#get_profile_info): Scrapes profile metadata and returns a structured ProfileData object.
  - [`get_feed()`](doc/DOCUMENTATION.md#get_feed): Retrieves user timeline posts with built-in pagination support.
  - [`get_comments()`](doc/DOCUMENTATION.md#get_comments): Fetches media comments and automates cursor-based pagination.

## Where to get it / Install
The source code is currently hosted on GitHub at: https://github.com/lucasoal/igmapper


> [!WARNING]
> It's essential to use [**Python 3.10** 🡽](https://www.python.org/downloads/release/python-310/) version
<!-- > It's essential to **upgrade pip** to the latest version to ensure compatibility with the library. -->
<!-- > ```sh
> # Requires the latest pip
> pip install --upgrade pip
> ``` -->

- [PyPI 🡽](https://pypi.org/project/igmapper/)
	```sh
	# PyPI
	pip install igmapper
	```
- GitHub
	```sh
	# or GitHub
	pip install git+https://github.com/lucasoal/igmapper.git
	```

## Documentation
- [Documentation 🡽](https://github.com/lucasoal/igmapper/blob/main/doc/DOCUMENTATION.md).

## License
- [MIT 🡽](https://github.com/lucasoal/igmapper/blob/main/LICENSE)

## Dependencies
- Requests

See the [full installation instructions](https://github.com/lucasoal/igmapper/blob/main/INSTALLATION.md) for minimum supported versions of required, recommended and optional dependencies.

<hr>

[⇧ Go to Top](#table-of-contents)