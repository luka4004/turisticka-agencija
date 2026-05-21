<template>
  <v-dialog
    :model-value="modelValue"
    max-width="600"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card>
      <v-card-title>
        {{ editMode ? "Uredi zapis" : "Dodaj zapis" }}
      </v-card-title>

      <v-card-text>
        <template v-if="config">
          <div v-for="field in config.fields" :key="field.key">
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

        <v-btn @click="$emit('update:modelValue', false)">
          Odustani
        </v-btn>

        <v-btn color="primary" @click="$emit('save-item')">
          Spremi
        </v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
  editMode: {
    type: Boolean,
    required: true,
  },
  config: {
    type: Object,
    default: null,
  },
  form: {
    type: Object,
    required: true,
  },
});

defineEmits(["update:modelValue", "save-item"]);
</script>