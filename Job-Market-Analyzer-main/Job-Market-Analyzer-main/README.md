# Job Market Analyzer

An interactive dashboard that explores the data science job market using 660+ real Glassdoor job postings. It answers questions like which skills employers ask for most, which roles pay best, and where the hiring is happening.

🔗 **Live Demo**: [add your Streamlit app URL here]

## Features

- Summary metrics: total postings, average salary, number of states hiring, number of companies
- Most in-demand skills (Python, Excel, Hadoop, Spark, AWS, Tableau, Big Data)
- Average salary by job role
- Top 10 hiring states, shown with full state names
- Salary distribution across all postings
- Sidebar filters for job role and state, so every chart and metric updates together

## Tech Stack

- **Python** for the application logic
- **Pandas** for data cleaning and analysis
- **Plotly** for interactive charts
- **Streamlit** for the dashboard and deployment

## Dataset

[Data Science Job Postings on Glassdoor](https://www.kaggle.com/datasets/rashikrahmanpritom/data-science-job-posting-on-glassdoor) from Kaggle. It has 660 postings with 27 columns, including job title, salary estimate, company rating, location, industry, seniority, and flags for skills mentioned in each posting.

## Data Cleaning

- Converted the average salary column to numeric and dropped rows without a salary
- Stripped stray whitespace from state codes (values like `' NY'` would not match otherwise)
- Mapped state abbreviations to full names for readable filters and charts

## Key Insights

- Data Scientist is by far the most common role in the dataset (447 of 660 postings)
- California has the most openings (165 postings), followed by Virginia and Massachusetts
- Average salary across postings is about $124k, with a wide range from $43k to $271k

## Run Locally

```bash
git clone https://github.com/asxfhussain/job-market-analyzer.git
cd job-market-analyzer
pip install -r requirements.txt
streamlit run app.py
```

## Project Structure

```
job-market-analyzer/
├── app.py              # Streamlit dashboard
├── Cleaned_DS_jobs.csv # Dataset
├── requirements.txt    # Dependencies
└── README.md
```

## Future Improvements

- Add a skills vs salary comparison
- Add company rating and industry breakdowns
- Extend the data with more recent postings
