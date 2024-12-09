import hashlib
import pandas as pd


class Util:
    def get_bsuite_observation_id(self, series: pd.Series) -> str:
        assert type(series) is pd.Series, f"series needs to be of type {pd.Series}"
        assert "sample_id" in series, "'sample_id' not in series"
        assert (
            "sequences_requested_id" in series
        ), "'sequences_requested_id' not in series"

        fields = (series.sample_id, series.sequences_requested_id)
        m = "".join(fields).encode()
        return hashlib.sha1(m).hexdigest()

    def set_size(self, width_pt, fraction=1, subplots=(1, 1)):
        """Set figure dimensions to sit nicely in our document.

        Parameters
        ----------
        width_pt: float
                Document width in points
        fraction: float, optional
                Fraction of the width which you wish the figure to occupy
        subplots: array-like, optional
                The number of rows and columns of subplots.
        Returns
        -------
        fig_dim: tuple
                Dimensions of figure in inches
        """
        # Width of figure (in pts)
        fig_width_pt = width_pt * fraction
        # Convert from pt to inches
        inches_per_pt = 1 / 72.27

        # Golden ratio to set aesthetic figure height
        golden_ratio = (5 ** 0.5 - 1) / 2

        # Figure width in inches
        fig_width_in = fig_width_pt * inches_per_pt
        # Figure height in inches
        fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

        return (fig_width_in, fig_height_in)
