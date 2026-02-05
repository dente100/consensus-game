from simulator.strategy import Strategy
from simulator.blockchain import Block
import random

class MaStrategieOptimisee(Strategy):

    def should_mine_block(self) -> bool:
        """Décide si on crée un bloc à ce tick."""
        # miner si pas de fork en cours
        if self.blockchain.has_fork():
            return False

        # Miner si notre chaîne est plus courte que la hauteur moyenne estimée
        # (ici, on suppose que la hauteur moyenne est proche de la hauteur max moins 2)
        max_height = max(self.blockchain.blocks_by_height.keys())
        if self.blockchain.height < max_height - 2:
            return True

        # Sinon, miner avec une probabilité de 50% pour éviter de surcharger le réseau
        return random.random() < 0.5

    def on_block_received(self, block: Block, sender_id: str) -> bool:
        """Décide si on relaye ce bloc aux autres nœuds."""
        # Ne pas relayer les blocs qui causeraient un fork
        if self.blockchain.has_fork():
            return False

        # Relayer uniquement les blocs qui prolongent notre chaîne principale
        current_head = self.blockchain.get_head()
        if block.height > current_head.height + 1:
            return False  # Trop en avance, probablement un fork

        return True

    def choose_parent_block(self) -> str:
        """Choisit le parent du nouveau bloc."""
        # Toujours choisir le dernier bloc de la chaîne principale
        # sauf si un fork est en cours, auquel cas on choisit le bloc le plus long
        if self.blockchain.has_fork():
            # Choisir la chaîne la plus longue parmi les forks
            main_chain = self.blockchain.get_main_chain()
            all_tips = self.blockchain.get_all_tips()
            longest_chain_tip = max(all_tips, key=lambda b: b.height)
            return longest_chain_tip.hash

        return self.blockchain.get_head().hash