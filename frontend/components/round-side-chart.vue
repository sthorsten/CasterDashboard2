<template>
  <apexchart type="bar" :options="chartOptions" :series="series"></apexchart>
</template>

<script>
export default {
  name: 'RoundSideChart',

  props: {
    teamBlue: String,
    teamOrange: String,
    atkTeam: String,
    otAtkTeam: String
  },

  data() {
    return {
      chartOptionsBase: {
        title: {
          text: 'Side Wins By Team',
          align: 'center',
          style: {
            color: '#fff'
          }
        },
        chart: {
          type: 'bar',
          stacked: true,
          toolbar: {
            show: false
          }
        },
        dataLabels: {
          formatter: function (val) {
            return `${val}x`
          }
        },
        legend: {
          show: true,
          position: 'bottom',
          labels: {
            colors: ['#fff']
          }
        },
        tooltip: {
          theme: 'dark'
        }
      },
    }
  },

  computed: {
    chartOptions() {
      return {
        ...this.chartOptionsBase,
        xaxis: {
          categories: [
            this.teamBlue, this.teamOrange
          ],
          labels: {
            style: {
              colors: '#fff'
            }
          }
        }
        //labels: this.winTypes,
      }
    },

    rounds() {
      return this.$store.state.matchSocket.rounds
    },

    series() {
      return [
        {
          name: 'ATK',
          data: this.winSeries[0]
        },
        {
          name: 'DEF',
          data: this.winSeries[1]
        }
      ]
    },

    winSeries() {
      const atkWins = [0, 0]
      const defWins = [0, 0]

      this.rounds.forEach(r => {
        if (this.teamBlue === this.atkTeam) {

          if (r.roundNo <= 6) {
            (this.teamBlue === r.winTeamName) ? atkWins[0]++ : defWins[1]++
          } else if (r.roundNo >= 7 && r.roundNo <= 12) {
            (this.teamBlue === r.winTeamName) ? defWins[0]++ : atkWins[1]++
          }

        } else {

          if (r.roundNo <= 6) {
            (this.teamOrange === r.winTeamName) ? atkWins[1]++ : defWins[0]++
          } else if (r.roundNo >= 7 && r.roundNo <= 12) {
            (this.teamOrange === r.winTeamName) ? defWins[1]++ : atkWins[0]++
          }

        }

        if (this.teamBlue === this.otAtkTeam) {

          if (r.roundNo === 13 || r.roundNo === 15) {
            (this.teamBlue === r.winTeamName) ? atkWins[0]++ : defWins[1]++
          }
          if (r.roundNo === 14) {
            (this.teamBlue === r.winTeamName) ? defWins[0]++ : atkWins[1]++
          }

        } else {

          if (r.roundNo === 13 || r.roundNo === 15) {
            (this.teamOrange === trhis.winTeamName) ? atkWins[1]++ : defWins[0]++
          }
          if (r.roundNo === 14) {
            (this.teamOrange === r.winTeamName) ? defWins[1]++ : atkWins[0]++
          }

        }
      })

      return [atkWins, defWins]
    },


    teamBlueSeries() {
      const sideWins = {
        'ATK': 0,
        'DEF': 0
      }
      this.rounds.forEach(r => {
        if (r.winTeamName !== this.teamBlue) return

        if (this.teamBlue === this.atkTeam) {
          if (r.roundNo <= 6) {
            sideWins['ATK']++
          } else if (r.roundNo >= 7 && r.roundNo <= 12) {
            sideWins['DEF']++
          }
        } else {
          if (r.roundNo <= 6) {
            sideWins['DEF']++
          } else if (r.roundNo >= 7 && r.roundNo <= 12) {
            sideWins['ATK']++
          }
        }

        if (this.teamBlue === this.otAtkTeam) {
          if (r.roundNo === 13) sideWins['ATK']++
          if (r.roundNo === 14) sideWins['DEF']++
          if (r.roundNo === 15) sideWins['ATK']++
        } else {
          if (r.roundNo === 13) sideWins['DEF']++
          if (r.roundNo === 14) sideWins['ATK']++
          if (r.roundNo === 15) sideWins['DEF']++
        }
      })
      return Object.values(sideWins)
    },

    teamOrangeSeries() {
      const sideWins = {
        'ATK': 0,
        'DEF': 0
      }
      this.rounds.forEach(r => {
        if (r.winTeamName !== this.teamOrange) return

        if (this.teamOrange === this.atkTeam) {
          if (r.roundNo <= 6) {
            sideWins['ATK']++
          } else if (r.roundNo >= 7 && r.roundNo <= 12) {
            sideWins['DEF']++
          }
        } else {
          if (r.roundNo <= 6) {
            sideWins['DEF']++
          } else if (r.roundNo >= 7 && r.roundNo <= 12) {
            sideWins['ATK']++
          }
        }

        if (this.teamOrange === this.otAtkTeam) {
          if (r.roundNo === 13) sideWins['ATK']++
          if (r.roundNo === 14) sideWins['DEF']++
          if (r.roundNo === 15) sideWins['ATK']++
        } else {
          if (r.roundNo === 13) sideWins['DEF']++
          if (r.roundNo === 14) sideWins['ATK']++
          if (r.roundNo === 15) sideWins['DEF']++
        }
      })
      return Object.values(sideWins)
    },



  }


}
</script>
