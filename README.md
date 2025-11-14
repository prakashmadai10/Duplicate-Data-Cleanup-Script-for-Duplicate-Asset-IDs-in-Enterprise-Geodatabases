# One-Time-Cleanup-Tool-for-Duplicate-Asset-IDs-in-Enterprise-Geodatabases

* The script can be run from **ArcGIS Pro Notebook, Toolbox (.pyt), VS Code, or any Python environment with arcpy**
* It is intended to be used **one time** (or occasionally) to clean existing duplicates
* After cleanup, users should enable a **GNextSequenceValue ('Test')** to ensure future features always get a unique ID automatically

Everything is phrased clearly, professionally, and applicable to *any* feature layer.

---

# 🔧 FixDuplicateUniqueIDs

### One-Time Cleanup Tool for Duplicate Asset IDs in Enterprise Geodatabases (ArcGIS SDE)

This script detects and fixes **duplicate ID values** in any SDE feature class.
Although the example uses `HYDRANT_ID`, the script is fully generic and works for ANY unique ID field such as:

* `ASSET_ID`
* `ADDRESS_ID`
* `METER_ID`
* `VALVE_ID`
* `PIPE_ID`
* `PROJECT_ID`
* Custom primary keys used by Utilities, Engineering, Addressing, Public Works, etc.

This tool is typically run **once** to clean existing data.
After cleanup, you can enable **GENERATE_ID attribute rules** so future features always get a unique ID automatically.

---

## 🚀 Where You Can Run This Script

This script works in **all ArcGIS Python environments**, including:

### ✔ ArcGIS Pro Notebook

### ✔ ArcGIS Pro Toolbox (as a script tool or .pyt)

### ✔ ArcGIS Server Python environment

### ✔ VS Code running arcpy (Pro/Server conda environment)

### ✔ Any scheduled Python job (Windows Task Scheduler, Jenkins, etc.)

If your feature layer currently contains duplicate IDs → **run this script once** to fix all duplicates safely.

---

## 🧠 When To Use This Tool

Use this script **before enabling attribute rules**, **before migrating to Utility Network**, or **before publishing layers to AGOL/Portal**.

Common scenarios:

### 🏘️ Addressing

Address IDs accidentally duplicated during bulk imports.

### 🚒 Utilities / Fire

Hydrant, valve, or meter IDs repeated after historical edits.

### 🏗️ Engineering

Manhole, pipe, or lift station IDs not unique after merges or append jobs.

### 🗂️ Data Governance / QA

Nightly ETL cleanup where uniqueness is required.

---

## ⭐ Benefits

✔ Ensures all IDs in the feature class are unique
✔ Prevents work order and integration errors
✔ Avoids conflicts with domain systems (Cityworks, Maximo, UN)
✔ Enables successful GENERATE_ID attribute rules
✔ Fully automated, safe, rollback-capable
✔ Ideal for enterprise GIS data governance

---

## 🧩 How the Script Works

### **1. Scan all existing ID values**

* Ignores blanks
* Converts numeric IDs safely
* Determines the **highest used ID**

### **2. Detect duplicates**

* Dictionary-based lookup
* Identifies OBJECTIDs that need reassignment

### **3. Assign new IDs to duplicates**

* Each duplicate gets:

  ```
  max_id + 1
  max_id + 2
  ...
  ```

### **4. Transaction-safe editing**

Uses `arcpy.da.Editor` to:

* Start edit session
* Perform updates
* Commit on success
* Roll back changes on failure

---

## ✔ After Cleanup: Enable Automatic NextSequenceValue ('Test') Attribute Rule

Once all duplicates are removed, enable this attribute rule:

```
NextSequenceValue ('Test')
```

This ensures:

* Every new feature gets a unique ID
* No duplicates will occur again
* Field crews, editors, and automated workflows stay consistent

This script = **one-time cleanup**
Attribute rule = **permanent prevention**

---

## 📄 Example Implementation Snippet

```python
field_name = "HYDRANT_ID"  # Replace with your field (ASSET_ID, ADDRESS_ID, etc.)
```

Replace this with the ID field used in your dataset.

---

