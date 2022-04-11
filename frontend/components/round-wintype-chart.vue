<template>
  <apexchart
    type="donut"
    :options="chartOptions"
    :series="roundWinTypeSeries"
  ></apexchart>
</template>

<script>
export default {
  name: 'RoundWintypeChart',

  data() {
    return {
      winTypes: ['Kills', 'Time', 'Defuser Planted', 'Defuser Disabled'],

      chartOptionsBase: {
        title: {
          text: 'Round Win Types',
          align: 'center',
          style: {
            color: '#fff'
          }
        },
        chart: {
          type: 'donut',
        },
        fill: {
          type: 'gradient',
        },
        dataLabels: {
          formatter: function (val, opt) {
            return `${opt.w.config.series[opt.seriesIndex]}x / ${val.toFixed(1)}%`
          }
        },
        legend: {
          show: true,
          position: 'bottom',
          labels: {
            colors: ['#fff']
          }
        },
      },
    }
  },

  computed: {
    chartOptions() {
      return {
        ...this.chartOptionsBase,
        labels: this.winTypes,
      }
    },

    rounds() {
      return this.$store.state.matchSocket.rounds
    },

    roundWinTypeSeries() {
      const winTypeFrequencies = {
        'KILLS': 0,
        'TIME': 0,
        'DEFUSER_PLANTED': 0,
        'DEFUSER_DISABLED': 0,
      }
      this.rounds.forEach(r => {
        winTypeFrequencies[r.winType]++
      })
      return Object.values(winTypeFrequencies)
    },

  }


}
</script>
