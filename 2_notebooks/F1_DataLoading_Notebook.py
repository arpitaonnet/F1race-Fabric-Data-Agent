# ============================================================
# F1 Data Model - Full Data Loading Notebook
# Reads SAS credentials from Lakehouse JSON file
# ============================================================


# -------------------------------------------------------
# CELL 1: Read SAS credentials from Lakehouse JSON file
# -------------------------------------------------------

import json

# Read the SAS credentials JSON from Lakehouse Files
with open("/lakehouse/default/Files/sascredentials.json", "r") as f:
    creds = json.load(f)

# Extract values from JSON
# Adjust these keys to match what's inside your sascredentials.json
storage_account = creds["storage_account"]   # e.g. "fabricaidata"
container       = creds["container"]          # e.g. "f1race"
sas_token       = creds["sas_token"]          # e.g. "?sv=2021-xx&ss=..."

print(f"✅ Credentials loaded successfully!")
print(f"   Storage Account : {storage_account}")
print(f"   Container       : {container}")
print(f"   SAS Token       : {sas_token[:30]}...")  # Only show first 30 chars for safety


# -------------------------------------------------------
# CELL 2: Configure Spark to use SAS Token
# -------------------------------------------------------

spark.conf.set(
    f"fs.azure.sas.{container}.{storage_account}.blob.core.windows.net",
    sas_token
)

base_path = f"wasbs://{container}@{storage_account}.blob.core.windows.net"

print(f"✅ Spark configured for: {base_path}")


# -------------------------------------------------------
# CELL 3: Helper function to read CSV files
# -------------------------------------------------------

def read_csv(filename):
    path = f"{base_path}/{filename}"
    df = spark.read.csv(path, header=True, inferSchema=True)
    print(f"✅ Loaded {filename}: {df.count():,} rows | {len(df.columns)} columns")
    return df


# -------------------------------------------------------
# CELL 4: Load all DIMENSION tables
# -------------------------------------------------------

print("=" * 55)
print("  Loading DIMENSION Tables...")
print("=" * 55)

dim_circuits      = read_csv("Dim_Circuits.csv")
dim_constructors  = read_csv("Dim_Constructors.csv")
dim_drivers       = read_csv("Dim_Drivers.csv")
dim_races         = read_csv("Dim_Races.csv")
dim_seasons       = read_csv("Dim_Seasons.csv")
dim_status        = read_csv("Dim_Status.csv")

print("\n✅ All 6 Dimension tables loaded!")


# -------------------------------------------------------
# CELL 5: Load all FACT tables
# -------------------------------------------------------

print("=" * 55)
print("  Loading FACT Tables...")
print("=" * 55)

fact_results                = read_csv("Fact_Results.csv")
fact_lap_times              = read_csv("Fact_LapTimes.csv")
fact_pit_stops              = read_csv("Fact_PitStops.csv")
fact_qualifying             = read_csv("Fact_Qualifying.csv")
fact_sprint_results         = read_csv("Fact_SprintResults.csv")
fact_driver_standings       = read_csv("Fact_DriverStandings.csv")
fact_constructor_standings  = read_csv("Fact_ConstructorStandings.csv")
fact_constructor_results    = read_csv("Fact_ConstructorResults.csv")

print("\n✅ All 8 Fact tables loaded!")


# -------------------------------------------------------
# CELL 6: Write DIMENSION tables to Lakehouse (Delta)
# -------------------------------------------------------

print("=" * 55)
print("  Writing DIMENSION tables to Lakehouse...")
print("=" * 55)

dim_circuits.write.mode("overwrite").format("delta").saveAsTable("Dim_Circuits")
print("✅ Dim_Circuits saved")

dim_constructors.write.mode("overwrite").format("delta").saveAsTable("Dim_Constructors")
print("✅ Dim_Constructors saved")

dim_drivers.write.mode("overwrite").format("delta").saveAsTable("Dim_Drivers")
print("✅ Dim_Drivers saved")

dim_races.write.mode("overwrite").format("delta").saveAsTable("Dim_Races")
print("✅ Dim_Races saved")

dim_seasons.write.mode("overwrite").format("delta").saveAsTable("Dim_Seasons")
print("✅ Dim_Seasons saved")

dim_status.write.mode("overwrite").format("delta").saveAsTable("Dim_Status")
print("✅ Dim_Status saved")

print("\n✅ All Dimension tables written to Lakehouse!")


# -------------------------------------------------------
# CELL 7: Write FACT tables to Lakehouse (Delta)
# -------------------------------------------------------

print("=" * 55)
print("  Writing FACT tables to Lakehouse...")
print("=" * 55)

fact_results.write.mode("overwrite").format("delta").saveAsTable("Fact_Results")
print("✅ Fact_Results saved")

fact_lap_times.write.mode("overwrite").format("delta").saveAsTable("Fact_LapTimes")
print("✅ Fact_LapTimes saved")

fact_pit_stops.write.mode("overwrite").format("delta").saveAsTable("Fact_PitStops")
print("✅ Fact_PitStops saved")

fact_qualifying.write.mode("overwrite").format("delta").saveAsTable("Fact_Qualifying")
print("✅ Fact_Qualifying saved")

fact_sprint_results.write.mode("overwrite").format("delta").saveAsTable("Fact_SprintResults")
print("✅ Fact_SprintResults saved")

fact_driver_standings.write.mode("overwrite").format("delta").saveAsTable("Fact_DriverStandings")
print("✅ Fact_DriverStandings saved")

fact_constructor_standings.write.mode("overwrite").format("delta").saveAsTable("Fact_ConstructorStandings")
print("✅ Fact_ConstructorStandings saved")

fact_constructor_results.write.mode("overwrite").format("delta").saveAsTable("Fact_ConstructorResults")
print("✅ Fact_ConstructorResults saved")

print("\n✅ All Fact tables written to Lakehouse!")


# -------------------------------------------------------
# CELL 8: Verify all tables exist in Lakehouse
# -------------------------------------------------------

print("=" * 55)
print("  Verifying tables in Lakehouse...")
print("=" * 55)

tables = spark.sql("SHOW TABLES").select("tableName").collect()
print(f"\n📦 Total tables in Lakehouse: {len(tables)}\n")
for t in tables:
    print(f"   ✅ {t['tableName']}")


# -------------------------------------------------------
# CELL 9: Quick preview of all tables
# -------------------------------------------------------

# Dimensions
display(dim_circuits)
display(dim_constructors)
display(dim_drivers)
display(dim_races)
display(dim_seasons)
display(dim_status)

# Facts
display(fact_results)
display(fact_lap_times)
display(fact_pit_stops)
display(fact_qualifying)
display(fact_sprint_results)
display(fact_driver_standings)
display(fact_constructor_standings)
display(fact_constructor_results)
