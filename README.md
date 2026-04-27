# F1 Race Intelligence — Fabric Data Agent

I built this project to explore Microsoft Fabric's Data Agent capability using a dataset I actually care about — Formula 1. The idea was simple: take 70 years of F1 data, model it properly, and see if I could get an AI agent to answer real racing questions in plain English without writing a single SQL query.

---

## What this does

You connect to the agent and ask things like:

- *"Who won the 2019 Monaco Grand Prix?"*
- *"How many times did Schumacher win the championship?"*
- *"Which constructor had the most DNFs in 2012?"*

The agent figures out the SQL, runs it against the Lakehouse, and gives you an answer. No dashboards, no filters, just a question.

---

## The data

Sourced from [this Kaggle dataset](https://www.kaggle.com/datasets/rohanrao/formula-1-world-championship-1950-2020) — F1 results from 1950 to 2020. It came as 14 CSV files which I renamed with Dim/Fact prefixes before loading.

**Dimension tables** — the reference data:

| Table | What's in it | Rows |
|---|---|---|
| Dim_Circuits | Track name, country, location | 76 |
| Dim_Drivers | Driver name, DOB, nationality | 856 |
| Dim_Constructors | Team name, nationality | 211 |
| Dim_Races | Race name, year, round, date | 1,101 |
| Dim_Seasons | Season years | 74 |
| Dim_Status | Finish status (Finished, Engine, Accident...) | 139 |

**Fact tables** — the events and results:

| Table | What's in it | Rows |
|---|---|---|
| Fact_Results | Every driver's result per race | 25,839 |
| Fact_LapTimes | Lap-by-lap timing data | 538,121 |
| Fact_PitStops | Pit stop durations and laps | 9,634 |
| Fact_Qualifying | Q1/Q2/Q3 times per driver | 9,574 |
| Fact_DriverStandings | Championship points after each race | 33,902 |
| Fact_ConstructorStandings | Constructor points after each race | 12,941 |
| Fact_ConstructorResults | Points per constructor per race | 12,169 |
| Fact_SprintResults | Sprint race results | 119 |

---

## How it's built

**Storage:** Files live in Azure Blob Storage, authenticated via SAS token stored in the Lakehouse.

**Loading:** PySpark notebook reads each CSV from blob and writes it as a Delta table into the Fabric Lakehouse. The SAS credentials are read from a JSON file rather than hardcoded.

**Agent setup:** Three things needed configuring —
- Agent instructions (what the agent is, what data it covers, how to behave)
- Data source instructions (the non-obvious rules — like always use `positionOrder` not `position` for race winners, and always filter to `MAX(round)` for season champions)
- Example queries (question + SQL pairs that teach the agent the correct patterns for your specific schema)

**Testing:** There's a notebook that reads a CSV of test questions, runs the SQL directly against the endpoint, and compares the output. Useful for catching regressions when you update the agent config.

---

## Stuff I learned the hard way

**`position` vs `positionOrder`** — `position` in the results table is nullable (NULL for DNFs). `positionOrder` is always populated. Without this the agent returns empty results for race winners.

**Season champion logic** — you can't just filter `WHERE position = 1` in the standings table. That gives you the leader after every single race. You need to filter to the last round of the season: `WHERE round = (SELECT MAX(round) FROM dim_races WHERE year = X)`.

**SAS token expiry** — if your notebook suddenly throws an Azure authentication error overnight and nothing changed in the code, it's the SAS token. They expire. Regenerate and re-run from the top.

**Example queries are not for simple questions** — the agent handles straightforward lookups fine on its own. Example queries are worth adding only when your schema has non-obvious logic the agent can't guess — like which table to use for wins, or how status codes work in a separate dimension table.

---

## Repo structure

```
F1-Fabric-Data-Agent/
├── README.md
├── 1_data/
│   └── processed/          renamed CSV files (Dim_ and Fact_ prefix)
├── 2_notebooks/
│   ├── DataLoading.py      reads from blob, writes Delta tables to Lakehouse
│   └── AutomatedTesting.py runs test questions against SQL endpoint
├── 3_agent_config/
│   ├── agent_instructions.md
│   ├── datasource_instructions.md
│   └── f1_example_queries.json
├── 4_sql_queries/
│   └── f1examplequeries.docx
└── 5_testing/
    └── AutomatedTestSheet.csv
```

---

## Setup

1. Download the dataset from Kaggle and rename the files with Dim/Fact prefixes
2. Upload to Azure Blob Storage, generate a SAS token, save to `sascredentials.json` in Lakehouse Files
3. Run `DataLoading.py` — it reads the token from the JSON and loads all 14 tables
4. Create a Data Agent in Fabric, attach the Lakehouse, paste the instructions, import the example queries JSON
5. Publish and test

Don't commit `sascredentials.json` to GitHub.

---

## Stack

Microsoft Fabric · Azure Blob Storage · PySpark · Delta Lake · T-SQL · Fabric Data Agent
