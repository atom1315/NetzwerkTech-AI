#!/usr/bin/env python3
"""
NetzwerkTech AI — Schnellstart-Beispiel
========================================

Demonstriert die Kernfunktionalität:
1. Anomalie-Erkennung
2. Topologie-Analyse mit GNN
3. Echtzeit-Monitoring
"""

import numpy as np


def demo_anomaly_detection():
    """Zeigt die Anomalie-Erkennung in Aktion."""
    from src.models.anomaly_detector import AnomalyDetector

    print("=" * 60)
    print("🔍 ANOMALIE-ERKENNUNG")
    print("=" * 60)

    detector = AnomalyDetector(
        input_dim=128,
        latent_dim=32,
        lstm_units=64,
        threshold="auto",
        sensitivity=0.95,
    )

    # Simulierte Trainingsdaten (normaler Verkehr)
    normal_traffic = np.random.randn(10_000, 128).astype(np.float32)

    print("\n📚 Training mit normalem Netzwerkverkehr...")
    history = detector.fit(normal_traffic, epochs=50)
    print(f"   ✅ Training abgeschlossen")
    print(f"   📉 Final Loss: {history['final_loss']}")
    print(f"   🎯 Schwellenwert: {history['threshold']:.6f}")

    # Simulierte Live-Daten (mit Anomalien)
    live_data = np.random.randn(1000, 128).astype(np.float32)

    print("\n🔎 Analysiere Live-Daten...")
    results = detector.predict(live_data)

    print(f"   📊 Analysiert: {results.total_samples} Samples")
    print(f"   ⏱️  Verarbeitung: {results.processing_time_ms:.2f} ms")
    print(f"   🎯 Modell-Konfidenz: {results.model_confidence:.1%}")
    print(f"   ⚠️  Anomalien gefunden: {len(results.anomalies)}")

    for anomaly in results.anomalies[:5]:
        status = "🔴 KRITISCH" if anomaly.is_critical else "🟡 Warnung"
        print(f"   {status} | {anomaly.type:20s} | "
              f"Score: {anomaly.score:.4f} | "
              f"Source: {anomaly.source_ip}")


def demo_topology_analysis():
    """Zeigt die GNN-basierte Topologie-Analyse."""
    from src.models.topology_mapper import TopologyMapper

    print("\n" + "=" * 60)
    print("🌐 TOPOLOGIE-ANALYSE (GraphSAGE)")
    print("=" * 60)

    mapper = TopologyMapper(
        model="GraphSAGE",
        embedding_dim=64,
        num_layers=3,
        aggregator="mean",
    )

    print("\n🔍 Netzwerk-Discovery: 10.0.0.0/24")
    topology = mapper.discover("10.0.0.0/24")

    print(f"   📡 Knoten gefunden: {topology.num_nodes}")
    print(f"   🔗 Verbindungen: {topology.num_edges}")

    print("\n🛡️ Resilienz-Analyse...")
    report = mapper.analyze_resilience(topology)

    print(f"   📊 Gesamt-Score: {report.overall_score:.2%}")
    print(f"   🔴 Kritische Knoten: {report.critical_nodes}")
    print(f"   ⚠️  Single Points of Failure: {report.spof}")
    print(f"   🔄 Redundanz-Score: {report.redundancy_score:.2%}")

    print("\n💡 Empfehlungen:")
    for rec in report.recommendations:
        print(f"   → {rec}")

    print("\n📊 Betweenness Centrality:")
    for node_id, bc in sorted(
        report.betweenness_centrality.items(),
        key=lambda x: x[1],
        reverse=True,
    ):
        bar = "█" * int(bc * 20)
        print(f"   {node_id:6s} {bar} {bc:.2f}")


if __name__ == "__main__":
    print()
    print("╔══════════════════════════════════════════╗")
    print("║     🧠 NetzwerkTech AI v2.0 — Demo      ║")
    print("╚══════════════════════════════════════════╝")

    demo_anomaly_detection()
    demo_topology_analysis()

    print("\n" + "=" * 60)
    print("✅ Demo abgeschlossen!")
    print("📖 Mehr Informationen: https://github.com/netzwerk-tech/netzwerk-ai")
    print("=" * 60)
