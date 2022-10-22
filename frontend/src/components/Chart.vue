<template>
  <LineChartGenerator
      :chart-options="chartOptions"
      :chart-data="chartData"
      chart-id="line-chart"
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
  props: ['datasetIdKey'],
  data() {
    return {
      chartOptions: {
        responsive: true,
        maintainAspectRatio: false
      },
      chartData: this.chartData,

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