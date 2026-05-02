import sys
import unittest

sys.path.insert(0, "backend")

from config import SIMULATION_CONFIG
from simulation.engine import GodTierEngine


class SimulationSmokeTests(unittest.TestCase):
    def setUp(self):
        self.engine = GodTierEngine(
            {
                **SIMULATION_CONFIG,
                "use_groq": False,
                "initial_agents": 6,
                "tick_delay_seconds": 0.0,
                "max_ticks": 2,
            }
        )
        self.engine.setup()

    def test_agent_snapshots_include_dimensions(self):
        agent = self.engine.agent_manager.get_all_agents()[0]
        snapshot = agent.get_snapshot()
        self.assertIn("dimensions", snapshot)
        self.assertGreaterEqual(len(snapshot["dimensions"]), 12)

    def test_world_snapshot_exposes_all_dimensions(self):
        self.engine.tick()
        dims = self.engine.world_state.get_dimensional_snapshot(
            self.engine.agent_manager.get_all_agents()
        )["dimensions"]
        self.assertEqual(len(dims), 12)
        self.assertIn("economic", dims)
        self.assertIn("causal", dims)

    def test_feature_registry_seeded(self):
        features = self.engine.feature_registry.list_features()
        self.assertGreaterEqual(len(features), 12)
        self.assertTrue(any(item["feature_id"] == "bio.stress_load" for item in features))

    def test_causal_records_accumulate(self):
        for _ in range(2):
            self.engine.tick()
        nodes = len(self.engine.causal_ledger.nodes)
        self.assertGreater(nodes, 0)

    def test_health_fields_exist_on_agent_snapshot(self):
        agent = self.engine.agent_manager.get_all_agents()[0]
        snapshot = agent.get_snapshot()
        self.assertIn("is_sick", snapshot)
        self.assertIn("illness_severity", snapshot)
        self.assertIn("disease_name", snapshot)


if __name__ == "__main__":
    unittest.main()
