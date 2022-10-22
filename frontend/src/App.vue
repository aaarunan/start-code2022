<template>
  <div class="main-container">
    <div class="info-container">
      <div class="row">
        <div class="output tile ">
          <h1>Output</h1>
          <div class="scrollable scrollbar">
            <p v-for="message in this.data.outputMessages" :key="message"> {{ message }} </p>
          </div>
        </div>
        <div class="tile-view">
          <div class="row">
            <div class="square tile">
              <h1>Goals</h1>
              <h2 class="centered-text attacker">{{ this.home_team.current_goals }}</h2>
              <h2 class="centered-text defender">{{ this.away_team.current_goals }}</h2>
            </div>
            <div class="square tile">
              <h1>Event time</h1>
              <div class="centered">
                <h1 class="centered-text large"> {{this.data.eventMinute}}:00</h1>
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
                <v-lazy-image v-for="event in this.data.events" :src=this.getImageURL(event) :alt="event.eventType" :key="event" style="width: 40px" />
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
      <div class="inner-bar" :style="{height: this.data.winrate_ratio * 100 + '%'}"></div>
    </div>

  </div>
</template>
<script>
import Chart from '@/components/Chart'
import Api from "../service/api";
import InfoTable from "@/components/infoTable";
import VLazyImage from 'v-lazy-image'

export default {
  name: 'App',
  components: {
    InfoTable,
    Chart,
    VLazyImage
  },
  data() {
    return {
      data: {
        defenderGoals: null,
        predictedChartValues: [],
        actualChartValues: [],
        outputMessages: [],
        winrate_ratio: 0.5,
        events: [],
        eventMinute: '00',
        eventSeconds: '00',

      },
      home_team: {
        predicted_goals: null,
        actual_goals: null,
        current_goals: null,
      },
      away_team: {
        predicted_goals: null,
        actual_goals: null,
        current_goals: null,
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
    setInterval(() => this.fetchNewValues(), 500)
  },
  methods: {
    fetchNewValues() {
      // eslint-disable-next-line
      Api().get("/next-minute").then(({data}) => {
        this.home_team = data.home_team;
        this.away_team = data.away_team;
        console.log(data.home_team.predicted_goals)
        this.data.winrate_ratio= data.away_team.predicted_goals / (data.home_team.predicted_goals + data.away_team.predicted_goals)
        console.log(this.data.winrate_ratio)
        if (isNaN(this.data.winrate_ratio)) {
          this.data.winrate_ratio = 0.5;
        }
        this.data.events = data.events
        this.data.outputMessages.push(data)
        this.chartData.labels.push(data.minutes)
        this.data.eventMinute = data.minutes
        this.chartData.datasets[0].data.push(this.data.winrate_ratio)
      }).catch(() => {
        console.error("moren din er feil")
        Api().get('/reset')
      });
    },
    getImageURL(event) {
      return require(`@/static/icons/${event.event}.png`)
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
