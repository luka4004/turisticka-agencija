<template>
  <div>
    <div class="d-flex justify-space-between align-center mb-4">
      <h1>{{ config.title }}</h1>

      <v-btn color="primary" @click="$emit('open-create', entityKey)">
        Dodaj
      </v-btn>
    </div>

    <v-text-field
      v-model="state.search"
      label="Pretraga"
      clearable
      class="mb-4"
      @input="$emit('load-entity', entityKey)"
    ></v-text-field>

    <v-table>
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

          <td>
            <v-btn
              size="small"
              color="warning"
              class="mr-2"
              @click="$emit('open-edit', entityKey, item)"
            >
              Uredi
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
      </tbody>
    </v-table>

    <div class="d-flex justify-center mt-4">
      <v-pagination
        v-model="state.page"
        :length="state.pages"
        @update:model-value="$emit('load-entity', entityKey)"
      ></v-pagination>
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
]);

function getValue(item, path) {
  return path.split(".").reduce((obj, key) => obj?.[key], item) ?? "";
}
</script>