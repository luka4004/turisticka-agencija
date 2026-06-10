<template>
  <div>
    <div class="section-header mb-5">
      <div>
        <p class="section-label mb-1">Pregled sistema</p>
        <h1>Dashboard</h1>
      </div>
    </div>

    <v-row>
      <v-col
        cols="12"
        sm="6"
        md="4"
        v-for="card in cards"
        :key="card.title"
      >
        <v-card class="dashboard-card" rounded="xl" elevation="0">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="card-title mb-3">
                  {{ card.title }}
                </p>

                <h2 class="card-value">
                  {{ card.value }}
                </h2>
              </div>

              <div class="card-icon">
                {{ getIcon(card.title) }}
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
defineProps({
  cards: {
    type: Array,
    required: true,
  },
});

function getIcon(title) {
  if (title.includes("destinacija")) return "🌍";
  if (title.includes("klijenata")) return "👥";
  if (title.includes("rezervacija")) return "📅";
  if (title.includes("zaposlenika")) return "💼";
  if (title.includes("Aktivne")) return "✅";
  if (title.includes("cijena")) return "💰";

  return "📊";
}
</script>

<style scoped>
.section-label {
  color: #64b5f6;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  font-size: 12px;
}

.section-header h1 {
  font-size: 34px;
  font-weight: 800;
}

.dashboard-card {
  background: #202020;
  border: 1px solid rgba(255, 255, 255, 0.06);
  transition: 0.2s ease;
}

.dashboard-card:hover {
  transform: translateY(-4px);
  border-color: rgba(33, 150, 243, 0.45);
}

.card-title {
  color: rgba(255, 255, 255, 0.7);
  font-size: 15px;
}

.card-value {
  font-size: 34px;
  font-weight: 800;
  color: white;
}

.card-icon {
  width: 52px;
  height: 52px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  background: rgba(33, 150, 243, 0.14);
}
</style>