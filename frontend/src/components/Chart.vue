<template>
  <LineChartGenerator
      :chart-options="chartOptions"
      :chart-data="chartData"
      :chart-id="chartId"
      :dataset-id-key="datasetIdKey"
      id="graph"
  />
</template>
<script>
import {Line as LineChartGenerator} from 'vue-chartjs'

import {CategoryScale, Chart as ChartJS, Legend, LinearScale, LineElement, PointElement, Title, Tooltip} from 'chart.js'

ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    LinearScale,
    CategoryScale,
    PointElement
)
export default {
  name: 'BarChart',
  components: {LineChartGenerator},
  props: {
    chartId: {
      type: String,
      default: 'bar-chart'
    },
    datasetIdKey: {
      type: String,
      default: 'label'
    },
  },
  data() {
    return {
      chartData: {
        labels: ['January', 'February', 'March',"",""],
        datasets: [{data: [40, 20, 12,1,1,1,1,1,]}]
      },
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      }
    }
  }
}
</script>
<style>
#graph {
  position: relative;
  height: 90%;
  width: 100%;
}

canvas {
  width: 100%;
}
</style>