<template>
  <table>
    <tr>
      <th>Expected goals</th>
      <th>Actual goals</th>
    </tr>
    <tr>
      <td>{{this.team.predicted_goals}}</td>
      <td>{{this.team.actual_goals}}</td>
    </tr>
  </table>
</template>

<script>
export default {
  name: "infoTable",
  props: ['team']
}
</script>

<style scoped>
  table {
    margin: auto;
  }
  th, td {
    padding: 7px 20px;
    width: max-content;
  }
</style>