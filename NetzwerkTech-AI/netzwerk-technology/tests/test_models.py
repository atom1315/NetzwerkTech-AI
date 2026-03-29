"""Tests für den Anomalie-Detektor."""

import numpy as np
import pytest

from src.models.anomaly_detector import (
    AnomalyDetector,
    AnomalyResult,
    DetectionResults,
)


class TestAnomalyDetector:
    """Tests für die AnomalyDetector-Klasse."""

    def test_initialization(self):
        detector = AnomalyDetector(input_dim=64, latent_dim=16)
        assert detector.input_dim == 64
        assert detector.latent_dim == 16
        assert detector.threshold == "auto"
        assert detector.sensitivity == 0.95

    def test_fit_returns_history(self):
        detector = AnomalyDetector(input_dim=32)
        data = np.random.randn(500, 32).astype(np.float32)
        history = detector.fit(data, epochs=10)

        assert "epochs" in history
        assert "final_loss" in history
        assert "threshold" in history
        assert history["epochs"] == 10

    def test_predict_requires_fit(self):
        detector = AnomalyDetector()
        data = np.random.randn(100, 128).astype(np.float32)

        with pytest.raises(RuntimeError, match="trainiert"):
            detector.predict(data)

    def test_predict_returns_results(self):
        detector = AnomalyDetector(input_dim=32)
        train_data = np.random.randn(1000, 32).astype(np.float32)
        detector.fit(train_data, epochs=5)

        test_data = np.random.randn(200, 32).astype(np.float32)
        results = detector.predict(test_data)

        assert isinstance(results, DetectionResults)
        assert results.total_samples == 200
        assert results.processing_time_ms > 0
        assert all(isinstance(a, AnomalyResult) for a in results.anomalies)

    def test_anomaly_rate(self):
        results = DetectionResults(
            anomalies=[
                AnomalyResult(0.0, 0.95, "ddos"),
                AnomalyResult(0.0, 0.88, "port_scan"),
            ],
            total_samples=100,
            processing_time_ms=1.5,
            model_confidence=0.95,
        )
        assert results.anomaly_rate == 0.02

    def test_is_critical(self):
        critical = AnomalyResult(0.0, 0.95, "ddos")
        normal = AnomalyResult(0.0, 0.5, "port_scan")

        assert critical.is_critical is True
        assert normal.is_critical is False

    def test_custom_threshold(self):
        detector = AnomalyDetector(threshold=0.5)
        data = np.random.randn(100, 128).astype(np.float32)
        history = detector.fit(data)
        assert detector._threshold_value == 0.5


class TestTopologyMapper:
    """Tests für den TopologyMapper."""

    def test_discover(self):
        from src.models.topology_mapper import TopologyMapper

        mapper = TopologyMapper(embedding_dim=32)
        topology = mapper.discover("10.0.0.0/24")

        assert topology.num_nodes > 0
        assert topology.num_edges > 0
        assert all(n.embedding is not None for n in topology.nodes)

    def test_adjacency_matrix(self):
        from src.models.topology_mapper import TopologyMapper

        mapper = TopologyMapper()
        topology = mapper.discover("10.0.0.0/24")
        adj = topology.get_adjacency_matrix()

        assert adj.shape == (topology.num_nodes, topology.num_nodes)
        # Symmetrisch (ungerichteter Graph)
        np.testing.assert_array_equal(adj, adj.T)

    def test_resilience_analysis(self):
        from src.models.topology_mapper import TopologyMapper, ResilienceReport

        mapper = TopologyMapper()
        topology = mapper.discover("10.0.0.0/24")
        report = mapper.analyze_resilience(topology)

        assert isinstance(report, ResilienceReport)
        assert 0 <= report.overall_score <= 1
        assert 0 <= report.redundancy_score <= 1
        assert isinstance(report.recommendations, list)
