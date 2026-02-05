rom simulator.strategy import Strategy
from simulator.blockchain import Block

class MaStrategie(Strategie):

    def should_mine_block(self) -> bool:
        """Décide si on crée un bloc à ce tick."""
        # Miner toujours pour maximiser la participation
        return True

    def on_block_received(self, block: Block, sender_id: str) -> bool:
        """Décide si on relaye ce bloc aux autres nœuds."""
        # Relayer toujours pour maximiser la diffusion des blocs
        return True

    def choose_parent_block(self) -> str:
        """Choisit le parent du nouveau bloc."""
        # Toujours choisir le dernier bloc de la chaîne principale
        return self.blockchain.get_head().hash