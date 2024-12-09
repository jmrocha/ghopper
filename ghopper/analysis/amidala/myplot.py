import matplotlib.pyplot as plt


colors = {"-O0": "green", "-O1": "red", "-O2": "orange", "-O3": "blue", "-Os": "brown"}

class MyPlot:
    def bar(self, df):
        self._df = df
        if self.benchmarks == []:
            self._benchmarks = list(self._df.index.values)
        else:
            self._benchmarks = list(self.benchmarks)

        if self.avg_label in self._benchmarks:
            self._benchmarks.remove(self.avg_label)
            self._benchmarks.sort()
            self._benchmarks.append(self.avg_label)
        #self._reindex_df_from_benchmarks()
        self._df = self._df.reindex(self._benchmarks, axis=0)
        #self._df = self._df.T
        self._df.plot(
                kind='bar',
                ax=self.ax,
                color=df.columns.map(colors)
                )
        self._set_horizontal_line_at_y1()
        labels = [self.avg_symbol if x == self.avg_label else x for x in
                self._benchmarks]
        self.ax.set_xticks(range(0, len(self._df.index.values)), labels=labels)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), **self._xlabels_options)
        self._set_labels()
        self._set_title()
        self.ax.legend(title='Strategy',
                loc='upper right',
                bbox_to_anchor=(1, 1),
                fontsize=7
                )


    def plot(self, df):
        self._df = df
        self._benchmarks = self._get_benchmarks()
        self._reindex_df_from_benchmarks()
        self._set_horizontal_line_at_y1()
        self._set_boxplot()
        self._set_xticks()
        self._set_labels()
        self._set_title()

    def __init__(self):
        self.benchmarks = []
        self.ax = None
        self.xlabel = ''
        self.ylabel = ''
        self.title = ''
        self.avg_label = "_average"
        self.avg_symbol = r"$\bar{b}$"
        self._df = None
        self._xlabels_options = dict(
            rotation=45, rotation_mode="anchor", ha="right", fontsize=8
        )

    def _get_benchmarks(self):
        assert self._df is not None
        if self.benchmarks == []:
            benchmarks = list(self._df.columns.values)
        else:
            benchmarks = list(self.benchmarks)

        if self.avg_label in benchmarks:
            benchmarks.remove(self.avg_label)
            benchmarks.sort()
            benchmarks.append(self.avg_label)
        return benchmarks

    def _reindex_df_from_benchmarks(self):
        self._df = self._df.reindex(self._benchmarks, axis=1)

    def _get_labels(self):
        return [self.avg_symbol if x == self.avg_label else x for x in self._benchmarks]

    def _set_horizontal_line_at_y1(self):
        self.ax.axhline(y=0, ls="--", color="green")

    def _set_boxplot(self):
        self.ax.boxplot(self._df.values, labels=self._benchmarks)

    def _set_xticks(self):
        labels = self._get_labels()
        self.ax.set_xticks(range(1, len(self._df.columns) + 1), labels=labels)
        self.ax.set_xticklabels(self.ax.get_xticklabels(), **self._xlabels_options)

    def _set_labels(self):
        self.ax.set_xlabel(self.xlabel)
        self.ax.set_ylabel(self.ylabel)
        self.xlabel = ''
        self.ylabel = ''

    def _set_title(self):
        self.ax.set_title(self.title)
        self.title = ''
