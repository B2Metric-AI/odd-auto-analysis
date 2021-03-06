# ODD Auto Analysis
This project is an interactive web dash prepared using automobile market data in Turkey.

Through the application you can see the share of auto brands sales of amount in Turkey.You can also see visualizations of data according to these selections by selecting brand and specific date ranges.

## Getting Started

Analysis was performed using AUTOMOTIVE DISTRIBUTERS ASSOCIATION (ODD) data in this application. ODD data can be found on [this page](http://www.odd.org.tr/web_2837_1/neuralnetwork.aspx?type=73).

### Running the app locally

First create a virtual environment with conda or venv inside a temp folder, then activate it.

```
virtualenv odd-auto-analysis-venv

# Windows
odd-auto-analysis-venv\Scripts\activate
# Or Linux
source  odd-auto-analysis-venv/bin/activate
```

Clone the git repo, then install the requirements with pip:
```
git clone https://github.com/b2metric-automl/odd-auto-analysis.git
cd odd-auto-analysis
pip install -r requirements.txt
```
Run the app
```
python app.py
```
![animated1](odd-auto-b2metric.gif)
