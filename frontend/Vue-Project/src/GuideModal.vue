<!--Guide Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <div class="modal_title">Plant Guide</div>
      <span class="guide_text">
        <span>1. Power on your probe and connect it to Wi-Fi.</span>
        <span>2. Synchronize your probe with a specific plant.</span>
        <span>3. Insert the probe into the plant, keeping [non-waterproof part] above the soil.</span>
        <span>4. Hang out, have a good time.</span>
      </span>
      <button class="close_button" @click="$emit('close')">X</button>
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
.modal_title {
  font-size: 3rem;
  color: #0E2F15;
  cursor: default;
}

.guide_text {
  color: #0E2F15;
  cursor: default;
}

.close_button {
  top: 95%;
  left: 95%;
  border-radius: 25px;
}
</style>