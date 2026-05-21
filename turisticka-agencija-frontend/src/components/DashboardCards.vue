<template>
  <div>
    <h1 class="mb-4">Dashboard</h1>

    <v-row>
      <v-col
        cols="12"
        md="4"
        v-for="card in cards"
        :key="card.title"
      >
        <v-card>
          <v-card-title>{{ card.title }}</v-card-title>
          <v-card-text class="text-h4">
            {{ card.value }}
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
</script>