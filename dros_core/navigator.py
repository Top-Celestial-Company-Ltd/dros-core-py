from typing import List
from dros_core.types import DrosMatch, ActiveNeighbor
from dros_core.weaver import DrosWeaver

class DrosNavigator:
    def __init__(self, weaver: DrosWeaver):
        self.weaver = weaver

    def navigate(self, matches: List[DrosMatch], decay_factor: float) -> List[ActiveNeighbor]:
        """
        導航一階突觸鄰域，進行權重衰減乘算與多核心共鳴度累加
        """
        core_node_ids = {m.node_id for m in matches}
        neighbor_map = {}

        for r_match in matches:
            core_node = self.weaver.get_node(r_match.node_id)
            if not core_node:
                continue

            for synapse in core_node.synapses:
                # 排除已經被直接匹配的核心節點，避免重複推薦
                if synapse.target in core_node_ids:
                    continue

                target_node = self.weaver.get_node(synapse.target)
                if not target_node:
                    continue

                decayed_weight = synapse.weight * decay_factor

                if synapse.target in neighbor_map:
                    # 【突觸共鳴累加演算法】
                    neighbor_map[synapse.target].weight += decayed_weight
                else:
                    neighbor_map[synapse.target] = ActiveNeighbor(
                        node_id=synapse.target,
                        canonical=target_node.canonical,
                        relation=synapse.relation,
                        source_node_id=r_match.node_id,
                        weight=decayed_weight
                    )

        # 轉化為列表並按共鳴權重降序排序
        result = list(neighbor_map.values())
        result.sort(key=lambda x: x.weight, reverse=True)
        return result
