"""
Stratégie d'exemple pour Consensus-as-a-Game.

Cette stratégie illustre comment implémenter une stratégie simple.

Comportement:
- Accepte tous les blocs reçus
- Mine régulièrement (tous les 10 ticks)
- Suit toujours la chaîne la plus longue
- Relaie tous les nouveaux blocs
"""
from simulator.strategy import Strategy
from simulator.blockchain import Block


class ExampleStrategy(Strategy):
    """
    Stratégie d'exemple simple.
    
    Points clés:
    1. Hérite de Strategy
    2. Implémente les 3 méthodes abstraites
    3. N'a accès qu'aux informations locales
    """
    
    def __init__(self, node_id: str):
        """
        Initialise la stratégie.
        
        Vous pouvez ajouter des paramètres personnalisés ici.
        """
        super().__init__(node_id)
        
        # Paramètre : fréquence de minage
        self.mining_frequency = 10
        
        # Dernière fois qu'on a miné
        self.last_mine_tick = 0
        
        # Vous pouvez ajouter d'autres variables d'état local
        self.blocks_seen = set()
    
    def on_block_received(self, block: Block, sender_id: str) -> bool:
        """
        Traite un bloc reçu.
        
        Cette méthode est appelée à chaque fois qu'un bloc arrive.
        
        Args:
            block: Le bloc reçu
            sender_id: Identifiant du nœud qui a envoyé le bloc
            
        Returns:
            True pour relayer le bloc aux autres nœuds
        """
        # Vérifier si on connaît déjà ce bloc
        if block.hash in self.blocks_seen:
            # Bloc déjà vu, ne pas relayer
            return False
        
        # Marquer comme vu
        self.blocks_seen.add(block.hash)
        
        # Ajouter le bloc à notre blockchain locale
        # La blockchain gère automatiquement les orphelins, les forks, etc.
        assert self.blockchain is not None
        added = self.blockchain.add_block(block)
        
        # Si le bloc a été ajouté (nouveau et valide), le relayer
        if added:
            return True
        
        return False
    
    def should_mine_block(self) -> bool:
        """
        Décide s'il faut essayer de miner un bloc maintenant.
        
        Cette méthode est appelée à chaque tick.
        
        Returns:
            True pour commencer à miner
        """
        # Stratégie simple : miner tous les N ticks
        if self.current_tick - self.last_mine_tick >= self.mining_frequency:
            self.last_mine_tick = self.current_tick
            return True
        
        return False
    
    def choose_parent_block(self) -> str:
        """
        Choisit le bloc parent pour le prochain bloc à miner.
        
        C'est ici que vous décidez quelle branche suivre en cas de fork.
        
        Returns:
            Hash du bloc parent
        """
        # Stratégie simple : toujours suivre la tête de la chaîne principale
        # (la plus longue selon la règle par défaut)
        assert self.blockchain is not None
        head = self.blockchain.get_head()
        return head.hash


# IMPORTANT : La classe doit hériter de Strategy
# et être définie dans ce fichier pour être détectée automatiquement.
