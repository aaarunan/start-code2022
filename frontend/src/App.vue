<template>
  <div class="main-container">
    <div class="info-container">
      <div class="row">
        <div class="output tile ">
          <h1>Live Feed</h1>
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
                <h1 class="centered-text large"> {{ this.data.eventMinute }}:00</h1>
              </div>
            </div>
          </div>
          <div class="row">
            <div class="square tile" id="reset-button" @click="reload">
              <h1>RESET</h1>
            </div>
            <div class="square tile">
              <h1>Events</h1>
              <div class="centered">
                <v-lazy-image v-for="event in this.data.events" :src=this.getImageURL(event) :alt="event.eventType"
                              :key="event" style="width: 80px"/>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row">
        <div class="graph tile">
          <h1>Graph</h1>
          <Chart :chart-data="this.chartData" :dataset-id-key="this.datasetIdKey"/>
        </div>
        <div class="predicted-score tile scrollbar" style="overflow-y: auto">
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
      <div class="inner-bar" :style="{height: (1 - this.data.winrate_ratio) * 100 + '%'}"></div>
    </div>
    <div class="actual-bar" :style="{height: (1 - this.data.winrate_actual) * 100 +'%'}"/>
  </div>
</template>
<script>
import Chart from '@/components/Chart'
import Api from "../service/api";
import InfoTable from "@/components/infoTable";
import VLazyImage from 'v-lazy-image';

export default {
  name: 'App',
  components: {
    InfoTable,
    Chart,
    VLazyImage
  },
  data() {
    return {
      finish: false,
      data: {
        defenderGoals: null,
        predictedChartValues: [],
        actualChartValues: [],
        outputMessages: [],
        winrate_ratio: 0.5,
        winrate_actual: 0.5,
        events: [],
        eventMinute: '00',
        eventSeconds: '00',

      },
      home_team: {
        predicted_goals: null,
        actual_goals: null,
        current_goals: null,
        name: null,
        abbr: null,
      },
      away_team: {
        predicted_goals: null,
        actual_goals: null,
        current_goals: null,
        name: null,
        abbr: null,
      },
      datasetIdKey: {
        type: String,
        default: 'label'
      },
      chartData: {
        labels: [],
        datasets: [
          {
            label: 'Predicted ratio',
            borderColor: '#00c0ef',
            data: []
          },
          {
            label: 'Actual ratio',
            borderColor: '#ef2a00',
            data: []
          },
        ]
      },
    }
  },
  mounted() {
    Api().get("/reset")
    setInterval(() => this.fetchNewValues(), 500)
  },
  methods: {
    fetchNewValues() {
      Api().get("/next-minute").then(({data}) => this.updateData(data)).catch((e) => {
        if (e instanceof TypeError) {
          console.log("done")
        } else throw e;
      });
    },
    getImageURL(event) {
      return require(`@/static/icons/${event.event}.png`)
    },
    updateChartData(data) {
      this.chartData.labels.push(data.minutes)
      this.chartData.datasets[1].data.push(this.data.winrate_actual)
      this.chartData.datasets[0].data.push(this.data.winrate_ratio)
    },
    updateData(data) {
      if (data === null) {
        throw TypeError("No more data")
      }
      this.home_team = data.home_team;
      this.away_team = data.away_team;
      console.log(data.home_team.predicted_goals)
      this.data.winrate_actual = data.home_team.actual_goals / (data.home_team.actual_goals + data.away_team.actual_goals)
      this.data.winrate_ratio = data.home_team.predicted_goals / (data.home_team.predicted_goals + data.away_team.predicted_goals)
      if (isNaN(this.data.winrate_ratio)) {
        this.data.winrate_ratio = 0.5;
      }
      if (isNaN(this.data.winrate_actual)) {
        this.data.winrate_actual = 0.5
      }
      this.data.events = data.events
      for (const message of this.getActionWord(data)) {
        if (message !== ""){
          this.data.outputMessages.unshift(message)
        }
      }
      this.data.eventMinute = String(data.minutes).padStart(2, "0")
      this.updateChartData(data)
    },
    getActionWord: function*(data) {
      for(let i = 0; i < data.events.length; i++){
        let event = data.events[i]
        switch (event.event) {
          case "FREE KICK":
            yield this.getEventLine(event, "got a free kick")
            break

          case "FREE-THROW":
            yield this.getEventLine(event, "got a free throw.")
            break

          case "PENALTY AWARDED":
            yield this.getEventLine(event, "was awarded a penalty!")
            break

          case "SHOT OF TARGET":
            yield this.getEventLine(event, "shot off target...")
            break

          case "GOAL":
            yield this.getEventLine(event, "scored!!! The score is now " + this.getScore(data))
            break

          case "RED CARD":
            yield this.getEventLine(event, "got a red card and had to sub!")
            break

          default:
            yield "";
            break
        }
      }
    },
    getEventLine(event, text) {
      return String(event.minutes).padStart(2, '0') + ":" + String(event.seconds).padStart(2, '0') + "    " + ((event.perpetrator === "home") ? this.home_team.name : this.away_team.name) + " " + text;
    },
    getScore(data) {
      return data.home_team.current_goals + " : " + data.away_team.current_goals;
    },
    reload() {
      window.location.reload();
    }
  }
}
</script>
<style>
@import '@/static/css/main.css';

#reset-button {
  justify-content: center;
  text-align: center;
  align-items: center;
  display: flex;
  font-size: 32px;
}

#reset-button:hover {
  background-color: tomato;
  cursor: pointer;
  border: 2px #2c3e50 solid;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  margin: 0;
}
</style>
