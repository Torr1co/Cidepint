<script setup>
import InstitutionsChart from '../components/analisis/InstitutionsChart.vue'
import ServicesChart from '../components/analisis/ServicesChart.vue'
import ServicesTypesChart from '../components/analisis/ServicesTypesChart.vue'
</script>

<template>
  <section class="flex gap-16 flex-col">
    <InstitutionsChart />
    <ServicesChart />
    <ServicesTypesChart />
  </section>
</template>
