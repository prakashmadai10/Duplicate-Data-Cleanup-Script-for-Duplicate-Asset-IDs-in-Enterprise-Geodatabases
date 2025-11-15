import arcpy
import pandas as pd

# -------------------------------------------------------------------
# User Inputs
# -------------------------------------------------------------------
fc = r"x.sde\My.DBO.Hydrants"
field_name = "HYDRANT_ID"
workspace = r"x.sde"

# -------------------------------------------------------------------
# STEP 1 — Load Hydrant IDs into Pandas
# -------------------------------------------------------------------
data = []

with arcpy.da.SearchCursor(fc, ["OBJECTID", field_name]) as cursor:
    for oid, val in cursor:
        if val is None:
            data.append([oid, None])
        else:
            data.append([oid, str(val).strip()])

df = pd.DataFrame(data, columns=["OBJECTID", "HYDRANT_ID"])

# Clean spaces + normalize
df["HYDRANT_ID"] = df["HYDRANT_ID"].replace(["", " "], None)

# Extract numeric part of ID
def extract_num(v):
    if v is None:
        return None
    try:
        return int(v)
    except:
        return None

df["NUM"] = df["HYDRANT_ID"].apply(extract_num)

# -------------------------------------------------------------------
# STEP 2 — Determine Current Max ID
# -------------------------------------------------------------------
max_id = df["NUM"].dropna().max()
if pd.isna(max_id):
    max_id = 0

arcpy.AddMessage(f"Max HYDRANT_ID detected = {max_id}")

# -------------------------------------------------------------------
# STEP 3 — Identify duplicates using Pandas
# -------------------------------------------------------------------
df["IS_DUP"] = df.duplicated(subset=["HYDRANT_ID"], keep="first")

duplicates_df = df[df["IS_DUP"] == True]
arcpy.AddMessage(f"Duplicate count = {len(duplicates_df)}")

# -------------------------------------------------------------------
# STEP 4 — Assign new unique IDs to duplicates
# -------------------------------------------------------------------
new_ids = range(max_id + 1, max_id + 1 + len(duplicates_df))
df.loc[df["IS_DUP"] == True, "NEW_ID"] = [str(i) for i in new_ids]

# Create a mapping: OBJECTID → NEW HYDRANT_ID
update_map = df.dropna(subset=["NEW_ID"])[["OBJECTID", "NEW_ID"]]
update_dict = dict(zip(update_map["OBJECTID"], update_map["NEW_ID"]))

# -------------------------------------------------------------------
# STEP 5 — Apply changes back into SDE with Editor
# -------------------------------------------------------------------
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

try:
    with arcpy.da.UpdateCursor(fc, ["OBJECTID", field_name]) as cursor:
        for oid, val in cursor:
            if oid in update_dict:
                new_val = update_dict[oid]
                cursor.updateRow((oid, new_val))
                arcpy.AddMessage(f"Updated OBJECTID {oid} → {new_val}")

    edit.stopOperation()
    edit.stopEditing(True)
    arcpy.AddMessage("✅ Hydrant ID Fix Completed Successfully.")

except Exception as e:
    edit.stopOperation()
    edit.stopEditing(False)
    arcpy.AddError(f"❌ Error: {e}")
