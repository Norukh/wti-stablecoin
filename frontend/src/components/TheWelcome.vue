<script setup lang="ts">
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import ToolingIcon from './icons/IconTooling.vue'
import EcosystemIcon from './icons/IconEcosystem.vue'
import CommunityIcon from './icons/IconCommunity.vue'
import SupportIcon from './icons/IconSupport.vue'
</script>

<template>
  <div class="flex flex-col justify-items-start items-center gap-4">
    <WelcomeItem icon="pi pi-book" heading="Documentation">
      Vue’s
      <a href="https://vuejs.org/" target="_blank" rel="noopener">official documentation</a>
      provides you with all information you need to get started.
    </WelcomeItem>

    <WelcomeItem icon="pi pi-cog" heading="Tooling">
      The Vue CLI is a globally installed npm package and provides the vue command in your terminal.
    </WelcomeItem>

    <WelcomeItem icon="pi pi-sitemap" heading="Ecosystem">
      The Vue ecosystem is constantly growing and evolving. Check out the official
      <a href="https://vuejs.org/v3/guide/ecosystem.html" target="_blank" rel="noopener"
        >Vue ecosystem guide</a
      >
      to find tools and libraries to help you build your next project.
    </WelcomeItem>
  </div>
</template>
