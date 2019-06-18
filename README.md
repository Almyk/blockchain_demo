# blockchain_demo
Blockchain Demo for Software Engineering Class

To run the tests in the test folder:
```python
python3 -m tests.[test]
```

  *  *  *  *  *

## Dependencies

* fastecdsa (https://pypi.org/project/fastecdsa/)
* hashlib
* json
* tkinter
* PIL

If any of the dependencies require to be installed, they should be available through pip3:
```bash
pip3 install [dependency]
```

  *  *  *  *  *

The callback function for debugging need to have the following header:
```python
def eventCallback(event, server, node, data=None):
```
event is a string containing the name of the event, server is an object of the Node class, node is an object of the NodeConnection class and data is a python dictionary type.
