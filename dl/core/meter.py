from typing import Any, Dict
from collections import defaultdict

from torch import nn
from torchnet.meter import AverageValueMeter


class MetricManager:

    def __init__(self):
        self._meter = AverageValueMeter()
        self._all_epoch_values: [float] = []

    def add_batch_value(self, value: float):
        # Set correct n to avoid batch size influence on mean value
        self._meter.add(value)

    def begin_epoch(self):
        self._meter.reset()

    def end_epoch(self):
        current_epoch_value = self._meter.value()
        self._all_epoch_values.append(current_epoch_value[0])

    @property
    def last_epoch_value(self):
        return self._all_epoch_values[-1]

    @property
    def all_epoch_values(self) -> [float]:
        return self._all_epoch_values

    def get_best_epoch_value(self, minimize: bool) -> float:
        if minimize:
            return min(self._all_epoch_values)
        else:
            return max(self._all_epoch_values)


class MetricsManager:

    def __init__(self):
        self._managers: Dict[str, MetricManager] = defaultdict(MetricManager)

    @property
    def metric_names(self) -> [str]:
        return self._managers.keys()

    def add_batch_value(
        self,
        metric_name: str,
        value: float
    ):
        self._managers[metric_name].add_batch_value(value)

    def begin_epoch(self):
        for manager in self._managers.values():
            manager.begin_epoch()

    def end_epoch(self):
        for manager in self._managers.values():
            manager.end_epoch()

    def get_last_epoch_value(
        self,
        metric_name: str
    ) -> float:
        return self._managers[metric_name].last_epoch_value

    def get_all_epoch_values(
        self,
        metric_name: str
    ) -> [float]:
        return self._managers[metric_name].all_epoch_values

    def get_best_epoch_value(
        self,
        metric_name: str,
        minimize: bool
    ) -> float:
        return self._managers[metric_name].get_best_epoch_value(minimize=minimize)


class Meter:

    def __init__(self):
        self._managers: Dict[str, MetricsManager] = defaultdict(MetricsManager)

    def get_all_metric_names(
        self,
        phase: str
    ) -> [str]:
        return self._managers[phase].metric_names

    def add_batch_value(
        self,
        phase: str,
        metric_name: str,
        value: float
    ):
        self._managers[phase].add_batch_value(metric_name, value)

    def begin_phase(
        self,
        phase: str
    ):
        self._managers[phase].begin_epoch()

    def end_phase(
        self,
        phase: str
    ):
        self._managers[phase].end_epoch()

    def get_last_epoch_value(
        self,
        phase: str,
        metric_name: str
    ) -> float:
        return self._managers[phase].get_last_epoch_value(metric_name)

    def get_all_epoch_values(
        self,
        phase: str,
        metric_name: str
    ) -> [float]:
        return self._manages[phase].get_all_epoch_values(metric_name)

    def get_best_epoch_value(
        self,
        phase: str,
        metric_name: str,
        minimize: bool
    ) -> float:
        return self._managers[phase].get_best_epoch_value(
            metric_name=metric_name,
            minimize=minimize
        )

    def is_last_epoch_value_best(
        self,
        phase: str,
        metric_name: str,
        minimize: bool
    ) -> bool:
        last = self.get_last_epoch_value(
            phase=phase,
            metric_name=metric_name
        )

        best = self.get_best_epoch_value(
            phase=phase,
            metric_name=metric_name,
            minimize=minimize
        )

        # print(f'Last: {last}')
        # print(f'Best: {best}')

        return last==best



class Monitor:

    def __init__(self, str: str):
        components = str.split('_')

        self.str = str
        self.phase = components[0]
        self.metric_name = components[1]
