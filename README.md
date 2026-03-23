# acs-nativity-streamlit

[![CI](https://github.com/arilamstein/acs-nativity-streamlit/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/arilamstein/acs-nativity-streamlit/actions/workflows/python-app.yml)

A Streamlit web app for exploring trends in nativity data in the United States. The app uses the [`acs-nativity`](https://github.com/arilamstein/acs-nativity) package to download and visualize data from the [American Community Survey (ACS) 1‑year estimates](https://www.census.gov/data/developers/data-sets/acs-1year.html). Users can explore all available data (2005-2024) for the nation, all states, and all counties and places (i.e. cities) with a population of 65,000 or more.

View the app **[here](https://acs-nativity.streamlit.app/)**.

## Adding New Data

When new ACS 1‑year estimates are released (typically each July):

1. Update the constant `END_YEAR` in `scripts/gen_data.py`.
2. From the project root, run:

   ```bash
   make data
   ```

   That will update all the files in the `data/` directory with latest available data.
3. Commit the updated CSVs and push to GitHub. Streamlit Cloud will automatically redeploy the app.

## Development workflow

Before committing any changes, run:

```bash
make check
```

This runs the same checks used in CI: 
  * `ruff format` 
  * `ruff check` 
  * `mypy .`
  
These commands help ensure the codebase stays clean, consistent, and type‑safe.
