<script setup lang="ts">
import Fieldset from 'primevue/fieldset';
import Avatar from 'primevue/avatar';

defineProps({
  icon: String,
  heading: String,
});
</script>

<template>
  <div class="card">
      <Fieldset>
          <template #legend>
              <div class="flex items-center">
                  <Avatar :icon="icon" shape="circle" size="small" />
                  <span class="font-bold p-2">{{ heading }}</span>
              </div>
          </template>
          <p class="m-0">
              <slot />
          </p>
      </Fieldset>
  </div>
</template>