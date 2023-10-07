# mdpd
`mdpd` is a simpler tool for convert markdown table to pandas.
This tool is a lightweight tool for testing a code, so note that we are not validating the user's input.

## usage

```python
# pip install mdpd
import mdpd

df = mdpd.from_md("""
+------------+-----+
| id         | age |
+------------+-----+
| 1          | 15  |
| 2          | 11  |
| 3          | 11  |
| 4          | 20  |
+------------+-----+
""")
```


## contribute
If you have suggestions for features or improvements to the code, please feel free to create an issue or PR.
