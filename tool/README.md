
### Script To Process Annotations

Outputs the json as key value pairs of user fields as key and their user attributes as values.
If the key is header, and has only answers then all answers are stored as array values.
Otherwise user attributes (dictionary values) are stored as key value pairs.

```
cd tool
python process_annotations.py
```