<!--existing_plant Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">

      <header class="header">
        <span class="modal_title">{{ plant ? plant.name : "Existing Plant" }}</span>  
        <button class="close_button" @click="$emit('close')">X</button>
      </header>
      
      <div class="main">
        <span class="plant_status"> {{ plantStatusMessage }} </span>

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
        if (!this.plant) return

        const context = this.$refs.plant_chart.getContext("2d")

        let data_points = []
        let labels = []

        try {
          if (this.plant.isProbe) {
          const response = await fetch(`/api/getHistoricalData?plantIdentifier=${this.plant.id}`)
          const result = await response.json()

          data_points = result.data
          labels = result.labels

          const latestMoisture = data_points[data_points.length - 1]

          if (latestMoisture > 60) {
            this.plantStatusMessage = "Your probe-connected plant is doing well. Moisture levels are healthy."
          } else if (latestMoisture > 30) {
            this.plantStatusMessage = "Your probe-connected plant may need water soon."
          } else {
            this.plantStatusMessage = "Your probe-connected plant needs water soon. Moisture levels are low."
          }

        } else {
          data_points = this.plant.graphData
          labels = this.plant.graphLabels

          this.plantStatusMessage = "This is a demo plant. Its graph uses randomly generated smooth fake data."
        }
          
        this.loading = false
         
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
              maintainAspectRatio: false,

              layout: {
                padding: o
              },

              scales: {
                y: {
                  min: 0,
                  max: 100
                }
              }
            }
          })
          
        } catch (err) {
          console.error("Failed to load chart data: ", err)
          this.plantStatusMessage = "Failed to load graph data."
          this.loading = false
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

  padding: 0..25rem 1rem 0.25rem 1rem;
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
  gap: 0.5rem;
  padding: 0.25rem 1rem 0.75rem 1rem;
  color: #0E2F15;
  cursor: default;
  box-sizing: border-box;
}

.plant_status {
  width: 75%;
  height: 50px;

  padding: 0.75rem;
  box-sizing: border-box;

  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  
  overflow-y: auto;
}

.plant_graph {
  width: 75%;
  height: 250px;

  padding: 0.75rem;

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