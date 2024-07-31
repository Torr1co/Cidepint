<script>
import api from '@/helpers/api'
import {
  Chart,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

Chart.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend)

export default {
  name: 'InstitutionChart',
  components: {
    Line
  },
  data() {
    return {
      institutions: [],
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Tiempo de resolucion',
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
    api.get('/analisis/institutions/ranking').then(({ data }) => {
      this.institutions = data.data
      this.chartData = {
        labels: this.institutions.map((institution) => institution.name),
        datasets: [
          {
            label: 'Tiempo de resolucion',
            backgroundColor: '#f87979',
            data: this.institutions.map((institution) => institution.time_resolution)
          }
        ]
      }
    })
  }
}
</script>

<template>
  <div>
    <h2 class="">Ranking de las 10 instituciones con mejor tiempo de resolucion</h2>
    <Line :data="chartData" :options="options" />
  </div>
</template>
