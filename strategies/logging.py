"""
Exemple d'utilisation de self.log() dans une stratégie.

Les étudiants peuvent utiliser self.log() pour capturer des messages
qui seront sauvegardés dans results/simulation_TIMESTAMP_logs/

Avantage: les logs sont organisés par stratégie et limités en taille.
"""
from simulator.strategy import Strategy
from simulator.blockchain import Block


class LoggingExampleStrategy(Strategy):
    """Exemple montrant comment logger dans une stratégie."""
    
    def __init__(self, node_id: str):
        super().__init__(node_id)
        self.mining_frequency = 10
        self.last_mine_tick = 0
        self.blocks_seen = set()
        
        # Log au démarrage
        self.log(f"Stratégie initialisée pour {node_id}")
    
    def on_block_received(self, block: Block, sender_id: str) -> bool:
        """Traite un bloc reçu avec logging."""
        
        if block.hash in self.blocks_seen:
            return False
        
        self.blocks_seen.add(block.hash)
        
        assert self.blockchain is not None
        added = self.blockchain.add_block(block)
        
        if added:
            # Logger les événements importants
            self.log(f"Nouveau bloc accepté: {block.block_id} de {sender_id}, hauteur {block.height}")
            return True
        else:
            self.log(f"Bloc rejeté: {block.block_id} de {sender_id}")
        
        return False
    
    def should_mine_block(self) -> bool:
        """Décide s'il faut miner."""
        if self.current_tick - self.last_mine_tick >= self.mining_frequency:
            self.last_mine_tick = self.current_tick
            self.log(f"Tentative de minage au tick {self.current_tick}")
            return True
        return False
    
    def choose_parent_block(self) -> str:
        """Choisit le bloc parent."""
        assert self.blockchain is not None
        head = self.blockchain.get_head()
        
        # Logger le choix de parent
        self.log(f"Choix du parent: {head.block_id} (hauteur {head.height})")
        
        return head.hash
