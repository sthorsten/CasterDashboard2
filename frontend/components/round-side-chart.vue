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
          stackType: '100%'
        },
        xaxis: {
          categories: ['ATK', 'DEF'],
          labels: {
            style: {
              colors: '#fff'
            }
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
        //labels: this.winTypes,
      }
    },

    rounds() {
      return this.$store.state.matchSocket.rounds
    },

    series() {
      return [
        {
          name: this.teamBlue,
          data: this.teamBlueSeries
        },
        {
          name: this.teamOrange,
          data: this.teamOrangeSeries
        }
      ]
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
