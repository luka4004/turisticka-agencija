<template>
  <v-app>
    <v-main>
      <v-container class="main-container">
        <v-tabs class="custom-tabs">
          <v-tab to="/home">Početna</v-tab>
          <v-tab to="/dashboard">Dashboard</v-tab>
          <v-tab to="/destinacije">Destinacije</v-tab>
          <v-tab to="/klijenti">Klijenti</v-tab>
          <v-tab to="/zaposlenici">Zaposlenici</v-tab>
          <v-tab to="/rezervacije">Rezervacije</v-tab>
        </v-tabs>

        <div class="content-window">
          <PublicHome v-if="currentPage === 'home'" />
          
          <DashboardCards
            v-else-if="currentPage === 'dashboard'"
            :cards="dashboardCards"
          />

          <EntityCrud
            v-else
            :entity-key="currentPage"
            :config="configs[currentPage]"
            :state="state[currentPage]"
            @open-create="openCreate"
            @open-edit="openEdit"
            @confirm-delete="confirmDelete"
            @load-entity="loadEntity"
            @finish-reservation="finishReservation"
          />
        </div>
      </v-container>

      <EntityFormDialog
        v-model="dialog"
        :edit-mode="editMode"
        :config="activeEntity ? configs[activeEntity] : null"
        :form="form"
        @save-item="saveItem"
      />

      <DeleteConfirmDialog
        v-model="deleteDialog"
        @delete-item="deleteItem"
      />

      <v-snackbar v-model="snackbar.show" :timeout="2500">
        {{ snackbar.text }}
      </v-snackbar>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";
import { useRoute } from "vue-router";

import DashboardCards from "./components/DashboardCards.vue";
import EntityCrud from "./components/EntityCrud.vue";
import EntityFormDialog from "./components/EntityFormDialog.vue";
import DeleteConfirmDialog from "./components/DeleteConfirmDialog.vue";
import PublicHome from "./components/PublicHome.vue";

const API = "http://127.0.0.1:5000/api";

const route = useRoute();

const currentPage = computed(() => {
  return route.name || "dashboard";
});

const dialog = ref(false);
const deleteDialog = ref(false);
const editMode = ref(false);
const activeEntity = ref(null);
const activeId = ref(null);
const form = reactive({});
const itemForDelete = ref(null);

const snackbar = reactive({
  show: false,
  text: "",
});

const dashboard = reactive({
  broj_destinacija: 0,
  broj_klijenata: 0,
  broj_rezervacija: 0,
  broj_zaposlenika: 0,
  aktivne_rezervacije: 0,
  prosjecna_cijena: 0,
});

const klijentOptions = ref([]);
const destinacijaOptions = ref([]);

const entityKeys = ["destinacije", "klijenti", "zaposlenici", "rezervacije"];

const state = reactive({
  destinacije: createState(),
  klijenti: createState(),
  zaposlenici: createState(),
  rezervacije: createState(),
});

function createState() {
  return {
    items: [],
    search: "",
    country: "Sve države",
    page: 1,
    perPage: 5,
    pages: 1,
    total: 0,
  };
}

const configs = computed(() => ({
  destinacije: {
    title: "Destinacije",
    path: "destinacije",
    columns: [
      { key: "id", label: "ID" },
      { key: "naziv", label: "Naziv" },
      { key: "drzava", label: "Država" },
      { key: "grad", label: "Grad" },
      { key: "cijena", label: "Cijena" },
    ],
    fields: [
      { key: "naziv", label: "Naziv" },
      { key: "drzava", label: "Država" },
      { key: "grad", label: "Grad" },
      { key: "opis", label: "Opis", type: "textarea" },
      { key: "cijena", label: "Cijena", type: "number" },
    ],
  },

  klijenti: {
    title: "Klijenti",
    path: "klijenti",
    columns: [
      { key: "id", label: "ID" },
      { key: "ime", label: "Ime" },
      { key: "prezime", label: "Prezime" },
      { key: "email", label: "Email" },
      { key: "telefon", label: "Telefon" },
    ],
    fields: [
      { key: "ime", label: "Ime" },
      { key: "prezime", label: "Prezime" },
      { key: "email", label: "Email" },
      { key: "telefon", label: "Telefon" },
    ],
  },

  zaposlenici: {
    title: "Zaposlenici",
    path: "zaposlenici",
    columns: [
      { key: "id", label: "ID" },
      { key: "ime", label: "Ime" },
      { key: "prezime", label: "Prezime" },
      { key: "email", label: "Email" },
      { key: "pozicija", label: "Pozicija" },
    ],
    fields: [
      { key: "ime", label: "Ime" },
      { key: "prezime", label: "Prezime" },
      { key: "email", label: "Email" },
      { key: "pozicija", label: "Pozicija" },
    ],
  },

  rezervacije: {
    title: "Rezervacije",
    path: "rezervacije",
    columns: [
      { key: "id", label: "ID" },
      { key: "klijent.ime", label: "Klijent ime" },
      { key: "klijent.prezime", label: "Klijent prezime" },
      { key: "destinacija.naziv", label: "Destinacija" },
      { key: "datum_rezervacije", label: "Datum" },
      { key: "broj_osoba", label: "Broj osoba" },
      { key: "status", label: "Status" },
    ],
    fields: [
      {
        key: "klijent_id",
        label: "Klijent",
        type: "select",
        items: klijentOptions.value,
      },
      {
        key: "destinacija_id",
        label: "Slobodna destinacija",
        type: "select",
        items: destinacijaOptions.value,
      },
      { key: "datum_rezervacije", label: "Datum rezervacije", type: "date" },
      { key: "broj_osoba", label: "Broj osoba", type: "number" },
      {
        key: "status",
        label: "Status",
        type: "select",
        items: [
          { title: "aktivna", value: "aktivna" },
          { title: "otkazana", value: "otkazana" },
          { title: "završena", value: "završena" },
        ],
      },
    ],
  },
}));

const dashboardCards = computed(() => [
  { title: "Broj destinacija", value: dashboard.broj_destinacija },
  { title: "Broj klijenata", value: dashboard.broj_klijenata },
  { title: "Broj rezervacija", value: dashboard.broj_rezervacija },
  { title: "Broj zaposlenika", value: dashboard.broj_zaposlenika },
  { title: "Aktivne rezervacije", value: dashboard.aktivne_rezervacije },
  { title: "Prosječna cijena", value: dashboard.prosjecna_cijena },
]);

async function loadDashboard() {
  const res = await fetch(`${API}/dashboard`);
  const data = await res.json();
  Object.assign(dashboard, data);
}

async function loadEntity(entityKey) {
  const currentState = state[entityKey];
  const path = configs.value[entityKey].path;

  let url = `${API}/${path}?search=${encodeURIComponent(
    currentState.search || ""
  )}&page=${currentState.page}&per_page=${currentState.perPage}`;

  if (entityKey === "rezervacije" && currentState.country !== "Sve države") {
    url += `&drzava=${encodeURIComponent(currentState.country)}`;
  }

  const res = await fetch(url);
  const data = await res.json();

  currentState.items = data.items || data;
  currentState.total = data.total || currentState.items.length;
  currentState.page = data.page || 1;
  currentState.pages = data.pages || 1;
}

async function loadAll() {
  await loadDashboard();

  for (const key of entityKeys) {
    await loadEntity(key);
  }

  await loadSelectOptions();
}

async function loadSelectOptions() {
  const klijentiRes = await fetch(`${API}/klijenti?page=1&per_page=100`);
  const klijentiData = await klijentiRes.json();

  klijentOptions.value = (klijentiData.items || klijentiData).map((k) => ({
    title: `${k.ime} ${k.prezime}`,
    value: k.id,
  }));

  const destinacijeRes = await fetch(`${API}/destinacije?page=1&per_page=100`);
  const destinacijeData = await destinacijeRes.json();

  const rezervacijeRes = await fetch(`${API}/rezervacije?page=1&per_page=100`);
  const rezervacijeData = await rezervacijeRes.json();

  const zauzeteDestinacije = new Set(
    (rezervacijeData.items || rezervacijeData)
      .filter((r) => r.status === "aktivna")
      .map((r) => r.destinacija_id)
  );

  destinacijaOptions.value = (destinacijeData.items || destinacijeData)
    .filter((d) => !zauzeteDestinacije.has(d.id))
    .map((d) => ({
      title: `${d.naziv} - ${d.grad} / slobodna`,
      value: d.id,
    }));
}

function resetForm() {
  for (const key of Object.keys(form)) {
    delete form[key];
  }
}

function openCreate(entityKey) {
  resetForm();

  activeEntity.value = entityKey;
  activeId.value = null;
  editMode.value = false;

  for (const field of configs.value[entityKey].fields) {
    form[field.key] = "";
  }

  if (entityKey === "rezervacije") {
    form.status = "aktivna";
  }

  dialog.value = true;
}

function openEdit(entityKey, item) {
  resetForm();

  activeEntity.value = entityKey;
  activeId.value = item.id;
  editMode.value = true;

  for (const field of configs.value[entityKey].fields) {
    form[field.key] = item[field.key] ?? "";
  }

  if (entityKey === "rezervacije") {
    form.klijent_id = item.klijent_id ?? item.klijent?.id ?? "";
    form.destinacija_id = item.destinacija_id ?? item.destinacija?.id ?? "";
  }

  dialog.value = true;
}

async function saveItem() {
  const entityKey = activeEntity.value;
  const path = configs.value[entityKey].path;

  const body = {};

  for (const field of configs.value[entityKey].fields) {
    body[field.key] = form[field.key];

    if (field.type === "number") {
      body[field.key] = Number(form[field.key]);
    }
  }

  const url = editMode.value
    ? `${API}/${path}/${activeId.value}`
    : `${API}/${path}`;

  const method = editMode.value ? "PUT" : "POST";

  const res = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    snackbar.text = "Greška pri spremanju.";
    snackbar.show = true;
    return;
  }

  dialog.value = false;
  snackbar.text = "Zapis je spremljen.";
  snackbar.show = true;

  await loadEntity(entityKey);
  await loadDashboard();
  await loadSelectOptions();
}

function confirmDelete(entityKey, item) {
  activeEntity.value = entityKey;
  itemForDelete.value = item;
  deleteDialog.value = true;
}

async function deleteItem() {
  const entityKey = activeEntity.value;
  const path = configs.value[entityKey].path;

  const res = await fetch(`${API}/${path}/${itemForDelete.value.id}`, {
    method: "DELETE",
  });

  if (!res.ok) {
    snackbar.text =
      "Greška pri brisanju. Možda je zapis povezan s drugom tablicom.";
    snackbar.show = true;
    deleteDialog.value = false;
    return;
  }

  deleteDialog.value = false;
  snackbar.text = "Zapis je obrisan.";
  snackbar.show = true;

  await loadEntity(entityKey);
  await loadDashboard();
  await loadSelectOptions();
}

async function finishReservation(item) {
  await fetch(`${API}/rezervacije/${item.id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      klijent_id: item.klijent_id,
      destinacija_id: item.destinacija_id,
      datum_rezervacije: item.datum_rezervacije,
      broj_osoba: item.broj_osoba,
      status: "završena",
    }),
  });

  await loadEntity("rezervacije");
  await loadSelectOptions();
  await loadDashboard();
}

watch(currentPage, async (newPage) => {
  if (newPage === "dashboard") {
    await loadDashboard();
  } else if (entityKeys.includes(newPage)) {
    await loadEntity(newPage);
  }
});

onMounted(loadAll);
</script>

<style scoped>
.main-container {
  width: 100%;
  max-width: 1180px;
  padding-top: 28px;
  padding-bottom: 60px;
}

.custom-tabs {
  width: fit-content;
  min-width: 720px;
  background: linear-gradient(135deg, #1565c0, #26a69a);
  border-radius: 18px;
  padding: 10px 14px;
  margin: 0 auto 28px auto;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
}

.custom-tabs :deep(.v-tab) {
  color: white;
  font-weight: 700;
  text-transform: none;
  letter-spacing: 0;
  border-radius: 14px;
  margin-right: 8px;
  min-width: 120px;
}

.custom-tabs :deep(.v-tab--selected) {
  background: rgba(255, 255, 255, 0.18);
}

.content-window {
  max-width: 1180px;
  margin: 0 auto;
  background: #181818;
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 22px;
  padding: 32px;
  box-shadow: 0 18px 45px rgba(0, 0, 0, 0.35);
}

.content-window :deep(h1) {
  font-size: 34px;
  margin-bottom: 26px;
}

.content-window :deep(.v-card),
.content-window :deep(.v-table),
.content-window :deep(.v-field) {
  border-radius: 16px;
}

.content-window :deep(.v-row) {
  row-gap: 18px;
}

@media (max-width: 850px) {
  .custom-tabs {
    width: 100%;
    min-width: 0;
    overflow-x: auto;
  }

  .content-window {
    padding: 22px;
  }
}

.custom-tabs {
  width: fit-content;
  min-width: 720px;
  height: 52px;
  background: linear-gradient(135deg, #1565c0, #26a69a);
  border-radius: 18px;
  padding: 6px 14px;
  margin: 0 auto 28px auto;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.35);
  overflow: visible;
}

.custom-tabs :deep(.v-slide-group__container) {
  overflow: visible;
}

.custom-tabs :deep(.v-slide-group__content) {
  align-items: center;
}

.custom-tabs :deep(.v-tab) {
  height: 40px;
  min-width: 120px;
  color: white;
  font-weight: 700;
  text-transform: none;
  letter-spacing: 0;
  border-radius: 14px;
  margin-right: 8px;
}

.custom-tabs :deep(.v-tab--selected) {
  background: rgba(255, 255, 255, 0.18);
}

.custom-tabs :deep(.v-btn__content) {
  height: 40px;
  line-height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>