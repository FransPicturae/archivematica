# -*- coding: utf-8 -*-
from __future__ import absolute_import

import bagit

from archivematicaFunctions import get_bag_size, walk_dir


def test_get_bag_size(tmpdir):
    """Test that get_bag_size uses bag-info Payload-Oxum when present.
    """
    # Set up test data
    bag_dir = tmpdir.mkdir("bag")
    data_file = bag_dir.join("file.txt")
    data_file.write("Lorem ipsum")
    bagit.make_bag(bag_dir.strpath)
    # Replace Payload-Oxum with incorrect arbitrary value
    bag_info = bag_dir.join("bag-info.txt")
    size_oxum = 1056
    bag_info.write("Payload-Oxum: {}.1".format(str(size_oxum)))
    # Test returned value against expected
    size_on_disk = walk_dir(bag_dir.strpath)
    size = get_bag_size(bag_dir.strpath)
    assert size == size_oxum
    assert size != size_on_disk


def test_get_bag_size_bag_missing_oxum(tmpdir):
    """Test that get_bag_size uses walk if bag-info Payload-Oxum is missing.
    """
    # Set up test data
    bag_dir = tmpdir.mkdir("bag")
    data_file = bag_dir.join("file.txt")
    data_file.write("Lorem ipsum")
    bagit.make_bag(bag_dir.strpath)
    # Overwrite bag-info.txt without Payload-Oxum
    bag_info = bag_dir.join("bag-info.txt")
    bag_info.write("Bagging-Date: 2020-04-15")
    # Test returned value against expected
    size_on_disk = walk_dir(bag_dir.strpath)
    size = get_bag_size(bag_dir.strpath)
    assert size == size_on_disk
