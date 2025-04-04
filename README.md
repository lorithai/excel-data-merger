# excel-data-merger

```
import merge_data
timepairs = {
            "Date_col1": ["val_col1", "val_col2"],
            "Date_col2": ["val_col3", "val_col4"]
            }

merged = merge_data("filename.csv",timepairs)

# save to file
merged.to_csv("merged_sensors.csv",index=False,encoding="utf-8-sig")
```