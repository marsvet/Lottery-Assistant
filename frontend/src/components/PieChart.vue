<template>
  <div class="pie-chart-container" :ref="chartRef" style="height: 400px;"></div>
</template>

<script>
export default {
  props: {
    chartRef: String,

    legendData: Array,
    data: Array
  },
  data() {
    return { myChart: null };
  },
  computed: {
    option() {
      return {
        tooltip: {
          trigger: "item"
        },
        legend: {
          left: "center",
          type: "scroll",
          top: "bottom",
          data: this.legendData
        },
        series: [
          {
            type: "pie",
            radius: ["15%", "75%"],
            roseType: "radius",
            data: this.data,
            label: {
              fontWeight: "bold"
            }
          }
        ]
      };
    }
  },
  watch: {
    data() {
      this.myChart.setOption(this.option);
    }
  },
  mounted() {
    this.myChart = this.$echarts.init(this.$refs[this.chartRef]);
    this.myChart.setOption(this.option);
  }
};
</script>
