<script setup lang="ts">
import { ref } from 'vue'
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
import Menu from 'primevue/menu'

const items = ref([
  { label: 'Home', icon: 'pi pi-fw pi-home', route: '/' },
  { label: 'Transparency', icon: 'pi pi-fw pi-eye', route: '/transparency' },
  { label: 'About', icon: 'pi pi-fw pi-info-circle', route: '/about' },
  { label: 'Stablecoin DApp', icon: 'pi pi-fw pi-chart-line', route: '/wti' }
])
</script>

<template>
  <header>
    <RouterLink to="/">
      <img alt="WTIST logo" class="logo" src="@/assets/wtist-no-bg.png" width="800" />
      </RouterLink>

    <div class="wrapper">
      <HelloWorld msg="Introducing WTIST" />

      <nav>
        <Menu :model="items" class="w-full">
          <template #item="{ item, props }">
            <router-link v-if="item.route" v-slot="{ href, navigate }" :to="item.route" custom>
              <a v-ripple :href="href" v-bind="props.action" @click="navigate">
                <span :class="item.icon" />
                <span>{{ item.label }}</span>
              </a>
            </router-link>
          </template>
        </Menu>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style>
