<template>
  <div class="home-page">
    <section class="hero">
      <div>
        <p class="eyebrow">TURISTIČKA AGENCIJA</p>
        <h1>Rezerviraj dostupnu destinaciju</h1>
        <p class="subtitle">
          Odaberi jednu od slobodnih lokacija i pošalji rezervaciju.
        </p>

        <v-btn color="primary" size="large" @click="scrollToForm">
          Rezerviraj odmah
        </v-btn>
      </div>
    </section>

    <section class="destinations">
      <h2>Dostupne destinacije</h2>

      <div class="destination-grid">
        <v-card
          v-for="d in slobodneDestinacije"
          :key="d.id"
          class="destination-card"
        >
          <v-card-title>{{ d.naziv }}</v-card-title>

          <v-card-text>
            <p>{{ d.grad }}, {{ d.drzava }}</p>
            <h3>{{ d.cijena }} €</h3>
          </v-card-text>

          <v-card-actions>
            <v-btn color="primary" @click="selectDestination(d)">
              Rezerviraj
            </v-btn>
          </v-card-actions>
        </v-card>
      </div>
    </section>

    <section ref="formSection" class="reservation-form">
      <h2>Forma za rezervaciju</h2>

      <v-text-field
        v-model="form.ime"
        label="Ime"
        append-inner-icon="mdi-account"
      />

      <v-text-field
        v-model="form.prezime"
        label="Prezime"
        append-inner-icon="mdi-account-outline"
      />

      <v-text-field
        v-model="form.email"
        label="Email"
        append-inner-icon="mdi-email"
      />

      <v-text-field
        v-model="form.telefon"
        label="Telefon"
        append-inner-icon="mdi-phone"
      />

      <v-select
        v-model="form.destinacija_id"
        label="Slobodna destinacija"
        :items="destinacijaOptions"
        item-title="title"
        item-value="value"
        append-inner-icon="mdi-map-marker"
      />

      <v-text-field
        v-model="form.datum_rezervacije"
        label="Datum rezervacije"
        type="date"
      />

      <v-text-field
        v-model="form.broj_osoba"
        label="Broj osoba"
        type="number"
        append-inner-icon="mdi-account-group"
      />

      <v-btn color="primary" size="large" @click="submitReservation">
        Potvrdi rezervaciju
      </v-btn>
    </section>

    <v-snackbar v-model="snackbar.show" :timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from "vue";

const API = "http://127.0.0.1:5000/api";

const destinacije = ref([]);
const rezervacije = ref([]);
const formSection = ref(null);

const snackbar = reactive({
  show: false,
  text: "",
});

const form = reactive({
  ime: "",
  prezime: "",
  email: "",
  telefon: "",
  destinacija_id: "",
  datum_rezervacije: "",
  broj_osoba: 1,
});

const zauzeteDestinacije = computed(() => {
  return new Set(
    rezervacije.value
      .filter((r) => r.status === "aktivna")
      .map((r) => r.destinacija_id)
  );
});

const slobodneDestinacije = computed(() => {
  return destinacije.value.filter((d) => !zauzeteDestinacije.value.has(d.id));
});

const destinacijaOptions = computed(() => {
  return slobodneDestinacije.value.map((d) => ({
    title: `${d.naziv} - ${d.grad}, ${d.drzava} (${d.cijena} €)`,
    value: d.id,
  }));
});

async function loadData() {
  const destinacijeRes = await fetch(`${API}/destinacije?page=1&per_page=100`);
  const destinacijeData = await destinacijeRes.json();
  destinacije.value = destinacijeData.items || destinacijeData;

  const rezervacijeRes = await fetch(`${API}/rezervacije?page=1&per_page=100`);
  const rezervacijeData = await rezervacijeRes.json();
  rezervacije.value = rezervacijeData.items || rezervacijeData;
}

function scrollToForm() {
  formSection.value?.scrollIntoView({ behavior: "smooth" });
}

function selectDestination(destinacija) {
  form.destinacija_id = destinacija.id;
  scrollToForm();
}

async function submitReservation() {
  if (
    !form.ime ||
    !form.prezime ||
    !form.email ||
    !form.destinacija_id ||
    !form.datum_rezervacije ||
    !form.broj_osoba
  ) {
    snackbar.text = "Popuni sva obavezna polja.";
    snackbar.show = true;
    return;
  }

  const klijentRes = await fetch(`${API}/klijenti`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      ime: form.ime,
      prezime: form.prezime,
      email: form.email,
      telefon: form.telefon,
    }),
  });

  if (!klijentRes.ok) {
    snackbar.text = "Greška pri kreiranju klijenta.";
    snackbar.show = true;
    return;
  }

  const klijent = await klijentRes.json();

  const rezervacijaRes = await fetch(`${API}/rezervacije`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      klijent_id: klijent.id,
      destinacija_id: form.destinacija_id,
      datum_rezervacije: form.datum_rezervacije,
      broj_osoba: Number(form.broj_osoba),
      status: "aktivna",
    }),
  });

  if (!rezervacijaRes.ok) {
    snackbar.text = "Greška pri rezervaciji.";
    snackbar.show = true;
    return;
  }

  snackbar.text = "Rezervacija je uspješno kreirana.";
  snackbar.show = true;

  form.ime = "";
  form.prezime = "";
  form.email = "";
  form.telefon = "";
  form.destinacija_id = "";
  form.datum_rezervacije = "";
  form.broj_osoba = 1;

  await loadData();
}

onMounted(loadData);
</script>

<style scoped>
.home-page {
  display: flex;
  flex-direction: column;
  gap: 34px;
}

.hero {
  min-height: 320px;
  border-radius: 26px;
  padding: 48px;
  background: linear-gradient(135deg, #1565c0, #26a69a);
  display: flex;
  align-items: center;
  color: white;
}

.eyebrow {
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 3px;
  margin-bottom: 12px;
}

.hero h1 {
  font-size: 48px;
  max-width: 720px;
  line-height: 1.05;
  margin-bottom: 16px;
}

.subtitle {
  font-size: 18px;
  max-width: 620px;
  margin-bottom: 28px;
}

.destinations,
.reservation-form {
  background: #181818;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 22px;
  padding: 32px;
}

.destination-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
  margin-top: 22px;
}

.destination-card {
  border-radius: 18px;
}

.reservation-form {
  max-width: 720px;
  margin: 0 auto;
  width: 100%;
}

.reservation-form :deep(.v-field__append-inner) {
  color: #42a5f5;
  opacity: 1;
}

.reservation-form :deep(.v-field) {
  border-radius: 16px;
}

@media (max-width: 850px) {
  .hero {
    padding: 32px;
  }

  .hero h1 {
    font-size: 34px;
  }

  .destination-grid {
    grid-template-columns: 1fr;
  }
}
</style>