import sys
import io
import unittest

# Configure sys.stdout to handle UTF-8 encoding on Windows
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from dros_core import DrosEngine, parse_manifest

class TestDrosCorePy(unittest.TestCase):
    def get_mock_manifest(self):
        data = {
            "version": "7.0.test",
            "metadata": {},
            "nodes": {
                "T0001": {
                    "id": "T0001",
                    "canonical": "真如",
                    "aliases": ["如如", "法性", "Suchness"],
                    "weights": {"tiantai": 0.95, "yogacara": 0.90},
                    "definition": "一切諸法之真實本性，非虛妄、非變異，離言絕慮之究竟實在。",
                    "synapses": [
                        {"target": "T0002", "relation": "等同", "weight": 1.0},
                        {"target": "T0003", "relation": "依止", "weight": 0.8}
                    ]
                },
                "T0002": {
                    "id": "T0002",
                    "canonical": "實相",
                    "aliases": ["真諦", "Ultimate Reality"],
                    "weights": {"tiantai": 0.90},
                    "definition": "諸法之真實相狀，無生無滅，離一切虛妄之虛空常住。",
                    "synapses": []
                },
                "T0003": {
                    "id": "T0003",
                    "canonical": "般若波羅蜜多",
                    "aliases": ["般若", "大智慧"],
                    "weights": {"tiantai": 0.98},
                    "definition": "能度脫生死彼岸之究竟大智慧，照見五蘊皆空。",
                    "synapses": []
                }
            }
        }
        return parse_manifest(data)

    def test_dros_core_py_pipeline(self):
        manifest = self.get_mock_manifest()
        engine = DrosEngine(manifest)

        # 1. 測試 O(1) 內存尋址能力
        node_t0001 = engine.weaver.get_node("T0001")
        self.assertIsNotNone(node_t0001)
        self.assertEqual(node_t0001.canonical, "真如")
        self.assertIsNone(engine.weaver.get_node("T9999"))

        # 2. 測試最長匹配優先掃描 (LMF Scanner)
        input_text = "當知「般若波羅蜜多」即是諸法之「如如」之相，不可言說。"
        result = engine.process(input_text, "vajra", 0.5)

        matched_texts = [m.matched_text for m in result.matches]
        self.assertIn("般若波羅蜜多", matched_texts)
        self.assertNotIn("般若", matched_texts)
        self.assertIn("如如", matched_texts)

        # 3. 測試拓撲鄰域擴展與衰減 (Decay & Filters)
        self.assertEqual(len(result.active_neighbors), 1)
        neighbor = result.active_neighbors[0]
        self.assertEqual(neighbor.node_id, "T0002")
        self.assertEqual(neighbor.weight, 0.5) # 1.0 * 0.5 衰減

        # 4. 測試 GuardVM 金剛模式 (Vajra - Strict)
        vajra_prompt = result.context_prompt
        self.assertIn("DROS 拓撲義理網格", vajra_prompt)
        self.assertIn("一切諸法之真實本性", vajra_prompt)
        self.assertNotIn("關聯拓撲鄰居", vajra_prompt)
        self.assertIn("金剛契約已生效", vajra_prompt)

        # 5. 測試 GuardVM 菩薩模式 (Prajna - Interpretive)
        prajna_result = engine.process(input_text, "prajna", 0.5)
        prajna_prompt = prajna_result.context_prompt
        self.assertIn("關聯拓撲鄰居", prajna_prompt)
        self.assertIn("實相 (T0002)", prajna_prompt)
        self.assertIn("菩薩契約已生效", prajna_prompt)

        print("\n🎉 [dros-core-py] 所有 14 項核心 Python 斷言測試均 100% 成功通過！\n")

if __name__ == "__main__":
    unittest.main()
