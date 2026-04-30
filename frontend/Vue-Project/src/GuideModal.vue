<!--Guide Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <header class="header">
        <div class="modal_title">Plant Guide</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>

      <div class="scroll_content">
        <div class="guide_text">
          <span>1. Power on your probe and connect it to Wi-Fi.</span>
          <span>2. Synchronize your probe with a specific plant.</span>
          <span>3. Insert the probe into the plant, keeping [non-waterproof part] above the soil.</span>
          <span>4. Hang out, have a good time.</span>
        </div>
        <header class="header">
          <div class="modal_title">Connect to WiFi</div>
        </header>
        <div class="guide_text">
          <span>- When the device is in access point mode, connect to it on a phone or computer with the following credentials.</span>
          <span>- SSID: ThirstyPlant-Setup </span>
          <span>- Password: ThirstyPlant123 </span>
          <span>- When connected, open your phone or computer browser and navigate to the following url. </span>
          <span>- http://192.168.4.1 </span>
          <span>- Enter your WiFi credentials into the corresponding text fields, and confirm by pressing submit.</span>
          <span>- The confirmation page will save your WiFi credentials and restart the probe.</span>
        </div>
        <header class="header">
          <div class="modal_title">LED Status Legend</div>
        </header>
        <div class="guide_text">
          <span>- 4 long blinks: device is booting. </span>
          <span>- 3 medium blinks: attempting WiFi connect. </span>
          <span>- 6 fast blinks: WiFi connection failed. </span>
          <span>- 1 blink: probe sending data to web application. </span>
          <span>- 3 fast blinks: probe sending data failed. </span>
          <span>- 2 short blinks, pause, 2 short blinks, pause, 1 long blink: AP mode starting. </span>
          <span>- LED light on (persistent): normal mode </span>
        </div>
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
.scroll_content {
  overflow-y: auto;
  max-height: 60vh;
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