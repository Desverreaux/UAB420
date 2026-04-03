<!--existing_plant Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <h2>Existing Plant</h2>
      <input v-model="search_bar" placeholder="Search for plant"/>
      <textarea>This should say some text about your plant </textarea>
      <button @click="closeModal">X</button>
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

.close_button {
  top: 95%;
  left: 95%;
  border-radius: 25px;
}
</style>