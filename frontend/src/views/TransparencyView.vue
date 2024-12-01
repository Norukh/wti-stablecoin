<script setup lang="ts">
import Panel from 'primevue/panel'
import Avatar from 'primevue/avatar'
</script>

<template>
  <div class="flex flex-col justify-center">
    <h1 class="text-4xl">Transparency & Stability</h1>
    <p class="text-lg mt-5">
      The WTIST stablecoin is a transparent and stable digital currency that is backed by real-world
      oil reserves.
    </p>

    <div class="card mt-4">
      <Panel toggleable>
        <template #header>
          <div class="flex items-center gap-2">
            <Avatar
              icon="pi pi-key"
              shape="circle"
              size="small"
              style="
                background-color: var(--p-success-color);
                color: var(--p-success-contrast-color);
              "
            />
            <span class="font-bold">Oil Reserves Composition</span>
          </div>
        </template>

        <p class="m-0">
          The WTIST stablecoin is backed by oil reserves. The Western Texas Intermediate oil
          reserves are stored in secure locations around the world and are audited regularly to
          ensure that the reserves are sufficient to back the WTIST stablecoin.
        </p>
      </Panel>
    </div>

    <div class="card mt-4">
      <Panel toggleable>
        <template #header>
          <div class="flex items-center gap-2">
            <Avatar
              icon="pi pi-share-alt"
              shape="circle"
              size="small"
              style="
                background-color: var(--p-success-color);
                color: var(--p-success-contrast-color);
              "
            />
            <span class="font-bold">Blockchain Transparency</span>
          </div>
        </template>

        <p class="m-0">
          The WTI Stablecoin DApp is built on the Ethereum blockchain, which is a public and
          transparent blockchain.
        </p>
      </Panel>
    </div>
  </div>
</template>
