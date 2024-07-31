<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <nav class="sticky top-0 left-0 flex gap-8 p-8">
    <RouterLink to="/">Home</RouterLink>
    <RouterLink to="/analisis">Analisis</RouterLink>
  </nav>
  <main class="mt-12 p-8">
    <RouterView />
  </main>
</template>
