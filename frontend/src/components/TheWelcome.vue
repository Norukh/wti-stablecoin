<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
</script>

<template>
  <div class="flex flex-col justify-items-start items-center gap-4">
    <WelcomeItem icon="pi pi-money-bill" heading="Collaterization">
      The Western Texas Intermediate Stablecoin (WTIST) is collaterized by oil assets and backed by the
      USDC stablecoin to ensure stability and security for all users.
    </WelcomeItem>

    <WelcomeItem icon="pi pi-equals" heading="Stabilization">
      We stabilize the Western Texas Intermediate Stablecoin (WTIST) by backing it with oil assets
      and using automated offchain processes that keep the price stable at all times.
    </WelcomeItem>

    <WelcomeItem icon="pi pi-sitemap" heading="Distributed Finance">
      Our coin swap feature allows you to swap your USDC with the Western Texas Intermediate Stablecoin (WTIST) 
      and buy oil assets on the blockchain.
    </WelcomeItem>

    <WelcomeItem icon="pi pi-users" heading="Availability">
      Our goal is to provide a stablecoin that is available to everyone, regardless of their location or financial status.
      Invest in oil assets on-chain to invest in one of the most traded commodities in the world.
    </WelcomeItem>
  </div>
</template>
