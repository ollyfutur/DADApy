# Copyright 2021-2023 The DADApy Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

import numpy as np
from sklearn.neighbors import NearestNeighbors


def _return_ranks(dist_indices_1, dist_indices_2, k=1):
    """Finds all the ranks according to distance 2 of the neighbours according to distance 1.
       Neighbours in distance 1 are considered up to order k.

    Args:
        dist_indices_1 (np.ndarray(int)): N x maxk matrix, nearest neighbours according to distance 1
        dist_indices_2 (np.ndarray(int))): N x maxk_2 matrix, nearest neighbours according to distance 2
        k (int): order of nearest neighbour considered for the calculation of the conditional ranks, default is 1

    Returns:
        conditional_ranks (np.ndarray(int)): N x k matrix, ranks according to distance 2 of the neighbours in distance 1

    """
    assert dist_indices_1.shape[0] == dist_indices_2.shape[0]

    N = dist_indices_1.shape[0]
    maxk_2 = dist_indices_2.shape[1]

    conditional_ranks = np.zeros((N, k))

    for i in range(N):
        idx_k_d1 = dist_indices_1[i, 1 : k + 1]

        wr = [
            np.where(idx_k_d1[k_neighbor] == dist_indices_2[i])[0]
            for k_neighbor in range(k)
        ]

        for k_neighbor in range(k):
            if len(wr[k_neighbor]) == 0:
                conditional_ranks[i, k_neighbor] = np.random.randint(maxk_2, N)
            else:
                conditional_ranks[i, k_neighbor] = wr[k_neighbor][0]

    return conditional_ranks


def _return_imbalance(dist_indices_1, dist_indices_2, k=1):
    """Compute the information imbalance between two precomputed distance measures.

    Args:
        dist_indices_1 (np.ndarray(int)): nearest neighbours according to distance 1
        dist_indices_2 (np.ndarray(int)): nearest neighbours according to distance 2
        k (int): order of nearest neighbour considered for the calculation of the imbalance, default = 1

    Returns:
        (float): information imbalance from distance 1 to distance 2

    """
    assert dist_indices_1.shape[0] == dist_indices_2.shape[0]

    N = dist_indices_1.shape[0]

    ranks = _return_ranks(dist_indices_1, dist_indices_2, k=k)

    imb = np.mean(ranks) / (N / 2.0)

    return imb
