Tensorflow Uploader
===================

This tool will load a Django queryset containing references to training images, generate a zip file and upload it to [tensorflow.wq.io].

```python
from observation.models import Observation
from tfuploader import upload_from_queryset

upload_from_queryset(
    Observation.objects.all(),
    name="observations.zip",
    file_attr="file",
    class_attr="category",
    size=299,
)
```

[tensorflow.wq.io]: https://tensorflow.wq.io
