"""
Stratégie conservatrice : attend avant de décider.

Comportement:
- Attend un certain temps avant de relayer
- Mine moins fréquemment
- Privilégie la stabilité sur la vitesse

Avantages:
- Moins de forks
- Plus stable

Inconvénients:
- Plus lent à progresser
- Peut perdre en liveness
"""
from simulator.strategy import Strategy
from simulator.blockchain import Block


class ConservativeWaiter(Strategy):
    """Stratégie conservatrice qui attend."""
    
    def __init__(self, node_id: str):
        super().__init__(node_id)
        
        # Temps d'attente avant de relayer (en ticks)
        self.wait_time = 15
        
        # Fréquence de minage
        self.mining_frequency = 20
        
        # Blocs en attente : {block_hash: tick_received}
        self.pending_blocks = {}
        
        self.blocks_seen = set()
    
    def on_block_received(self, block: Block, sender_id: str) -> bool:
        """Attend avant de relayer."""
        if block.hash in self.blocks_seen:
            return False
        
        self.blocks_seen.add(block.hash)
        
        # Enregistrer le moment de réception
        self.pending_blocks[block.hash] = self.current_tick
        
        # Ajouter à la blockchain
        assert self.blockchain is not None
        self.blockchain.add_block(block)
        
        # Relayer seulement après le délai d'attente
        ticks_waiting = self.current_tick - self.pending_blocks.get(block.hash, 0)
        
        if ticks_waiting >= self.wait_time:
            return True
        
        return False
    
    def should_mine_block(self) -> bool:
        """Mine moins fréquemment."""
        return self.current_tick % self.mining_frequency == 0
    
    def choose_parent_block(self) -> str:
        """Choisit la tête après avoir attendu."""
        assert self.blockchain is not None
        return self.blockchain.get_head().hash
