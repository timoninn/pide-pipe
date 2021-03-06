from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from ..core.callback import Callback
from ..core.state import State


class InferCallback(Callback):

    def __init__(
        self,
        out_dir: str
    ):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.predictions = []

    def on_batch_end(self, state: State):
        for arr in state.output.cpu().numpy():
            self.predictions.append(arr)

    def on_phase_end(self, state: State):
        np.save(self.out_dir / 'infer.npy', self.predictions)


class FilesInferCallback(Callback):

    def __init__(
        self,
        out_dir: str
    ):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

    def on_batch_end(self, state: State):
        output = state.output.cpu().numpy()
        ids = state.batch['id']

        for id, out in zip(ids, output):
            np.save(self.out_dir / f'{id}.npy', out)


class CSVInferCallback(Callback):

    def __init__(
        self,
        out_dir: str,
        columns: [str] = None
    ):
        self.out_dir = Path(out_dir)
        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.columns = columns

        self.data = []

    def on_batch_end(self, state: State):
        output = state.output.cpu().numpy()
        ids = state.batch['id']

        batch_data = {}
        for id, out in zip(ids, output):
            batch_data['id'] = id

            for idx, o in enumerate(out):
                batch_data[f'o_{idx}'] = o

        self.data.append(batch_data)

    def on_phase_end(self, state: State):
        df = pd.DataFrame(self.data)
        df.to_csv(self.out_dir / 'infer.csv', index=False)
