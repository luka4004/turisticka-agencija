<template>
  <v-dialog
    :model-value="modelValue"
    max-width="400"
    @update:model-value="$emit('update:modelValue', $event)"
  >
    <v-card>
      <v-card-title>Potvrda brisanja</v-card-title>

      <v-card-text>
        Jesi li siguran da želiš obrisati ovaj zapis?
      </v-card-text>

      <v-card-actions>
        <v-spacer></v-spacer>

        <v-btn @click="$emit('update:modelValue', false)">
          Odustani
        </v-btn>

        <v-btn color="error" @click="$emit('delete-item')">
          Obriši
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
});

defineEmits(["update:modelValue", "delete-item"]);
</script>