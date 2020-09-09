# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

# TODO: Use magics types


def convert_colours():
    pass


def convert(args):
    a = {}
    for k, v in args.items():
        a[k] = v
        if isinstance(v, tuple):
            a[k] = "rgba%r" % (v,)
    return a
