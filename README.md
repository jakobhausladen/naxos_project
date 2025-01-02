# An Analysis of the Naxos Catalog

## Overview

For this project, data from the music catalog of the Naxos Group, which has a large number of classical music labels in its portfolio, was scraped and analyzed.

The data was analyzed in terms of changes in genre distribution, the development and acquisition of sub-labels and the (lack of) improvement in gender representation. A network graph was created to illustrate the musical landscape of the catalog.

The results were published in a [Medium article](https://medium.com/@jakob.hausladen/exploring-the-naxos-catalogue-ac8a9b2705ba).


## Repository Contents

- **Data**:
  - **Not Included**: Data is proprietary to Naxos and is not provided in this repository.

- **Data Collection**:
  - Code for setting up and normalizing the database.
  - Scrapy project for web scraping (relies primarily on XMLHttpRequests).

- **Analysis**:
  - Jupyter Notebooks for analyzing genre trends, label developments, and gender representation.
  - SQL queries for preparing network graph data.
  - Gephi project files and resulting images.

## Copyright Note

All data used in this analysis is copyrighted by Naxos and was scraped and analyzed with their permission. If you wish to use the Scrapy project or any related tools from this repository, please obtain permission from Naxos first.
