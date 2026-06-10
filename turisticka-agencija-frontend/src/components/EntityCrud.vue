<template>
  <div class="entity-crud">
    <div class="entity-header">
      <h1>{{ config.title }}</h1>

      <v-btn color="primary" @click="$emit('open-create', entityKey)">
        Dodaj
      </v-btn>
    </div>

    <div class="filters">
      <v-text-field
        v-model="state.search"
        label="Pretraga"
        clearable
        class="search-field"
        append-inner-icon="mdi-magnify"
        @input="$emit('load-entity', entityKey)"
      />

      <v-select
        v-if="entityKey === 'rezervacije'"
        v-model="state.country"
        label="Država"
        :items="['Sve države', 'Crna Gora', 'Hrvatska', 'Turska', 'Italija', 'Francuska', 'Grčka']"
        class="country-select"
        append-inner-icon="mdi-earth"
        @update:model-value="$emit('load-entity', entityKey)"
      />
    </div>

    <v-table class="entity-table">
      <thead>
        <tr>
          <th v-for="column in config.columns" :key="column.key">
            {{ column.label }}
          </th>
          <th>Akcije</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="item in state.items" :key="item.id">
          <td v-for="column in config.columns" :key="column.key">
            {{ getValue(item, column.key) }}
          </td>

          <td class="actions">
            <v-btn
              size="small"
              color="warning"
              @click="$emit('open-edit', entityKey, item)"
            >
              Uredi
            </v-btn>

            <v-btn
              v-if="entityKey === 'rezervacije'"
              size="small"
              color="success"
              @click="$emit('finish-reservation', item)"
            >
              Završi
            </v-btn>

            <v-btn
              size="small"
              color="error"
              @click="$emit('confirm-delete', entityKey, item)"
            >
              Obriši
            </v-btn>
          </td>
        </tr>

        <tr v-if="!state.items || state.items.length === 0">
          <td :colspan="config.columns.length + 1" class="empty-row">
            Nema podataka za prikaz.
          </td>
        </tr>
      </tbody>
    </v-table>

    <div class="pagination-wrapper">
      <v-pagination
        v-model="state.page"
        :length="state.pages"
        @update:model-value="$emit('load-entity', entityKey)"
      />
    </div>
  </div>
</template>

<script setup>
defineProps({
  entityKey: {
    type: String,
    required: true,
  },
  config: {
    type: Object,
    required: true,
  },
  state: {
    type: Object,
    required: true,
  },
});

defineEmits([
  "open-create",
  "open-edit",
  "confirm-delete",
  "load-entity",
  "finish-reservation",
]);

function getValue(item, path) {
  return path.split(".").reduce((obj, key) => obj?.[key], item) ?? "";
}
</script>

<style scoped>
.entity-crud {
  width: 100%;
}

.entity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 28px;
}

.entity-header h1 {
  margin: 0;
  font-size: 34px;
  color: white;
}

.filters {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 28px;
}

.search-field {
  max-width: 520px;
  width: 100%;
}

.country-select {
  max-width: 280px;
  width: 100%;
}

.entity-table {
  border-radius: 18px;
  overflow: hidden;
}

.entity-table th {
  font-weight: 800;
  color: white;
  white-space: nowrap;
}

.entity-table td {
  vertical-align: middle;
}

.actions {
  display: flex;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.empty-row {
  text-align: center;
  padding: 28px;
  opacity: 0.7;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

@media (max-width: 800px) {
  .entity-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 14px;
  }

  .filters {
    flex-direction: column;
    align-items: stretch;
  }

  .search-field,
  .country-select {
    max-width: 100%;
  }

  .entity-table {
    overflow-x: auto;
    display: block;
  }
}
</style>