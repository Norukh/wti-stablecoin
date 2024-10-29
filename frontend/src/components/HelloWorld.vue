<script setup lang="ts">
defineProps<{
  msg: string
}>()
</script>

<template>
  <div class="greetings">
    <h1>{{ msg }}</h1>
    <h3>
      The world's first Stablecoin of crude oil!
      <ul>
        <li><a href="https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.html" target="_blank" rel="noopener">WTI information</a></li>
        <li><a href="https://www.investing.com/commodities/crude-oil" target="_blank" rel="noopener">WTI Stats</a></li>
      </ul>
    </h3>
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

.greetings h1,
.greetings h3 {
  text-align: center;
}

@media (min-width: 1024px) {
  .greetings h1,
  .greetings h3 {
    text-align: left;
  }
}
</style>
