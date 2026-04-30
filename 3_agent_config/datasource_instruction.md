Data source description
Describe what's in this data source, what it represents, and why someone might use it to answer a question. Learn more
The F1 Race Intelligence Lakehouse contains Formula 1 racing data covering all seasons from 1950 to 2023. It includes race results, driver and constructor championship standings, lap times, pit stop events, circuit information, and driver/team reference data. Use this source for any questions about F1 race history, championship battles, driver performance, team statistics, and circuit records.

Data source instructions
For each connected data source, help the data agent understand its data and how to use it most effectively. Learn more
Format:
Markdown







Use Tab to navigate between formatting options, Enter or Space to activate
1428/15000 characters used
Data Range
This data source covers Formula 1 seasons from 1950 to 2023 only.

NEVER reference events, drivers, or results beyond the 2023 season
When asked about "current" or "latest", always refer to 2023as the most recent season available
Always Join Through dim_races for Season Filtering
Every fact table connects to seasons through dim_races via raceId.

NEVER filter by year directly on a fact table
ALWAYS join fact tables → dim_races to apply any year or season filter
Championship Winners
To find a season championship winner:

Use fact_driver_standings or fact_constructor_standings
ALWAYS filter to the LAST round of the season (MAX round)
ALWAYS filter WHERE position = 1
Race Winners and Podiums
Use fact_results WHERE positionOrder = 1 for race winners
Use fact_results WHERE positionOrder <= 3 for podiums
position column can be NULL for DNFs — always use positionOrder for ranking
DNF and Retirement Analysis
Use dim_status joined to fact_results on statusId
"Finished" and "+1 Lap", "+2 Laps" etc. are classified as race finishers
Everything else (Engine, Accident, Collision etc.) is a DNFetirement
Pit Stop and Lap Time Data
fact_pit_stops and fact_lap_times data is most complete from the 1990s onward
Early era data (1950s–1960s) may have incomplete lap time and pit stop records — flag this when relevant
