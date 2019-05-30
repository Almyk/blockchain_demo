# blockchain_demo
Blockchain Demo for Software Engineering Class

To run the tests in the test folder:
```python
python3 -m tests.[test]
```

The callback function need to have the following header:
```python
def eventCallback(event, server, node, data=None):
```
event is a string containing the name of the event, server is an object of the Node class, node is an object of the NodeConnection class and data is a python dictionary type.
