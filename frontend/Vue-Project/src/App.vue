<template>
  <div>
    <p>{{ message }} this should display regardless, right?</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const message = ref('')

onMounted(async () => {
  const res = await fetch('http://uab420.desverreaux.com:8000/api/hello')
  const data = await res.json()
  message.value = data.message
})
</script>
