<!--Guide Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <header class="header">
        <div class="modal_title">Plant Guide</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>

      <div class="guide_text">
        <span>1. Power on your probe and connect it to Wi-Fi.</span>
        <span>2. Synchronize your probe with a specific plant.</span>
        <span>3. Insert the probe into the plant, keeping [non-waterproof part] above the soil.</span>
        <span>4. Hang out, have a good time.</span>
      </div>

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
  align-items: flex-start;
  padding: 1rem;

  padding: 0.5rem 1rem 0.25rem 1rem;
}

.modal_title {
  font-size: 3rem;
  color: #0E2F15;
  cursor: default;

  margin: 0;
  line-height: 1;
}

.close_button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #0E2F15;
  font-weight: bold;
  cursor: pointer;

  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

.guide_text {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0 1rem 1rem 1rem;
  color: #0E2F15;
  cursor: default;
}
</style>