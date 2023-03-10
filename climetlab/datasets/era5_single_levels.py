# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation
# nor does it submit to any jurisdiction.
#

from climetlab import load_source
from climetlab.utils.dates import to_datetime
from climetlab.utils.domains import domain_to_area

from . import Dataset


class Era5SingleLevels(Dataset):
    def _load(self, variable, period, domain=None, time=None, grid=None):
        self.variable = variable

        request = dict(
            variable=self.variable,
            product_type="reanalysis",
        )

        if domain is not None:
            request["area"] = domain_to_area(domain)

        request["time"] = time if time is not None else list(range(24))
        if grid is not None:
            request["grid"] = [grid, grid] if isinstance(grid, (int, float)) else grid
        if isinstance(period, int):
            period = (period, period)

        if isinstance(period, (tuple, list)) and len(period) == 1:
            period = (period[0], period[0])

        sources = []
        for year in range(period[0], period[1] + 1):
            request["year"] = year
            sources.append(
                load_source("cds", "reanalysis-era5-single-levels", **request)
            )

        self.source = load_source("multi", sources)

    def __getitem__(self, n):
        # TODO: move to superclass
        if isinstance(n, int):
            return super().__getitem__(n)

        n = to_datetime(n)
        for field in self:
            if field.datetime() == n:
                return field

        raise KeyError(n)


dataset = Era5SingleLevels
