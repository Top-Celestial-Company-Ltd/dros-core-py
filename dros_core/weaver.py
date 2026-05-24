from typing import List, Optional
from dros_core.types import DrosManifest, DrosNode, DrosMatch

class TrieNode:
    def __init__(self):
        self.children = {}
        self.node_id = None

class DrosWeaver:
    def __init__(self, manifest: DrosManifest):
        self.root = TrieNode()
        self.node_map = manifest.nodes
        self._build_trie()

    def _build_trie(self):
        """
        將黃金清單中的 Canonical 正名與 Aliases 別名全面織入 Trie 樹
        """
        for node_id, node in self.node_map.items():
            self._insert(node.canonical, node_id)
            for alias in node.aliases:
                self._insert(alias, node_id)

    def _insert(self, word: str, node_id: str):
        cleaned = word.strip()
        if not cleaned:
            return

        current = self.root
        for c in cleaned:
            if c not in current.children:
                current.children[c] = TrieNode()
            current = current.children[c]
        current.node_id = node_id

    def weave(self, text: str) -> List[DrosMatch]:
        """
        最長匹配優先（LMF）滑動掃描演算法
        時間複雜度：O(N) 線性掃描
        """
        matches = []
        chars = list(text) # 轉化為字元列表，保證 Unicode 索引在物理上的絕對精確
        length = len(chars)
        i = 0

        while i < length:
            current = self.root
            longest_match_node_id = None
            longest_match_length = 0

            for j in range(i, length):
                c = chars[j]
                if c in current.children:
                    current = current.children[c]
                    if current.node_id is not None:
                        longest_match_node_id = current.node_id
                        longest_match_length = j - i + 1
                else:
                    break

            if longest_match_node_id is not None:
                matched_text = "".join(chars[i:i + longest_match_length])
                matches.append(DrosMatch(
                    node_id=longest_match_node_id,
                    start_index=i,
                    end_index=i + longest_match_length,
                    matched_text=matched_text
                ))
                i += longest_match_length # 滑動最長匹配寬度，熔斷重疊短詞
            else:
                i += 1

        return matches

    def get_node(self, node_id: str) -> Optional[DrosNode]:
        return self.node_map.get(node_id)

    def get_all_nodes(self) -> List[DrosNode]:
        return list(self.node_map.values())
