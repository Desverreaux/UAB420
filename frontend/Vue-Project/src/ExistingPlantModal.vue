<!--existing_plant Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">

      <header class="header">
        <span class="modal_title">Existing Plant</span>  
        <button class="close_button" @click="$emit('close')">X</button>
      </header>
      
      <div class="main">
        <span class="plant_status">This should say something about the overall status of your plant</span>

        <div class="plant_graph">
          <canvas ref="plant_chart"></canvas>
          

        </div>

      </div>
      
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"
import { Chart, registerables } from "chart.js"

Chart.register(...registerables)

export default {
    props: ["show"],
    emits: ["close"],
    components: { Modal },

    data() {
      return {
        chart: null,
        loading: false // Loads stuff in real-time once we have backend fetching
      }
    },

    methods: {
      async render_chart() {
        const context = this.$refs.plant_chart.getContext("2d")

        let data_points
        let labels

        try {
          // RESERVED FOR ONCE BACKEND FETCHING IS LIVE

          
          this.loading = true

          const response = await fetch(`/api/getHistoricalData?plantIdentifier=plant1`)
          const result = await response.json() 
          //Should be formatted as:
          // data: [1, 2, 3, 4, 5]
          // labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

          data_points = result.data
          labels = result.labels

          this.loading = false
          

          // Test data that can be deleted later
          

          if (this.chart) {
            this.chart.destroy()
          }

          this.chart = new Chart(context, {
            type: "line",
            data: {
              labels, 
              datasets: [{
                label: "Moisture %",
                data: data_points,
                borderColor: "#0E2F15",
                backgroundColor: "rgba(14, 47, 21, 0.2)",
                tension: 0.3, 
                fill: true
              }]
            },
            
            options: {
              responsive: true, 
              maintainAspectRatio: false
            }

          })
          
        } catch (err) {
          console.error("Failed to load chart data: ", err)
        }
      }
    },

    watch: {
      show(val) {
        if (val) {
          this.$nextTick(() => {
            this.render_chart()
          })
        }
      }
    }
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
  width: 65%;
  height: 20vh;
  resize: none;
}

.plant_graph {
  width: 75%;
  height: 250px;

  padding: 1rem;

  border-radius: 12px;
  border: 2px solid #0E2F15;

  overflow: hidden;
}

.plant_graph canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}

</style>