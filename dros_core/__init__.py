from dros_core.types import (
    DrosManifest,
    DrosNode,
    DrosSynapse,
    DrosMatch,
    ActiveNeighbor,
    parse_manifest
)
from dros_core.weaver import DrosWeaver
from dros_core.navigator import DrosNavigator
from dros_core.guard import DrosGuardVM

class DrosProcessResult:
    def __init__(self, matches: list, active_neighbors: list, context_prompt: str):
        self.matches = matches
        self.active_neighbors = active_neighbors
        self.context_prompt = context_prompt

class DrosEngine:
    """
    📿 DROS Unified Integration Engine - Python Edition
    為 Python 各類 AI Agent (LangChain/LlamaIndex) 提供統一且開箱即用的推理網格與熔斷合約管道
    """
    def __init__(self, manifest: DrosManifest):
        self.weaver = DrosWeaver(manifest)

    def process(self, text: str, mode: str, decay_factor: float) -> DrosProcessResult:
        """
        一鍵執行完整 DROS 管道 (Weave -> Navigate -> Compile)
        """
        matches = self.weaver.weave(text)
        
        navigator = DrosNavigator(self.weaver)
        active_neighbors = navigator.navigate(matches, decay_factor)
        
        guard_vm = DrosGuardVM(self.weaver)
        context_prompt = guard_vm.compile(matches, active_neighbors, mode)
        
        return DrosProcessResult(
            matches=matches,
            active_neighbors=active_neighbors,
            context_prompt=context_prompt
        )
