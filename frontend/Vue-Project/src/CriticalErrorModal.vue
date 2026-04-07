<!--Critical Error Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <header class="header">
        <div class="modal_title">Critical Error</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>

      <div class = "error_explanation">
        <span>
            The program encountered a critical error; please restart the application.
        </span>

        <pre v-if="error" class="error_box"> {{ error }}</pre>
      </div>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    props:  {
        show: Boolean,
        error: String
    },
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

.error_explanation {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  padding: 0 1rem 1rem 1rem;
  color: #0E2F15;
  cursor: default;
}

.error_box {
    background-color: #f8d7da;
    color: #721c24;
    padding: 0.75rem;
    border-radius: 8px;
    font-family: monospace;
    white-space: pre-wrap;
    word-break: break-word;
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