<!--Guide Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <header class="header">
        <div class="modal_title">Plant Guide</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>

      <body class = "guide_text">
        <span>1. Power on your probe and connect it to Wi-Fi.</span>
        <span>2. Synchronize your probe with a specific plant.</span>
        <span>3. Insert the probe into the plant, keeping [non-waterproof part] above the soil.</span>
        <span>4. Hang out, have a good time.</span>
      </body>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    props: ["show"],
    emits: ["close"],
    components: { Modal }
}
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  padding: 1rem;
}

.modal_title {
  font-size: 3rem;
  color: #0E2F15;
  cursor: default;
}

.guide_text {
  display: flex;
  flex-direction: column;
  gap: 0.75 rem;
  padding: 0 1rem 1rem 1rem;
  color: #0E2F15;
  cursor: default;
}

.close_button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #0E2F15;
  font-weight: bold;
  cursor: pointer;
}
</style>