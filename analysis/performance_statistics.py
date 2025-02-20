#! /usr/bin/env python3

import pandas as pd
import numpy as np

class PerformanceStatistics:
    def __init__(self, csv_file, index_col=None):
        self._df = pd.read_csv(csv_file, index_col=index_col)
        self._df.fillna(0, inplace=True)

    def __getDataSet(self, index=None):
        if index==None:
            return self._df
        else:
            return self._df.loc[index]

    def __getWalkCounter(self, index, counter_suffix):
        data_set = self.__getDataSet(index)
        load_counter = 'dtlb_load_misses.walk_' + counter_suffix
        store_counter = 'dtlb_store_misses.walk_' + counter_suffix
        if self._df.columns.contains(load_counter) \
                and self._df.columns.contains(store_counter):
                    return data_set[load_counter] + data_set[store_counter]
        else:
            return None

    def getIndexColumn(self):
        return np.array(self._df.index)

    def getWalkDuration(self, index=None):
        walk_duration = self.__getWalkCounter(index, 'active')
        if walk_duration is not None:
            return walk_duration
        walk_duration = self.__getWalkCounter(index, 'duration')
        if walk_duration is not None:
            return walk_duration
        raise Exception('the data-set has no performance counters for page walks!')

    def getStlbHits(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('dtlb_load_misses.stlb_hit')\
                and self._df.columns.contains('dtlb_store_misses.stlb_hit'):
                    return data_set['dtlb_load_misses.stlb_hit'] \
                            + data_set['dtlb_store_misses.stlb_hit']
        else:
            raise Exception('the data-set has no performance counters for STLB hits!')

    def getStlbMisses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('dtlb_load_misses.miss_causes_a_walk')\
                and self._df.columns.contains('dtlb_store_misses.miss_causes_a_walk'):
                    return data_set['dtlb_load_misses.miss_causes_a_walk'] \
                            + data_set['dtlb_store_misses.miss_causes_a_walk']
        else:
            raise Exception('the data-set has no performance counters for TLB misses!')

    '''
    def getStlbMisses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('dtlb_load_misses.walk_completed')\
        and self._df.columns.contains('dtlb_store_misses.walk_completed'):
            return data_set['dtlb_load_misses.walk_completed'] \
                    + data_set['dtlb_store_misses.walk_completed']
        else:
            raise Exception('the data-set has no performance counters for STLB misses (dtlb-misses-walk-completed)!')
    '''

    def getStlbMisses2m(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('dtlb_load_misses.walk_completed_2m_4m')\
        and self._df.columns.contains('dtlb_store_misses.walk_completed_2m_4m'):
            return data_set['dtlb_load_misses.walk_completed_2m_4m'] \
                    + data_set['dtlb_store_misses.walk_completed_2m_4m']
        else:
            return self.getStlbMisses(index)
            #raise Exception('the data-set has no performance counters for STLB misses (for 2MB pages)!')

    def getStlbMisses4k(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('dtlb_load_misses.walk_completed_4k')\
        and self._df.columns.contains('dtlb_store_misses.walk_completed_4k'):
            return data_set['dtlb_load_misses.walk_completed_4k'] \
                    + data_set['dtlb_store_misses.walk_completed_4k']
        else:
            return self.getStlbMisses(index)
            #raise Exception('the data-set has no performance counters for STLB misses (for 4KB pages)!')

    def getStlbAccesses(self, index=None):
        return self.getStlbHits(index) + self.getStlbMisses(index)

    def getTlbAccesses(self, index=None):
        return self.getL1Accesses(index)

    def getTlbMisses(self, index=None):
        return self.getStlbAccesses(index)

    def getTlbHits(self, index=None):
        return self.getTlbAccesses(index) - self.getTlbMisses(index)

    def getL1Accesses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('L1-dcache-loads')\
                and self._df.columns.contains('L1-dcache-stores'):
                    return data_set['L1-dcache-loads'] \
                            + data_set['L1-dcache-stores']
        else:
            raise Exception('the data-set has no performance counters for L1 data cache accesses!')

    def getL1Misses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('L1-dcache-load-misses')\
                and self._df.columns.contains('L1-dcache-store-misses'):
                    return data_set['L1-dcache-load-misses'] \
                            + data_set['L1-dcache-store-misses']
        else:
            raise Exception('the data-set has no performance counters for L1 data cache misses!')

    def getL1Hits(self, index=None):
        misses = self.getL1Misses(index)
        accesses = self.getL1Accesses(index)
        hits = accesses - misses
        return hits

    def getLlcAccesses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('LLC-loads')\
                and self._df.columns.contains('LLC-stores'):
                    return data_set['LLC-loads'] \
                            + data_set['LLC-stores']
        else:
            raise Exception('the data-set has no performance counters for LLC accesses!')

    def getLlcMisses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('LLC-load-misses')\
                and self._df.columns.contains('LLC-store-misses'):
                    return data_set['LLC-load-misses'] \
                            + data_set['LLC-store-misses']
        else:
            raise Exception('the data-set has no performance counters for LLC misses!')

    def getLlcHits(self, index=None):
        return self.getLlcAccesses(index) - self.getLlcMisses(index)

    def getL2Accesses(self, index=None):
        return self.getL1Misses(index)

    def getL2Misses(self, index=None):
        return self.getLlcAccesses(index)

    def getL2Hits(self, index=None):
        return self.getL2Accesses(index) - self.getL2Misses(index)

    def getPageWalkerL1Hits(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('page_walker_loads.dtlb_l1'):
            return data_set['page_walker_loads.dtlb_l1']
        else:
            raise Exception('the data-set has no performance counters for page_walker_loads.dtlb_l1!')

    def getPageWalkerL2Hits(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('page_walker_loads.dtlb_l2'):
            return data_set['page_walker_loads.dtlb_l2']
        else:
            raise Exception('the data-set has no performance counters for page_walker_loads.dtlb_l2!')

    def getPageWalkerL3Hits(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('page_walker_loads.dtlb_l3'):
            return data_set['page_walker_loads.dtlb_l3']
        else:
            raise Exception('the data-set has no performance counters for page_walker_loads.dtlb_l3!')

    def getPageWalkerMemoryAccesses(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('page_walker_loads.dtlb_memory'):
            return data_set['page_walker_loads.dtlb_memory']
        else:
            raise Exception('the data-set has no performance counters for page_walker_loads.dtlb_memory!')


    def getRuntime(self, index=None):
        data_set = self.__getDataSet(index)
        if self._df.columns.contains('cpu-cycles'):
            return data_set['cpu-cycles']
        else:
            raise Exception('the data-set has no performance counters for CPU cycles!')
        return 0

    def getDataFrame(self):
        return self._df.copy()
