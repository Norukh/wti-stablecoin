<script setup lang="ts">
import Button from 'primevue/button'
</script>

<template>
  <div class="flex flex-col justify-center">
    <h1 class="text-4xl">Stay in the loop</h1>
    <p class="text-lg mt-5">
      The Western Texas Intermediate Stablecoin (WTIST) is a stablecoin that represents the oil
      price of "West Texas Intermediate". For general information on the WTI, visit:
    </p>

    <div class="flex mt-5 gap-4">
      <Button
        as="a"
        label="WTI Information"
        href="https://www.cmegroup.com/markets/energy/crude-oil/light-sweet-crude.html"
        target="_blank"
        rel="noopener"
      />

      <Button
        as="a"
        label="WTI Stats"
        href="https://www.investing.com/commodities/crude-oil"
        target="_blank"
        rel="noopener"
      />

    </div>
  </div>
</template>
