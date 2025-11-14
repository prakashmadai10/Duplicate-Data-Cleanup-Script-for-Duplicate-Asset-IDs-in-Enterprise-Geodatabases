import arcpy

# -------------------------------------------------------------------
# Script: Fix Duplicate HYDRANT_ID Values in an SDE Feature Class
# Purpose:
#   - Identify the highest existing HYDRANT_ID
#   - Detect any duplicate HYDRANT_ID values
#   - Reassign new unique IDs to duplicates (incrementing from max ID)
# Author: Prakash Madai
# -------------------------------------------------------------------

# Path to your SDE feature class
fc = r"x.sde\My.DBO.Address"

# Field to be fixed
field_name = "HYDRANT_ID"

# Workspace = SDE connection used for arcpy.da.Editor
workspace = r"x.sde"

# -------------------------------------------------------------------
# STEP 1 — Find the maximum existing HYDRANT_ID
# -------------------------------------------------------------------
max_id = 0
with arcpy.da.SearchCursor(fc, [field_name]) as cursor:
    for row in cursor:
        val = row[0]
        if val not in (None, "", " "):
            try:
                num = int(str(val).strip())
                if num > max_id:
                    max_id = num
            except:
                # Ignore non-numeric values
                pass

arcpy.AddMessage(f"Max HYDRANT_ID found = {max_id}")

# -------------------------------------------------------------------
# STEP 2 — Identify duplicate HYDRANT_ID values
# -------------------------------------------------------------------
seen = {}
duplicates = []

with arcpy.da.SearchCursor(fc, ["OBJECTID", field_name]) as cursor:
    for oid, val in cursor:
        if val not in (None, "", " "):
            key = str(val).strip()

            # If already seen ⇒ duplicate
            if key in seen:
                duplicates.append(oid)
            else:
                seen[key] = oid

arcpy.AddMessage(f"Found {len(duplicates)} duplicate records to fix")

# -------------------------------------------------------------------
# STEP 3 — Update duplicates with new unique HYDRANT_ID values
# -------------------------------------------------------------------
edit = arcpy.da.Editor(workspace)
edit.startEditing(False, True)
edit.startOperation()

try:
    counter = max_id + 1
    updated_count = 0

    with arcpy.da.UpdateCursor(fc, ["OBJECTID", field_name]) as cursor:
        for oid, val in cursor:
            if oid in duplicates:
                # Assign new unique value
                cursor.updateRow((oid, str(counter)))
                arcpy.AddMessage(f"Updated OBJECTID {oid} → HYDRANT_ID {counter}")
                counter += 1
                updated_count += 1

    edit.stopOperation()
    edit.stopEditing(True)
    arcpy.AddMessage(
        f"✅ Update complete. {updated_count} duplicate records reassigned. "
        f"Final HYDRANT_ID = {counter - 1}"
    )

except Exception as e:
    edit.stopOperation()
    edit.stopEditing(False)
    arcpy.AddError(f"❌ Error: {e}")
