<!--existing_plant Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">

      <header class="header">
        <span class="modal_title" modal_title>Existing Plant</span>  
        <button class="close_button" @click="$emit('close')">X</button>
      </header>
      
      <div class="main">
        <textarea class="plant_status">This should say something about the overall status of your plant</textarea>
        <textarea class="plant_graph">This should also eventually be a graph</textarea>
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

.main{
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  padding: 0 1rem 1rem 1rem;
  color: #0E2F15;
  cursor: default;
}

.plant_status {
  resize: none;
}

.plant_graph {
  resize: none;
}


</style>