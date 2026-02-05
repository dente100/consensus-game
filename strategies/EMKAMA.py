from simulator.strategy import Strategy
from simulator.blockchain import Block

class MaStrategie(Strategy):
    
    def should_mine_block(self) -> bool:
        """Decide si on cree un bloc ce tick (1000 ticks total)"""
        return True  # Simple: miner toujours
    
    def on_block_received(self, block: Block, sender_id: str) -> bool:
        """Decide si on relaye ce bloc aux autres"""
        return True  # Simple: relayer toujours
    
    def choose_parent_block(self) -> str:
        """Choisit le parent du nouveau bloc"""
        return self.blockchain.get_head().hash  # Simple: dernier bloc