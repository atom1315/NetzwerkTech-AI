"""
NetzwerkTech AI — Intelligente Netzwerk-Analyse & Optimierung mit KI
=====================================================================

Ein Framework für KI-gestützte Netzwerkanalyse, das modernste
Deep-Learning-Modelle mit Echtzeit-Netzwerkmonitoring verbindet.

Hauptmodule:
    - AnomalyDetector: LSTM + Autoencoder für Anomalie-Erkennung
    - TrafficAnalyzer: CNN + Attention für Traffic-Klassifikation
    - TopologyMapper: Graph Neural Network für Topologie-Analyse
    - NetworkOptimizer: Reinforcement Learning für Auto-Optimierung
    - IntrusionDetector: Transformer-basiertes IDS
    - PredictionEngine: GRU + Bayesian für Ausfallvorhersage
"""

__version__ = "2.0.0"
__author__ = "NetzwerkTech Team"

from .models.anomaly_detector import AnomalyDetector
from .models.traffic_analyzer import TrafficAnalyzer
from .models.topology_mapper import TopologyMapper
from .models.network_optimizer import NetworkOptimizer
from .models.intrusion_detector import IntrusionDetector
from .models.prediction_engine import PredictionEngine

from .ai_network_analyzer.engine import AIEngine
from .ai_network_analyzer.dashboard import Dashboard
from .ai_network_analyzer.network_profile import NetworkProfile

__all__ = [
    "AnomalyDetector",
    "TrafficAnalyzer",
    "TopologyMapper",
    "NetworkOptimizer",
    "IntrusionDetector",
    "PredictionEngine",
    "AIEngine",
    "Dashboard",
    "NetworkProfile",
]
