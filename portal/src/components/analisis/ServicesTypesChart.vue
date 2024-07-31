<script>
import api from '@/helpers/api'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Pie } from 'vue-chartjs'

ChartJS.register(ArcElement, Tooltip, Legend)

export default {
  name: 'InstitutionChart',
  components: {
    Pie
  },
  data() {
    return {
      serviceTypes: [],
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Pedidos por tipo de servicio',
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
    api.get('/analisis/services/types').then(({ data }) => {
      this.services = data.data
      this.chartData = {
        labels: this.services.map((service) => service.service_type),
        datasets: [
          {
            label: 'Pedidos al tipo de servicio',
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
    <Pie :data="chartData" :options="options" />
  </div>
</template>
