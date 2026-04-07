<!--Critical Error Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <header class="header">
        <div class="modal_title">Critical Error</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>

      <div class = "error_explanation">
        <span>The program encountered a critical error; please restart the application.</span>
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
  align-items: center;
  padding: 1rem;
}

.modal_title {
  font-size: 3rem;
  color: #FF0000;
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