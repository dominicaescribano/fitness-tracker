# Fitness Tracker

A simple calorie and weight tracking app built with Python and Streamlit. Allows users to log their daily weight and caloric intake and visualize the trend of their weight over time, filtering out the noise of day-to-day weight fluctuations that make it difficult to interpret the effects of their current diet.

## What it does

- **Daily logging**: Provides a UI for users to log weight, calories, protein, steps, and notes for each day.
- **Weight trend visualization**: Visualizes the 7-day rolling average for the user in addition to daily weight data, showing the real weight trend over time.
- **TDEE estimation**: Calculates the user's total daily energy expenditure (TDEE) based on weight change and caloric intake history. A confidence scoring is also shown, calculated based on how much data the user has logged so far.
- **Weight projection**: Estimates where the user's weight will be in 30 days based on their current weight trend.
- **Multi-user support**: Enables separate tracking for two users with shared database.

## Tech stack

- **Python** -> Core application logic and analytics
- **Streamlit** -> Web UI
- **SQLite** -> Local database
- **Plotly** -> Interactive charts
- **pytest** -> Unit tests
- **GitHub Actions** -> CI pipeline that runs tests on every push

## Project structure

```
fitness-tracker/
├── app/
│   ├── main.py          # Streamlit UI
│   ├── analytics.py     # TDEE calculation, rolling averages, projections
│   ├── database.py      # SQLite data access layer
│   └── charts.py        # Plotly chart builders
├── tests/
│   └── test_analytics.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── requirements.txt
└── README.md
```

## Running locally

1. Clone the repository

```bash
git clone https://github.com/dominicaescribano/fitness-tracker.git
cd fitness-tracker
```

2. Create and activate a virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Run the app

```bash
python -m streamlit run app/main.py
```

5. Run the tests

```bash
pytest -v
```

## How the TDEE estimate works

Rather than using population-average formulas based on height, weight, and activity level (like Harris-Benedict), the app estimates the user's TDEE directly from their personal data.

The app tracks weekly change in weight from the user's 7-day rolling averages, combined with the average number of calories logged for those days. Assuming the 3,500 calories-per-pound energy model, the app will derive how many calories the user would need to level their weight trend. This means the estimate improves over time and reflects the user's actual metabolism. The confidence score reflects how much data is available for the estimate. Two weeks of data will result in a lower confidence score than four or more weeks of data.

## Data layer

The app uses a three-table SQLite schema that mirrors a simplified data warehouse pattern:

- **users**: User profiles and targets
- **daily_log**: Raw daily entries (weight, calories, protein, steps)
- **tdee_estimates**: Calculated analytics layer

Raw data is never modified; all analytics are derived on read.