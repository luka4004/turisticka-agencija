<template>
  <v-app>
    <AppHeader />

    <v-main>
      <v-container>
        <v-tabs v-model="tab" class="mb-6">
          <v-tab value="dashboard">Dashboard</v-tab>
          <v-tab value="destinacije">Destinacije</v-tab>
          <v-tab value="klijenti">Klijenti</v-tab>
          <v-tab value="zaposlenici">Zaposlenici</v-tab>
          <v-tab value="rezervacije">Rezervacije</v-tab>
        </v-tabs>

        <v-window v-model="tab">
          <v-window-item value="dashboard">
            <DashboardCards :cards="dashboardCards" />
          </v-window-item>

          <v-window-item
            v-for="entityKey in entityKeys"
            :key="entityKey"
            :value="entityKey"
          >
            <EntityCrud
              :entity-key="entityKey"
              :config="configs[entityKey]"
              :state="state[entityKey]"
              @open-create="openCreate"
              @open-edit="openEdit"
              @confirm-delete="confirmDelete"
              @load-entity="loadEntity"
            />
          </v-window-item>
        </v-window>
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

import AppHeader from "./components/AppHeader.vue";
import DashboardCards from "./components/DashboardCards.vue";
import EntityCrud from "./components/EntityCrud.vue";
import EntityFormDialog from "./components/EntityFormDialog.vue";
import DeleteConfirmDialog from "./components/DeleteConfirmDialog.vue";

const API = "http://127.0.0.1:5000/api";

const tab = ref("dashboard");
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
        label: "Destinacija",
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

  const url = `${API}/${path}?search=${encodeURIComponent(
    currentState.search || ""
  )}&page=${currentState.page}&per_page=${currentState.perPage}`;

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

  destinacijaOptions.value = (destinacijeData.items || destinacijeData).map((d) => ({
    title: `${d.naziv} - ${d.grad}`,
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

watch(tab, async (newTab) => {
  if (newTab === "dashboard") {
    await loadDashboard();
  } else if (entityKeys.includes(newTab)) {
    await loadEntity(newTab);
  }
});

onMounted(loadAll);
</script>
