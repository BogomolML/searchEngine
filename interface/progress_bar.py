# progress_bar.pu

from tqdm import tqdm


class Progress:
    def __init__(self):
        self._progress = None

    def show_progress(self, total, desc='Поиск...'):
        self._progress = tqdm(
            total=total,
            desc=desc,
            unit='док',
            bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]',
            colour='GREEN'
        )

    def update_progress(self):
        if self._progress:
            self._progress.update()

    def close_progress(self):
        if self._progress:
            self._progress.close()
            self._progress = None

