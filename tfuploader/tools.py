from .images import export_images
from .zipfile import generate_zipfile, upload_zipfile
from collections import OrderedDict


def upload_from_queryset(queryset, name, file_attr="file",
                         class_attr="category", size=299, public=True):
    groups = get_groups(queryset, file_attr, class_attr)
    list_groups(groups)
    dirname, image_paths = export_images(groups, size)
    generate_zipfile(dirname, name, image_paths)
    upload_zipfile(dirname, name, public=public)


def list_groups_from_queryset(queryset, file_attr="file",
                              class_attr="category"):
    groups = get_groups(queryset, file_attr, class_attr)
    list_groups(groups)


def get_groups(queryset, file_attr, class_attr):
    groups = OrderedDict()
    for obj in queryset:
        group = str(getattr(obj, class_attr))
        groups.setdefault(group, [])
        groups[group].append((
            getattr(obj, file_attr).path,
            "%s.jpg" % obj.pk
        ))
    return groups


def list_groups(groups):
    print("Categories:")
    for group, paths in groups.items():
        print("%7s %s" % (len(paths), group))
