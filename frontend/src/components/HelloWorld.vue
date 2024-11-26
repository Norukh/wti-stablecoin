<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <div class="flex flex-col items-left gap-4">
    <h1>{{ msg }}</h1>
    <h3>
      <b> The world's first Stablecoin for US-American crude oil. </b>
    </h3>

    <h4>Invest in America's most valuable resource and contribute to the future of oil trading.</h4>
  </div>
</template>

<style scoped>
h1 {
  font-weight: 500;
  font-size: 2.6rem;
  position: relative;
  top: -10px;
  color: var(--color-heading);
}

h3 {
  font-size: 1.2rem;
}

</style>
