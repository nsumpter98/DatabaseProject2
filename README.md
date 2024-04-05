
# Missing Data Handler in Django

## Introduction
This Django project provides a comprehensive solution for handling missing data in customer datasets. By implementing various techniques for dealing with missing values in different attributes, the application ensures data integrity and usability for analysis or machine learning tasks. The project features a user-friendly GUI for easy interaction with the data handling methods.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)


## Installation

Before installation, ensure you have Python and Django installed on your system. Follow these steps to set up the project:

1. Clone the repository to your local machine:
   ```
   git clone <repository_url>
   ```
2. Navigate to the project directory:
   ```
   cd <project_directory>
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the Django server and access the GUI:
```
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your web browser to interact with the application.

### Handling Missing Data

Choose the method for handling missing data directly from the GUI:
- Substitution with mean for numeric attributes
- Substitution with median for numeric attributes
- Substitution with mode for categorical attributes
- Predictive modeling-based imputation for numeric attributes

## Features

- **Multiple Imputation Techniques**: Offers several strategies for imputing missing values in customer datasets.
- **Graphical User Interface**: Easy-to-use web interface for selecting imputation methods and viewing results.
- **Missing Values Report**: Generates reports on missing data using Jupyter Notebooks, including statistics and counts of missing values per attribute.
- **Predictive Modeling-Based Imputation**: Incorporates machine learning models for sophisticated imputation techniques.
