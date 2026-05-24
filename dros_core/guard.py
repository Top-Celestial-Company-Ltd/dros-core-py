from typing import List
from dros_core.types import DrosMatch, ActiveNeighbor
from dros_core.weaver import DrosWeaver

class DrosGuardVM:
    def __init__(self, weaver: DrosWeaver):
        self.weaver = weaver

    def compile(self, matches: List[DrosMatch], active_neighbors: List[ActiveNeighbor], mode: str) -> str:
        """
        編譯熔斷提示詞：將匹配的名相與關聯鄰居轉化為 Markdown Sovereign Context Grid
        """
        parts = []
        parts.append("<!-- DROS_SOVEREIGN_CONTEXT_START -->")
        parts.append("## 📿 DROS 拓撲義理網格 (Sovereign Context Grid)")
        parts.append("當前文本中已成功編織以下義理突觸：\n")

        # 1. 核心名相定義輸出
        parts.append("### 核心名相定義 (Canonical Core Nodes)")
        if not matches:
            parts.append("- *無直接匹配核心名相*")
        else:
            seen_core_ids = set()
            for r_match in matches:
                if r_match.node_id in seen_core_ids:
                    continue
                seen_core_ids.add(r_match.node_id)

                node = self.weaver.get_node(r_match.node_id)
                if node:
                    parts.append(f"- **{node.canonical} ({node.id})**：{node.definition}")
        parts.append("")

        # 2. 拓撲關聯鄰居輸出 (僅在 prajna 模式下輸出)
        if mode == "prajna":
            parts.append("### 關聯拓撲鄰居 (Active Synaptic Neighbors)")
            if not active_neighbors:
                parts.append("- *無關聯拓撲鄰居*")
            else:
                for neighbor in active_neighbors:
                    source_node = self.weaver.get_node(neighbor.source_node_id)
                    source_name = source_node.canonical if source_node else neighbor.source_node_id
                    parts.append(
                        f"- **{neighbor.canonical} ({neighbor.node_id})** (共鳴權重: {neighbor.weight:.2f})："
                        f"與 [{source_name}] 具有 [{neighbor.relation}] 關係。"
                    )
            parts.append("")

        # 3. 熔斷契約指令編寫
        parts.append(f"### 推理合約熔斷規則 (GuardVM Execution Mode: {mode.upper()})")
        if mode == "vajra":
            parts.append(
                "[金剛契約已生效]：你的一切推論必須 100% 侷限在上述給定的【核心名相定義】中。你必須保持極致的學術客觀，"
                "逐字對齊定義，不得添加任何未經定義的宗教發揮或主觀推演。如果用戶的問題超出了上述定義的範疇，你必須坦誠回答「非本合約所及」。"
            )
        else:
            parts.append(
                "[菩薩契約已生效]：在立足於【核心名相定義】的前提下，你可以沿著【關聯拓撲鄰居】所勾勒的突觸網格（"
                "特別是各鄰居之間的關係，如等同、依止、生起等），進行溫和、融會貫通的跨學科或現代化義理詮釋。"
                "請結合當前筆記內容，引導用戶體會空性與智慧的隨流運用。"
            )

        parts.append("<!-- DROS_SOVEREIGN_CONTEXT_END -->")
        return "\n".join(parts)
