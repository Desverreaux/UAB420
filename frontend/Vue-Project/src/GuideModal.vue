<!--Guide Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <div class="modal_title">Plant Guide</div>
      <span>
        1. Power on your probe and connect it to Wi-Fi.
        2. Synchronize your probe with a specific plant.
        3. Insert the probe into the plant, keeping [   ] above the soil.
        4. Hang out, have a good time.
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