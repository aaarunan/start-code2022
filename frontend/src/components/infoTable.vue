<template>
  <table>
    <tr>
      <th>Expected goals</th>
      <th>Average</th>
    </tr>
    <tr>
      <td>{{this.team.expectedGoals}}</td>
      <td>{{this.team.averageGoals}}</td>
    </tr>
  </table>
</template>

<script>
export default {
  name: "infoTable",
  props: [ 'team' ],
}
</script>

<style scoped>
  table {
    margin: auto;
  }
  th, td {
    padding: 10px 20px;
    width: max-content;
  }
</style>