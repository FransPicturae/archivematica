# -*- coding: utf-8 -*-
from __future__ import absolute_import

import bagit

from archivematicaFunctions import get_dir_size, walk_dir


def test_get_dir_size_bag(tmpdir):
    """Test that get_dir_size uses bag-info Payload-Oxum when present.
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
    size = get_dir_size(bag_dir.strpath)
    assert size == size_oxum
    assert size != size_on_disk


def test_get_dir_size_bag_missing_oxum(tmpdir):
    """Test that get_dir_size uses walk if bag-info Payload-Oxum is missing.
    """
    # Set up test data
    bag_dir = tmpdir.mkdir("bag")
    data_file = bag_dir.join("file.txt")
    data_file.write("Lorem ipsum")
    bagit.make_bag(bag_dir.strpath)
    # Overrite bag-info.txt without Payload-Oxum
    bag_info = bag_dir.join("bag-info.txt")
    bag_info.write("Bagging-Date: 2020-04-15")
    # Test returned value against expected
    size_on_disk = walk_dir(bag_dir.strpath)
    size = get_dir_size(bag_dir.strpath)
    assert size == size_on_disk


def test_get_dir_size_regular_directory(tmpdir):
    """Test that get_dir_size uses walk if source is not a Bag.
    """
    # Set up test data
    regular_dir = tmpdir.mkdir("regular_dir")
    data_file = regular_dir.join("file.txt")
    data_file.write("Lorem ipsum")
    # Test that get_dir_size returns filewalk
    size_on_disk = walk_dir(regular_dir.strpath)
    size = get_dir_size(regular_dir.strpath)
    assert size == size_on_disk
