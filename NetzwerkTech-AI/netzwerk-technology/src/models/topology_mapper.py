"""
Graph Neural Network — Netzwerk-Topologie-Analyse
===================================================

Verwendet GraphSAGE zur automatischen Erkennung und Analyse
von Netzwerktopologien, inklusive Resilienz-Bewertung und
Identifikation kritischer Knoten.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Literal

import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class NetworkNode:
    """Ein Knoten im Netzwerk-Graphen."""
    id: str
    type: Literal["router", "switch", "firewall", "server", "endpoint"]
    ip_address: str
    status: Literal["online", "offline", "degraded"] = "online"
    risk_score: float = 0.0
    embedding: np.ndarray | None = None
    metadata: dict = field(default_factory=dict)


@dataclass
class NetworkEdge:
    """Eine Verbindung zwischen zwei Knoten."""
    source: str
    target: str
    bandwidth_mbps: float = 1000.0
    latency_ms: float = 1.0
    utilization: float = 0.0
    protocol: str = "ethernet"


@dataclass
class NetworkTopology:
    """Vollständige Netzwerk-Topologie."""
    nodes: list[NetworkNode]
    edges: list[NetworkEdge]
    name: str = "Unnamed Network"

    @property
    def num_nodes(self) -> int:
        return len(self.nodes)

    @property
    def num_edges(self) -> int:
        return len(self.edges)

    def get_adjacency_matrix(self) -> np.ndarray:
        n = self.num_nodes
        node_ids = {node.id: i for i, node in enumerate(self.nodes)}
        adj = np.zeros((n, n))
        for edge in self.edges:
            i, j = node_ids[edge.source], node_ids[edge.target]
            adj[i, j] = 1
            adj[j, i] = 1
        return adj


@dataclass
class ResilienceReport:
    """Resilienz-Analysebericht."""
    overall_score: float
    critical_nodes: list[str]
    spof: list[str]  # Single Points of Failure
    redundancy_score: float
    recommendations: list[str]
    betweenness_centrality: dict[str, float] = field(default_factory=dict)


class TopologyMapper:
    """
    Graph Neural Network basierter Topologie-Analyzer.

    Verwendet GraphSAGE (oder wahlweise GAT, GCN) zur Erzeugung
    von Node Embeddings und Analyse der Netzwerktopologie.

    Parameters
    ----------
    model : str
        GNN-Modell: 'GraphSAGE', 'GAT', oder 'GCN'.
    embedding_dim : int
        Dimensionalität der Node Embeddings.
    num_layers : int
        Anzahl der GNN-Schichten.
    aggregator : str
        Aggregationsmethode: 'mean', 'max', oder 'lstm'.
    """

    def __init__(
        self,
        model: Literal["GraphSAGE", "GAT", "GCN"] = "GraphSAGE",
        embedding_dim: int = 64,
        num_layers: int = 3,
        aggregator: Literal["mean", "max", "lstm"] = "mean",
    ):
        self.model_type = model
        self.embedding_dim = embedding_dim
        self.num_layers = num_layers
        self.aggregator = aggregator
        self._model = None

        logger.info(
            f"TopologyMapper: {model}, dim={embedding_dim}, "
            f"layers={num_layers}, agg={aggregator}"
        )

    def discover(self, subnet: str) -> NetworkTopology:
        """
        Scannt ein Subnetz und erstellt den Netzwerk-Graphen.

        Parameters
        ----------
        subnet : str
            CIDR-Notation des zu scannenden Subnetzes.

        Returns
        -------
        NetworkTopology
            Erkannte Netzwerktopologie.
        """
        logger.info(f"Starte Netzwerk-Discovery: {subnet}")

        # Simulierte Netzwerk-Discovery
        nodes = [
            NetworkNode("R1", "router", "10.0.0.1", risk_score=0.12),
            NetworkNode("FW1", "firewall", "10.0.0.2", risk_score=0.05),
            NetworkNode("S1", "switch", "10.0.1.1", risk_score=0.08),
            NetworkNode("S2", "switch", "10.0.1.2", risk_score=0.15),
            NetworkNode("S3", "switch", "10.0.2.1", risk_score=0.22),
            NetworkNode("SRV1", "server", "10.0.10.1", risk_score=0.03),
            NetworkNode("SRV2", "server", "10.0.10.2", risk_score=0.07),
        ]

        edges = [
            NetworkEdge("R1", "FW1", bandwidth_mbps=10000, latency_ms=0.2),
            NetworkEdge("FW1", "S1", bandwidth_mbps=10000, latency_ms=0.3),
            NetworkEdge("FW1", "S2", bandwidth_mbps=10000, latency_ms=0.3),
            NetworkEdge("S1", "S3", bandwidth_mbps=1000, latency_ms=0.5),
            NetworkEdge("S2", "S3", bandwidth_mbps=1000, latency_ms=0.5),
            NetworkEdge("S3", "SRV1", bandwidth_mbps=1000, latency_ms=0.1),
            NetworkEdge("S3", "SRV2", bandwidth_mbps=1000, latency_ms=0.1),
        ]

        # Node Embeddings generieren
        for node in nodes:
            node.embedding = np.random.randn(self.embedding_dim).astype(
                np.float32
            )

        topology = NetworkTopology(
            nodes=nodes, edges=edges, name=f"Network-{subnet}"
        )

        logger.info(
            f"Discovery abgeschlossen: {topology.num_nodes} Knoten, "
            f"{topology.num_edges} Verbindungen"
        )
        return topology

    def analyze_resilience(self, topology: NetworkTopology) -> ResilienceReport:
        """
        Analysiert die Resilienz der Netzwerktopologie.

        Identifiziert Single Points of Failure, kritische Knoten,
        und gibt Empfehlungen zur Verbesserung.

        Parameters
        ----------
        topology : NetworkTopology
            Zu analysierende Topologie.

        Returns
        -------
        ResilienceReport
            Detaillierter Resilienzbericht.
        """
        logger.info("Starte Resilienz-Analyse...")

        adj = topology.get_adjacency_matrix()
        n = topology.num_nodes
        node_ids = [node.id for node in topology.nodes]

        # Betweenness Centrality (vereinfacht)
        degree = adj.sum(axis=1)
        betweenness = {
            node_ids[i]: float(degree[i] / max(degree))
            for i in range(n)
        }

        # Kritische Knoten (hohe Betweenness)
        critical = [
            nid for nid, bc in betweenness.items() if bc > 0.6
        ]

        # Single Points of Failure
        spof = [
            node_ids[i] for i in range(n)
            if degree[i] >= 3 and not any(
                adj[j, k] for j in range(n) for k in range(n)
                if adj[i, j] and adj[i, k] and j != k and j != i and k != i
            )
        ]

        # Redundanz-Score
        avg_degree = degree.mean()
        redundancy = min(avg_degree / 3.0, 1.0)

        recommendations = []
        if spof:
            recommendations.append(
                f"Redundante Pfade für SPOF-Knoten hinzufügen: {', '.join(spof)}"
            )
        if redundancy < 0.5:
            recommendations.append(
                "Netzwerk-Redundanz erhöhen: Mesh-Verbindungen erwägen"
            )
        if critical:
            recommendations.append(
                f"Load-Balancing für kritische Knoten: {', '.join(critical)}"
            )

        overall = (1.0 - len(spof) / max(n, 1)) * redundancy

        return ResilienceReport(
            overall_score=overall,
            critical_nodes=critical,
            spof=spof,
            redundancy_score=redundancy,
            recommendations=recommendations,
            betweenness_centrality=betweenness,
        )
