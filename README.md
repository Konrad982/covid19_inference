[Link to comparison of different countries](scripts/Comparison.html)
# Disclaimer
This repository is a fork of [the Priesemann Group's Covid-19 inference repository](https://github.com/Priesemann-Group/covid19_inference). It aims to apply the model to different datasets (e.g. from the Johns Hopkins University and national authorities) from different countries. There is no liability for correctness of the data, the statistical inference methods or any visible results. Chosen changing points for countries other than Germany reflect my personal judging.

# Copyright information on the data used
Data which may be found in raw or processed form in this repository comes from
- [data.gouv.fr](https://www.data.gouv.fr/en/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/#_), under the [open licence](https://www.etalab.gouv.fr/wp-content/uploads/2018/11/open-licence.pdf)
- [Italian Government GitHub repository](https://github.com/pcm-dpc/COVID-19), under [CC-BY-4.0 licence](https://creativecommons.org/licenses/by/4.0/deed.en)
- [Johns Hopkins University GitHub repository](https://github.com/CSSEGISandData/COVID-19) under the conditions specified there
- [Robert Koch Institut](https://www.rki.de) data retrieved from [here](https://experience.arcgis.com/experience/478220a4c454480e823b17327b2bf1d4) under [Open Data Datenlizenz Deutschland – Namensnennung – Version 2.0](https://www.govdata.de/dl-de/by-2-0)

The exact provenience and retrieval date of the data in any form is (usually) specified in or can be obtained from the relevant notebooks. Processed saved data in this repository should always correspond to a notebook by which it was produced.
# Readme of the Priesemann Group Repository:
# Bayesian inference and forecast of COVID-19, code repository

[![Documentation Status](https://readthedocs.org/projects/covid19-inference/badge/?version=latest)](https://covid19-inference.readthedocs.io/en/latest/doc/gettingstarted.html)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

This is a Bayesian python toolbox for inference and forecast of the spread of the Coronavirus.

Check out our [documentation](https://covid19-inference.readthedocs.io/en/latest/doc/gettingstarted.html).

An example notebook for one bundesland is [here](scripts/example_one_bundesland.ipynb), and for an hierarchical analysis of the bundeslaender [here](scripts/example_bundeslaender.ipynb) (could still have some problems).

The research article [is available on arXiv](https://arxiv.org/abs/2004.01105) (**updated on April 13**).
The code used to produce the figures is available in the other repository [here](https://github.com/Priesemann-Group/covid19_inference_forecast)

)
**We are looking for support** to help us with analyzing other countries and to extend to an hierarchical regional model. We have received additional funding to do so and are recruiting PostDocs, PhD candidates and research assistants:
https://www.ds.mpg.de/3568943/job_full_offer_14729553
https://www.ds.mpg.de/3568926/job_full_offer_14729572
https://www.ds.mpg.de/3568909/job_full_offer_14729591

### Please take notice of the Priesemann Group's [disclaimer](DISCLAIMER.md), which is valid also for this repository.


