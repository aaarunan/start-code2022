<template>
  <div class="main-container">
    <div class="info-container">
      <div class="row">
        <div class="output tile ">
          <h1>Output</h1>
          <div class="scrollable">
            <p v-for="message in this.data.outputMessages" :key="message"> {{ message }} </p>
          </div>
        </div>
        <div class="tile-view">
          <div class="row">
            <div class="square tile">
              <h1>Goals</h1>
              <h2 class="centered-text attacker">{{ this.home_team.expected_goals }}</h2>
              <h2 class="centered-text defender">{{ this.away_team.expected_goals }}</h2>
            </div>
            <div class="square tile">
              <h1>Event time</h1>
              <div class="centered">
                <h1 class="centered-text large">At {{this.data.eventMinute}} m</h1>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="square tile">
              <h1></h1>
            </div>
            <div class="square tile">
              <h1>Events</h1>
              <div class="centered">
                <h2 class="centered-text">{{ this.data.eventType }}</h2>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="graph tile">
          <h1>Graph</h1>
          <Chart :chart-data="this.chartData" :dataset-id-key="this.datasetIdKey" />
        </div>
        <div class="predicted-score tile">
          <h1>Prediction</h1>
          <h3>Attacker:</h3>
          <info-table :team="this.home_team"></info-table>
          <hr>
          <h3>Defender:</h3>
          <info-table :team="this.away_team"></info-table>
        </div>
      </div>
    </div>
    <div class="probability-bar tile">
      <div class="inner-bar" :style="{height: this.data.attackerWinRate * 100 + '%'}"></div>
    </div>

  </div>
</template>
<script>
import Chart from '@/components/Chart'
import Api from "../service/api";
import InfoTable from "@/components/infoTable";

export default {
  name: 'App',
  components: {
    InfoTable,
    Chart
  },
  data() {
    return {
      data: {
        defenderGoals: null,
        predictedChartValues: [],
        actualChartValues: [],
        outputMessages: [],
        attackerWinRate: 0.5,
        eventType: "",
        eventMinute: '00',
        eventSeconds: '00',

      },
      home_team: {
        expected_goals: null,
        actual_goals: null,
        average_goals: null,
      },
      away_team: {
        expected_goals: null,
        actual_goals: null,
        average_goals: null,
      },
      datasetIdKey: {
        type: String,
        default: 'label'
      },
      chartData: {
        labels: [],
        datasets: [{data: []}]
      },
    }
  },
  mounted() {
    setInterval(() => this.fetchNewValues(), 1000)
  },
  methods: {
    async fetchNewValues() {
      // eslint-disable-next-line
      Api().get("/next-minute").then(({data}) => {
        this.home_team = data.home_team;
        this.away_team = data.away_team;
        this.data.outputMessages.push(data)
        this.chartData.labels.push(data.minutes)
        //this.chartData.datasets.data.push(data.expected_goals)
        this.data.eventMinute = data.minutes
      }).catch(() => Api().get('/reset'));
    }
  }
}
</script>
<style>
@import '@/static/css/main.css';

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
}
</style>
