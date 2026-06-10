<template>
  <section class="hero">
    <div class="hero-content">
      <div>
        <p class="eyebrow">Turistička agencija</p>

        <h1>
          Pametno upravljanje putovanjima i rezervacijama
        </h1>

        <p class="subtitle">
          Organizuj destinacije, klijente, zaposlenike i rezervacije kroz moderan administracijski panel.
        </p>

        <div class="actions">
          <v-btn
            color="primary"
            size="large"
            rounded="xl"
            @click="$emit('change-tab', 'rezervacije')"
          >
            Rezervacije
          </v-btn>

          <v-btn
            variant="tonal"
            size="large"
            rounded="xl"
            @click="$emit('change-tab', 'destinacije')"
          >
            Destinacije
          </v-btn>
        </div>
      </div>

      <v-card class="overview" rounded="xl" elevation="0">
        <p class="overview-title">Brzi pregled</p>

        <div class="stat">
          <span>Destinacije</span>
          <strong>{{ stats.broj_destinacija }}</strong>
        </div>

        <div class="stat">
          <span>Klijenti</span>
          <strong>{{ stats.broj_klijenata }}</strong>
        </div>

        <div class="stat">
          <span>Rezervacije</span>
          <strong>{{ stats.broj_rezervacija }}</strong>
        </div>

        <div class="stat">
          <span>Aktivne</span>
          <strong>{{ stats.aktivne_rezervacije }}</strong>
        </div>
      </v-card>
    </div>
  </section>
</template>

<script setup>
defineProps({
  stats: {
    type: Object,
    required: true,
  },
});

defineEmits(["change-tab"]);
</script>

<style scoped>
.hero {
  position: relative;
  overflow: hidden;
  margin-bottom: 42px;
  padding: 56px;
  border-radius: 28px;
  background:
    linear-gradient(135deg, rgba(33, 150, 243, 0.95), rgba(0, 188, 212, 0.65)),
    url("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1600&q=80");
  background-size: cover;
  background-position: center;
  color: white;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, rgba(0,0,0,.62), rgba(0,0,0,.25));
}

.hero-content {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1.5fr 0.8fr;
  gap: 36px;
  align-items: center;
}

.eyebrow {
  margin-bottom: 14px;
  color: #bbdefb;
  text-transform: uppercase;
  letter-spacing: 3px;
  font-size: 13px;
  font-weight: 800;
}

h1 {
  max-width: 760px;
  font-size: clamp(36px, 5vw, 64px);
  line-height: 1;
  font-weight: 900;
}

.subtitle {
  max-width: 620px;
  margin-top: 20px;
  color: rgba(255,255,255,.85);
  font-size: 19px;
}

.actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 30px;
}

.overview {
  padding: 24px;
  background: rgba(18, 18, 18, 0.72);
  color: white;
  backdrop-filter: blur(16px);
  border: 1px solid rgba(255,255,255,.16);
}

.overview-title {
  margin-bottom: 16px;
  font-size: 22px;
  font-weight: 800;
}

.stat {
  display: flex;
  justify-content: space-between;
  padding: 15px 0;
  border-bottom: 1px solid rgba(255,255,255,.12);
}

.stat:last-child {
  border-bottom: 0;
}

.stat span {
  color: rgba(255,255,255,.72);
}

.stat strong {
  font-size: 24px;
}

@media (max-width: 900px) {
  .hero {
    padding: 34px;
  }

  .hero-content {
    grid-template-columns: 1fr;
  }
}
</style>