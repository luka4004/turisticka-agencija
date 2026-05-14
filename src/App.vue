<template>
  <v-app>
    <v-app-bar color="primary" title="Turistička agencija"></v-app-bar>

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
          <!-- DASHBOARD -->
          <v-window-item value="dashboard">
            <h1 class="mb-4">Dashboard</h1>

            <v-row>
              <v-col cols="12" md="4" v-for="card in dashboardCards" :key="card.title">
                <v-card>
                  <v-card-title>{{ card.title }}</v-card-title>
                  <v-card-text class="text-h4">{{ card.value }}</v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-window-item>

          <!-- GENERIČKI CRUD -->
          <v-window-item
            v-for="entityKey in entityKeys"
            :key="entityKey"
            :value="entityKey"
          >
            <div class="d-flex justify-space-between align-center mb-4">
              <h1>{{ configs[entityKey].title }}</h1>
              <v-btn color="primary" @click="openCreate(entityKey)">Dodaj</v-btn>
            </div>

            <v-text-field
              v-model="state[entityKey].search"
              label="Pretraga"
              clearable
              @input="loadEntity(entityKey)"
              class="mb-4"
            ></v-text-field>

            <v-table>
              <thead>
                <tr>
                  <th v-for="column in configs[entityKey].columns" :key="column.key">
                    {{ column.label }}
                  </th>
                  <th>Akcije</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="item in state[entityKey].items" :key="item.id">
                  <td v-for="column in configs[entityKey].columns" :key="column.key">
                    {{ getValue(item, column.key) }}
                  </td>
                  <td>
                    <v-btn size="small" color="warning" class="mr-2" @click="openEdit(entityKey, item)">
                      Uredi
                    </v-btn>
                    <v-btn size="small" color="error" @click="confirmDelete(entityKey, item)">
                      Obriši
                    </v-btn>
                  </td>
                </tr>
              </tbody>
            </v-table>

            <div class="d-flex justify-center mt-4">
              <v-pagination
                v-model="state[entityKey].page"
                :length="state[entityKey].pages"
                @update:model-value="loadEntity(entityKey)"
              ></v-pagination>
            </div>
          </v-window-item>
        </v-window>
      </v-container>

      <!-- DIALOG ZA DODAVANJE/UREĐIVANJE -->
      <v-dialog v-model="dialog" max-width="600">
        <v-card>
          <v-card-title>
            {{ editMode ? "Uredi zapis" : "Dodaj zapis" }}
          </v-card-title>

          <v-card-text>
            <template v-if="activeEntity">
              <div v-for="field in configs[activeEntity].fields" :key="field.key">
                <v-textarea
                  v-if="field.type === 'textarea'"
                  v-model="form[field.key]"
                  :label="field.label"
                ></v-textarea>

                <v-select
                  v-else-if="field.type === 'select'"
                  v-model="form[field.key]"
                  :label="field.label"
                  :items="field.items"
                  item-title="title"
                  item-value="value"
                ></v-select>

                <v-text-field
                  v-else
                  v-model="form[field.key]"
                  :label="field.label"
                  :type="field.type || 'text'"
                ></v-text-field>
              </div>
            </template>
          </v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="dialog = false">Odustani</v-btn>
            <v-btn color="primary" @click="saveItem">Spremi</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- DIALOG ZA BRISANJE -->
      <v-dialog v-model="deleteDialog" max-width="400">
        <v-card>
          <v-card-title>Potvrda brisanja</v-card-title>
          <v-card-text>Jesi li siguran da želiš obrisati ovaj zapis?</v-card-text>

          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn @click="deleteDialog = false">Odustani</v-btn>
            <v-btn color="error" @click="deleteItem">Obriši</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-snackbar v-model="snackbar.show" :timeout="2500">
        {{ snackbar.text }}
      </v-snackbar>
    </v-main>
  </v-app>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from "vue";

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

const entityKeys = ["destinacije", "klijenti", "zaposlenici", "rezervacije"];

const dashboardCards = computed(() => [
  { title: "Broj destinacija", value: dashboard.broj_destinacija },
  { title: "Broj klijenata", value: dashboard.broj_klijenata },
  { title: "Broj rezervacija", value: dashboard.broj_rezervacija },
  { title: "Broj zaposlenika", value: dashboard.broj_zaposlenika },
  { title: "Aktivne rezervacije", value: dashboard.aktivne_rezervacije },
  { title: "Prosječna cijena", value: dashboard.prosjecna_cijena },
]);

function getValue(item, path) {
  return path.split(".").reduce((obj, key) => obj?.[key], item) ?? "";
}

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
    snackbar.text = "Greška pri brisanju. Možda je zapis povezan s drugom tablicom.";
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