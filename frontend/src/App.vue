<!--suppress ALL -->
<template>
  <div class="main-container">
    <div class="info-container">
      <div class="row">
        <div class="output tile ">
          <h1>Output</h1>
          <div class="scrollable">
            <p v-for="message in this.data.outputMessages"> {{ message }} </p>
          </div>
        </div>
        <div class="tile-view">
          <div class="row">
            <div class="square tile">
              <h1>Goals</h1>
              <h2 class="centered-text attacker">{{ this.attacker.expectedGoals }}</h2>
              <h2 class="centered-text defender">{{ this.defender.expectedGoals }}</h2>
            </div>
            <div class="square tile">
              <h1>Event time</h1>
              <div class="centered">
                <h1 class="centered-text large">{{this.data.eventMinute}}:{{this.data.eventSeconds}}</h1>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="square tile">
              <h1></h1>
            </div>
            <div class="square tile">
              <h1>Event type</h1>
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
          <Chart/>
        </div>
        <div class="predicted-score tile">
          <h1>Prediction</h1>
          <h3>Attacker:</h3>
          <info-table :team="this.attacker"></info-table>
          <hr>
          <h3>Defender:</h3>
          <info-table :team="this.defender"></info-table>
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
        defenderGoals: 2,
        predictedChartValues: [],
        actualChartValues: [],
        outputMessages: [],
        attackerWinRate: 0.5,
        eventType: "Kick",
        eventMinute: 20,
        eventSeconds: 20,

      },
      attacker: {
        expectedGoals: 1,
        actualGoals: 1,
        averageGoals: 2,
      },
      defender: {
        expectedGoals: 1,
        actualGoals: 1,
        averageGoals: 2,
      }
    }
  },
  mounted() {

  },
  methods: {
    async fetchNewValues() {
      let newValues = Api().get("/api");
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
