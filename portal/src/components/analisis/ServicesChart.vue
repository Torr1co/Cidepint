<script>
import api from '@/helpers/api'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

export default {
  name: 'InstitutionChart',
  components: {
    Bar
  },
  data() {
    return {
      services: [],
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Pedidos por servicio',
            backgroundColor: '#f87979',
            data: []
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: true
      }
    }
  },
  mounted() {
    api.get('/analisis/services/ranking').then(({ data }) => {
      this.services = data.data
      this.chartData = {
        labels: this.services.map((service) => service.name),
        datasets: [
          {
            label: 'Pedidos al servicio',
            backgroundColor: '#f87979',
            data: this.services.map((service) => service.request_count)
          }
        ]
      }
    })
  }
}
</script>

<template>
  <div>
    <h2 class="">Ranking de los servicios mas solicitados</h2>
    <Bar :data="chartData" :options="options" />
  </div>
</template>
