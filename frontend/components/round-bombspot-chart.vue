<template>
  <apexchart
    type="donut"
    :options="chartOptions"
    :series="roundBombSpotSeries"
  ></apexchart>
</template>

<script>
export default {
  name: 'RoundBombspotChart',

  props: {
    mapId: Number
  },

  data() {
    return {
      chartOptionsBase: {
        title: {
          text: 'Played Bomb Spots',
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
        labels: this.bombSpotNames,
      }
    },

    rounds() {
      return this.$store.state.matchSocket.rounds
    },

    roundBombSpotSeries() {
      const bombSpotFrequencies = {}
      this.bombSpotNames.forEach(bs => bombSpotFrequencies[bs] = 0)
      this.rounds.forEach(r => {
        bombSpotFrequencies[r.bombSpotName]++
      })
      return Object.values(bombSpotFrequencies)
    },

    bombSpotNames() {
      if (!this.mapId) return
      const bombSpots = this.$store.getters["coreSocket/getBombSpotsByMap"](this.mapId)
      return bombSpots.map(bs => bs.name)
    },
  }


}
</script>
