# Duplicate Data Cleanup-Script-for-Duplicate-Asset-IDs-in-Enterprise-Geodatabases

* The script can be run from **ArcGIS Pro Notebook, Toolbox (.pyt), VS Code, or any Python environment with arcpy**
* It is intended to be used **one time** (or occasionally) to clean existing duplicates
* After cleanup, users should enable a **NextSequenceValue ('Test')** to ensure future features always get a unique ID automatically

Everything is phrased clearly, professionally, and applicable to *any* feature layer.


# 🔧 FixDuplicateUniqueIDs

### Duplicate Data Cleanup Tool for Duplicate Asset IDs in Enterprise Geodatabases (ArcGIS SDE)

This script detects and fixes **duplicate ID values** in any SDE feature class.
Although the example uses `HYDRANT_ID`, the script is fully generic and works for ANY unique ID field such as:

* `ASSET_ID`
* `ADDRESS_ID`
* `METER_ID`
* `VALVE_ID`
* `PIPE_ID`
* `PROJECT_ID`
* Custom primary keys used by Utilities, Engineering, Addressing, Public Works, etc.


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


## ⭐ Benefits

✔ Ensures all IDs in the feature class are unique  
✔ Prevents work order and integration errors  
✔ Avoids conflicts with domain systems (Cityworks, Maximo, Utility Network)  
✔ Enables successful GENERATE_ID attribute rules  
✔ Fully automated, safe, and rollback-capable  
✔ Ideal for enterprise GIS data governance  

## 📚 Libraries & Tools Used

### **arcpy**

The script uses **arcpy**, Esri’s official Python library for working with geodatabases and spatial data.
arcpy provides:

* **Data Access (arcpy.da)** for fast Search/Update Cursors
* **Editor** sessions for safe transactional edits in SDE
* **Geodatabase management** and field operations
* **Messaging tools** (`AddMessage`, `AddError`) when running inside ArcGIS Pro or a Toolbox

arcpy is included with **ArcGIS Pro** and requires no additional installation.


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


## ✔ After Cleanup: Enable Automatic NextSequenceValue ('Test') Attribute Rule

Once all duplicates are removed, enable this attribute rule:

NextSequenceValue ('Test')
URL : https://support.esri.com/en-us/knowledge-base/how-to-add-auto-sequential-values-using-attribute-rules-000024533

This ensures:

* Every new feature gets a unique ID
* No duplicates will occur again
* Field crews, editors, and automated workflows stay consistent

This script = **one-time cleanup**
Attribute rule = **permanent prevention**
