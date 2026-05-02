import re

with open(r'C:\Users\amegh\OneDrive\Desktop\real\backend\agents\agent.py', 'r', encoding='utf-8') as f:
    content = f.read()

old = "# Normal Needs Decay"

old_section = """# Normal Needs Decay
        hunger_rate   = 2.0 + self.traits.get("risk_tolerance", 0.3)
        energy_rate   = 1.5 + self.traits.get("ambition", 0.5) * 1.2
        loneliness_penalty = self.traits.get("sociability", 0.5) * 0.5 \\
                             if self.friend_count == 0 else 0.0
        happiness_rate = 1.0 + loneliness_penalty

        # Sickness accelerates needs dropping
        if self.is_sick:
            hunger_rate *= 1.5
            energy_rate *= 2.0
            happiness_rate += 1.0

        # Married agents are happier (smaller happiness decay)
        if self.is_married:
            happiness_rate = max(0.0, happiness_rate - 0.5)

        # Non-linear starvation panic
        if self.hunger < 30.0:
            hunger_rate *= 2.0

        self.hunger    = max(0.0, self.hunger    - hunger_rate)
        self.energy    = max(0.0, self.energy    - energy_rate)
        self.happiness = max(0.0, self.happiness - happiness_rate)
        self.age_ticks += 1"""

new_section = """# Normal Needs Decay
        hunger_rate   = 2.0 + self.traits.get("risk_tolerance", 0.3)
        energy_rate   = 1.5 + self.traits.get("ambition", 0.5) * 1.2
        loneliness_penalty = self.traits.get("sociability", 0.5) * 0.5 \\
                             if self.friend_count == 0 else 0.0
        happiness_rate = 1.0 + loneliness_penalty

        # Sickness accelerates needs dropping
        if self.is_sick:
            hunger_rate *= 1.5
            energy_rate *= 2.0
            happiness_rate += 1.0

        # Married agents are happier (smaller happiness decay)
        if self.is_married:
            happiness_rate = max(0.0, happiness_rate - 0.5)

        # Anhedonia deepens sadness
        if self.anhedonia_severity > 0.3:
            happiness_rate *= (1.0 + self.anhedonia_severity * 0.5)
        if self.rumination_depth > 0.4:
            happiness_rate *= (1.0 + self.rumination_depth * 0.3)

        # Experiential avoidance increases needs decay rate
        if self.experiential_avoidance > 0.5:
            energy_rate *= 1.2
            happiness_rate += 1.0

        # Psychomotor retardation slows action
        if self.psychomotor_retardation > 0.3:
            energy_rate *= (1.0 - self.psychomotor_retardation * 0.3)

        # Emotional blunting reduces happiness response
        if self.emotional_blunting > 0.3:
            happiness_rate *= (1.0 + self.emotional_blunting * 0.2)

        # Suppression increases emotional decay
        if self.suppression_tendency > 0.5:
            happiness_rate *= 1.15

        # Non-linear starvation panic
        if self.hunger < 30.0:
            hunger_rate *= 2.0

        self.hunger    = max(0.0, self.hunger    - hunger_rate)
        self.energy    = max(0.0, self.energy    - energy_rate)
        self.happiness = max(0.0, self.happiness - happiness_rate)
        self.age_ticks += 1

        # Core Affect Updates
        valence_shift = (50.0 - self.happiness) * 0.003
        if self.rumination_depth > 0.3:
            valence_shift -= self.rumination_depth * 0.01
        if self.anhedonia_severity > 0.2:
            valence_shift -= self.anhedonia_severity * 0.015
        self.affect_valence = max(0.0, min(1.0, self.affect_valence + valence_shift))

        arousal_shift = (self.is_sick * 0.01) + (self.energy < 30.0 * -0.005)
        self.affect_arousal = max(0.0, min(1.0, self.affect_arousal + arousal_shift))

        if self.hunger < 20.0 or self.energy < 20.0:
            self.affect_dominance = max(0.0, self.affect_dominance - 0.01)
        elif self.happiness > 70.0 and self.energy > 60.0:
            self.affect_dominance = min(1.0, self.affect_dominance + 0.005)

        if self.happiness < 30.0:
            self.emotional_granularity = max(0.0, self.emotional_granularity - 0.005)

        if self.happiness < 40.0:
            self.mood_congruent_memory = min(1.0, self.mood_congruent_memory + 0.002)

        self.affect_valence = self.affect_valence + (0.5 - self.affect_valence) * self.hedonic_adaptation_rate * 0.001"""

if old_section in content:
    content = content.replace(old_section, new_section)
    print("Replaced decay section")
else:
    print("ERROR: Could not find old section to replace")
    print("Trying to locate similar...")
    import re
    pattern = r'#\s*Normal\s+Needs\s+Decay.*?self\.age_ticks\s*\+=\s*1'
    match = re.search(pattern, content)
    if match:
        print(f"Found match at position: {match.start()}")
        print(repr(content[match.start():match.start()+100]))

with open(r'C:\Users\amegh\OneDrive\Desktop\real\backend\agents\agent.py', 'w', encoding='utf-8') as f:
    f.write(content)