# mdpd
`mdpd` is a simpler tool for convert markdown table to pandas.
This tool is a lightweight tool for testing a code, so note that we are not validating the user's input.

## install
```bash
pip install mdpd
```

## usage

```python
import mdpd

df = mdpd.from_md("""
+------------+-------+
| id         | score |
+------------+-------+
| 1          | 15    |
| 2          | 11    |
| 3          | 11    |
| 4          | 20    |
+------------+-------+
""")

print(df)
#   id score
# 0  1    15
# 1  2    11
# 2  3    11
# 3  4    20
```

```python
# the header can be overwritten if the header exists
import mdpd
df = mdpd.from_md("""
| 1          | 15    |
| 2          | 11    |
| 3          | 11    |
| 4          | 20    |
""", header=["id", "score"])

print(df)
#   id score
# 0  1    15
# 1  2    11
# 2  3    11
# 3  4    20
```


## accepted table patterns

```markdown
| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |
```

```markdown
+------------+-------------+
| Syntax     | Description |
+------------+-------------+
| Header     | Title       |
| Paragraph  | Text        |
+------------+-------------+
```

```markdown
| Syntax    | Description |
| :-------- | ----------: |
| Header    | Title       |
| Paragraph | Text        |
```

```markdown
| Header    | Title       |
| Paragraph | Text        |
```

## contribute
If you have suggestions for features or improvements to the code, please feel free to create an issue or PR.
