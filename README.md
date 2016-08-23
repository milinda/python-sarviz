# python-sarviz

Tool for visualizing [SAR](https://en.wikipedia.org/wiki/Sar_(Unix)) logs.

This is an extension of [python-sar](https://github.com/casastorta/python-sar). So this doesn't support SAR binary files, but only ASCII files. You can convert SAR binary files to ASCII files using following command.

```
sar -A -f <sar_binary_log> > <sar_data.txt>
```

## How To Use

```python
from sar import parser
from sar import viz

insar = parser.Parser('./data/sample.log')
sar_viz = viz.Visualization(insar.get_sar_info(), paging=True, network=True, disk=True)
sar_viz.save('sample.pdf')
```

# Example Visualization

![sarviz](https://raw.githubusercontent.com/milinda/python-sarviz/master/sample.png)
