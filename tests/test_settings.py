#!/usr/bin/env python3

# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from climetlab import settings
import os
import yaml
import climetlab.plotting
from climetlab.core.data import get_data_entry, clear_cache
from climetlab.core.plugins import directories


def check_user_defined_objects(collection, setting, obj, tree, get_list, get_entry):

    # Clear cache
    clear_cache()

    paths = settings.get(setting)
    assert isinstance(paths, (list, tuple)), paths
    assert len(paths) > 0

    for i, path in enumerate(paths):

        name = "pytest-%s-%s" % (tree[1], i)

        if os.path.exists(path) and os.path.isdir(path):
            assert path in directories(), directories()

        if not os.path.exists(path):
            os.mkdir(path)

        with open(os.path.join(path, "%s.yaml" % (name,)), "w") as f:
            a = obj
            for t in tree[:-1]:
                a = a[t]
            a[tree[-1]] = i
            yaml.dump(obj, f, default_flow_style=False)

    for i in range(0, len(paths)):
        name = "pytest-%s-%s" % (tree[1], i)
        get_data_entry(collection, name)
        assert name in get_list()
        p = get_entry(name).data

        a = p
        for t in tree:
            a = a[t]

        assert a == i

    # TODO: Move to tear-down
    for i, path in enumerate(paths):
        name = "pytest-%s-%s" % (tree[1], i)
        os.unlink(os.path.join(path, "%s.yaml" % (name,)))


def test_user_projections():
    check_user_defined_objects(
        "projections",
        "projections-directories",
        {"magics": {"mmap": {}}},
        ["magics", "mmap", "subpage_lower_left_latitude"],
        climetlab.plotting.projections,
        climetlab.plotting.projection,
    )


def test_user_styles_msymb():
    check_user_defined_objects(
        "styles",
        "styles-directories",
        {"magics": {"msymb": {}}},
        ["magics", "msymb", "symbol_marker_index"],
        climetlab.plotting.styles,
        climetlab.plotting.style,
    )


def test_user_styles_mcont():
    check_user_defined_objects(
        "styles",
        "styles-directories",
        {"magics": {"mcont": {}}},
        ["magics", "mcont", "contour_line_thickness"],
        climetlab.plotting.styles,
        climetlab.plotting.style,
    )


def test_user_layers():
    check_user_defined_objects(
        "layers",
        "layers-directories",
        {"magics": {"mcoast": {}}},
        ["magics", "mcoast", "map_grid_frame_thickness"],
        climetlab.plotting.layers,
        climetlab.plotting.layer,
    )

def test_settings():
    pass
